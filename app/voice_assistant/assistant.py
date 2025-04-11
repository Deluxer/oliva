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
from livekit.agents.pipeline import VoicePipelineAgent, AgentCallContext
from livekit.plugins import deepgram, openai, silero, elevenlabs
from app.agents.implementations.supervisor import graph
import os

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
        agent = AgentCallContext.get_current().agent
        local_participant = agent._room.local_participant
        
        try:
            #TODO: pass configurable options from livekit
            config = {
                "configurable": {
                    "user_id": local_participant.identity,
                    "chat_id": local_participant.identity
                }
            }

            input_state = {
                "messages": [
                    {
                        "role": "user",
                        "content": search_products
                    }
                ]
            }

            result = graph.invoke(
                input_state,
                config
            )

            if "messages" in result and result["messages"]:
                message = result["messages"][-1]
                message.pretty_print()
                return message.content
            else:
                logger.warning("No messages in result from graph invocation")
                return "I apologize, but I couldn't process your request properly."

        except Exception as e:
            logger.error(f"Error during graph invocation: {str(e)}", exc_info=True)
            return "I encountered an error while processing your request. Please try again."

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

    dg_model = "nova-2-general"
    if participant.kind == rtc.ParticipantKind.PARTICIPANT_KIND_SIP:
        # use a model optimized for telephony
        dg_model = "nova-2-phonecall"

    elevenlabs_voice = elevenlabs.Voice(
        id="ErXwobaYiN019PkySvjV",
        name="Antoni",
        category="premade",
        settings=elevenlabs.VoiceSettings(
            stability=0.71,
            speed=1.0,
            similarity_boost=0.5,
            style=0.0,
            use_speaker_boost=True,
        ),
    )
    # elevenlabs_tts = elevenlabs.TTS(voice=elevenlabs_voice, model="eleven_flash_v2_5", api_key=os.getenv("ELEVENLABS_API_KEY"), base_url="https://api.elevenlabs.io/v1")

    agent = VoicePipelineAgent(
        vad=ctx.proc.userdata["vad"],
        stt=deepgram.STT(model=dg_model, endpointing_ms=200, no_delay=True, energy_filter=True, interim_results=True),
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
            job_memory_warn_mb=1500,
        ),
    )