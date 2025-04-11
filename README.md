<div align="center">
  <h1>Oliva Multi-Agent Assistant</h1>
</div>
<p align="center">Oliva is a multi-agent assistant that combines different agents to handle various tasks. These agents can be used to perform various tasks such as semantic search, text generation, question answering, and more. The project is designed to be flexible and extensible, allowing you to add more agents as needed.</p>

<p align="center">
  <img src="assets/oliva_arquitecture_v2.png" alt="Oliva architecture" width="800">
</p>

### Requirements:

<table>
<thead>
  <tr>
    <th>Requirement</th>
    <th>Description</th>
  </tr>
</thead>
<tbody>
  <tr>
    <td>Database Population</td>
    <td>Follow the setup instructions in the <a href="https://github.com/decodingml/tabular-semantic-search-tutorial">tabular-semantic-search-tutorial</a> or download the snapshot in <code>assets/snapshot.zip</code></td>
  </tr>
  <tr>
    <td>Qdrant</td>
    <td>Vector database for efficient similarity search and storage of embeddings.</td>
  </tr>
  <tr>
    <td>Superlinked</td>
    <td>Framework for building AI applications with semantic search capabilities.</td>
  </tr>
  <tr>
    <td>Deepgram Account</td>
    <td>Speech-to-text service account required for converting voice input into text.</td>
  </tr> 
  <tr>
    <td>Livekit Account</td>
    <td>Real-time communication platform needed for handling voice interactions.</td>
  </tr>
  <tr>
    <td>Python Knowledge</td>
    <td>Understanding of Python programming language (version 3.12+).</td>
  </tr>
</tbody>
</table>

### Installation
1. Install project dependencies:
```bash
uv sync
```

This will create a virtual environment in `.venv` and install all required dependencies.

2. Livekit account

Create a Livekit account in [Livekit Cloud](https://cloud.livekit.io/login) and get `LIVEKIT_URL`, `LIVEKIT_API_KEY` and `LIVEKIT_API_SECRET`.


```bash
LIVEKIT_URL=wss://your-project.livekit.cloud
LIVEKIT_API_KEY=secret
LIVEKIT_API_SECRET=********
```

3. Environment variables

Before running any Python scripts, set the following environment variables:
```bash
cp .env.example .env
```

4. Qdrant

Use docker to run Qdrant, set an API key wherever you want:
```bash
docker run -p 6333:6333 -p 6334:6334 \
    -e QDRANT__SERVICE__API_KEY=******** \
    -v "$(pwd)/qdrant_storage:/qdrant/storage:z" \
    qdrant/qdrant
```

## Usage

### Voice assistant
```bash
make oliva-start
```

### Voice assistant frontend

Use [Agent playground](https://agents-playground.livekit.io/) and connect with your Livekit project to interact with the voice assistant.
If you prefer run locally, download the repo [Agent playground](https://github.com/livekit/agents-playground) and run `npm run start`.


<p align="center">
  <img src="assets/livekit_playground.png" alt="Livekit Agent Playground" width="900">
</p>


## Project Structure

```
oliva/
├── app/
│    ├── agents/
│    │   ├── implementations/     # Individual agent implementations
│    │   ├── core/       # Base classes and interfaces for agent components
│    │   └── langchain/
│    │       ├── base/      # Base LangChain integration classes
│    │       ├── config/    # LangChain configuration
│    │       ├── edges/     # Edge conditions for workflow routing
│    │       ├── nodes/     # Node implementations (agent, rewrite, generate)
│    │       └── tools/     # LangChain-specific tools
│    ├── voice_assistant/
│    └── utils/              # Shared utilities
```

### Architecture Overview

The project follows a modular architecture implementing an agentic RAG (Retrieval-Augmented Generation) system:

1. **Agent Components** (`app/agents/`)
   - `agents/`: Contains specific agent implementations
   - `core/`: Defines core interfaces and abstract classes for:
     - State management
     - Node implementations
     - Edge conditions
     - Tool interfaces
     - Graph workflow definitions

2. **LangChain Integration** (`app/agents/integrations/langchain/`)
   - Provides LangChain-specific implementations for:
     - Document retrieval
     - Tool operations
     - State management
     - Workflow nodes and edges

3. **Voice Assistant** (`app/voice_assistant/`)
   - LiveKit integration
      * Voice interface implementation
      * Speech-to-text and text-to-speech capabilities

4. **Utilities** (`app/utils/`)
   - Shared helper functions
   - Common utilities used across modules

The system implements a graph-based workflow where each agent processes state through a series of nodes (functions) connected by conditional edges, supporting dynamic routing based on the agent's decisions.

## Use cases

Langchain workflow by supervisor agent
```bash
make agent-supervisor
```

Langchain workflow by superlinked
```bash
make agent-search-by-superlinked
```

Langchain workflow by json file
```bash
make agent-search-by-json
```

## Tech Stack

<table>
<thead>
  <tr>
    <th>Technology</th>
    <th>Version/Type</th>
    <th>Role</th>
  </tr>
</thead>
<tbody>
  <tr>
    <td><a href="https://python.langchain.com">Langchain</a></td>
    <td>Latest</td>
    <td>LLM application framework</td>
  </tr>
  <tr>
    <td><a href="https://livekit.io">Livekit</a></td>
    <td>Cloud/Self-hosted</td>
    <td>Real-time voice communication</td>
  </tr>
  <tr>
    <td><a href="https://qdrant.tech">Qdrant</a></td>
    <td>Vector DB</td>
    <td>Semantic search storage</td>
  </tr>
  <tr>
    <td><a href="https://superlinked.com">Superlinked</a></td>
    <td>Framework</td>
    <td>Semantic search capabilities</td>
  </tr>
  <tr>
    <td><a href="https://deepgram.com">Deepgram</a></td>
    <td>API Service</td>
    <td>Speech-to-text conversion</td>
  </tr>
  <tr>
    <td><a href="https://openai.com">OpenAI</a></td>
    <td>API Service</td>
    <td>LLM provider</td>
  </tr>
  <tr>
    <td><a href="https://python.org">Python</a></td>
    <td>3.12+</td>
    <td>Core implementation</td>
  </tr>
</tbody>
</table>

## 📚 Contributing

This project is open-source and welcomes contributions from the community. For more details on how to contribute, please refer to the [Contributing Guide](./CONTRIBUTING.md).