# LangGraph Complete Learning Project

A beginner-to-advanced, runnable set of 25 LangGraph examples organized in the requested folder structure.

## Requirements

- Python 3.10+
- Recommended: Python 3.11 or 3.12
- LangGraph 1.x APIs
- Ollama is needed only for `10_llm_integration.py` and the LLM-backed agent examples.

## Setup (Windows PowerShell)

```powershell
cd langgraph_complete_course
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

If PowerShell blocks activation:
```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

## Ollama setup (LLM examples)

Install Ollama from https://ollama.com, then in a separate terminal run:

```powershell
ollama pull qwen3:4b
ollama serve
```

Keep the Ollama server running. The default model is `qwen3:4b`. You can change it with:
```powershell
$env:OLLAMA_MODEL="qwen3:4b"
```

## Run examples

Run commands from the project root. Example:

```powershell
python -m src.langgraph.01_Basic_Graph.01_First_Graph.01_basic_graph
```

The full command list for every lesson is in `RUN_COMMANDS.md`.

## Important notes

- Every lesson folder contains an `__init__.py`.
- All examples except the Ollama-dependent lessons use local deterministic logic; no API key is required.
- `Memory`, `Checkpointing`, `Persistence`, and `Human-in-the-Loop` examples use LangGraph's in-memory saver/store for learning. Data is not durable across process restarts unless you configure a production database-backed saver/store.
- These are teaching examples, not production security templates.
