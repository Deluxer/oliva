### Installation

1. Create Python environment and install Python:
```bash
uv python install
```

2. Install project dependencies:
```bash
uv sync
```

Restart the environment:
```bash
rm -rf .venv
```

This will create a virtual environment in `.venv` and install all required dependencies.

### Activate the Environment

Before running any Python scripts, activate the virtual environment:
```bash
source .venv/bin/activate
```

### Usage
```bash
uv run python -m assistant start
uv run python -m app.voice_assistant.assistant start
python assistant.py start
```

### test lagchain workflow
```bash
uv run python -m run
```