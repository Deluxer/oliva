oliva-start:
	uv run python -m app.voice_assistant.assistant start

agent-search-by-superlinked:
	uv run python -m use_cases.agent_search_by_superlinked

agent-search-by-json:
	uv run python -m use_cases.agent_search_by_json

agent-blog-post:
	uv run python -m use_cases.agent_blog_post_url

agent-supervisor:
	uv run python -m use_cases.agent_supervisor