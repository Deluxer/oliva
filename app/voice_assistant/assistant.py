import asyncio
import logging
from typing import Annotated
from livekit import rtc
from dotenv import load_dotenv
from livekit.agents import (
    AutoSubscribe,
    JobContext,
    JobProcess,
    WorkerOptions,
    cli,
    llm,
    metrics,
)
from livekit.agents.llm import (
    ChatContext,
    ChatMessage,
    FunctionContext
)
from livekit.agents.pipeline import VoicePipelineAgent
from livekit.plugins import deepgram, openai, silero
from app.agents.implementations.search_amazon_products.agent_by_superlinked import SearchAmazonProductsAgentBySuperlinked

from app.utils.prompts import Prompts

load_dotenv()
logger = logging.getLogger("oliva-voice-assistant")


def prewarm(proc: JobProcess):
    proc.userdata["vad"] = silero.VAD.load()

class SearchProducts(FunctionContext):
    """The class defines a set of LLM functions that the assistant can execute. """

    @llm.ai_callable(name="search_products", description="Called when asked to search for products in oliva database")
    async def search_products(
        self,
        search_products: Annotated[
            str,
            llm.TypeInfo(description="Search for products by title, description, category, price, rating, and review"),
        ],
    ):  
        try:
            agent = SearchAmazonProductsAgentBySuperlinked()
            result = agent.process({
                "query": search_products
            })

            return result
        except Exception as e:
            print(f"Superlinked call failed: {e}")

        return None


async def entrypoint(ctx: JobContext):
    fnc_ctx = SearchProducts()
    initial_ctx = ChatContext().append(
        role="system",
        text=Prompts.ASSISTANT_SYSTEM,
    )

    logger.info(f"connecting to room {ctx.room.name}")
    await ctx.connect(auto_subscribe=AutoSubscribe.AUDIO_ONLY)

    # wait for the first participant to connect
    participant = await ctx.wait_for_participant()
    logger.info(f"starting voice assistant for participant {participant.identity}")

    dg_model = "nova-3-general"
    if participant.kind == rtc.ParticipantKind.PARTICIPANT_KIND_SIP:
        # use a model optimized for telephony
        dg_model = "nova-2-phonecall"

    agent = VoicePipelineAgent(
        vad=ctx.proc.userdata["vad"],
        stt=deepgram.STT(model=dg_model),
        llm=openai.LLM(),
        tts=openai.TTS(),
        chat_ctx=initial_ctx,
        fnc_ctx=fnc_ctx
    )

    agent.start(ctx.room, participant)

    usage_collector = metrics.UsageCollector()

    @agent.on("metrics_collected")
    def _on_metrics_collected(mtrcs: metrics.AgentMetrics):
        # metrics.log_metrics(mtrcs)
        usage_collector.collect(mtrcs)

    async def log_usage():
        summary = usage_collector.get_summary()
        logger.info(f"Usage: ${summary}")

    ctx.add_shutdown_callback(log_usage)

    # listen to incoming chat messages, only required if you'd like the agent to
    # answer incoming messages from Chat
    chat = rtc.ChatManager(ctx.room)

    async def answer_from_text(txt: str):
        chat_ctx = agent.chat_ctx.copy()
        chat_ctx.append(role="user", text=txt)
        stream = agent.llm.chat(chat_ctx=chat_ctx)
        await agent.say(stream)

    @chat.on("message_received")
    def on_chat_received(msg: ChatMessage):
        if msg.message:
            asyncio.create_task(answer_from_text(msg.message))

    await agent.say("Hey, how can I help you today?", allow_interruptions=True)


if __name__ == "__main__":
    cli.run_app(
        WorkerOptions(
            entrypoint_fnc=entrypoint,
            prewarm_fnc=prewarm,
            job_memory_warn_mb=1300,
        ),
    )