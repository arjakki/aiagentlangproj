# MySQL AI Agent

## Architecture

```
frontend/index.html   (vanilla HTML/CSS/JS chat UI)
      ↓ POST /api/chat
app/main.py           (FastAPI)
      ↓ agent_session()
app/agent.py          (LangChain ReAct agent — Claude Sonnet 4.6)
      ↓ MCP stdio subprocess
mcp_server/server.py  (MCP server — 6 MySQL tools)
      ↓ mysql-connector-python
Local MySQL database
```

## Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python 3.11+, FastAPI, Uvicorn |
| AI agent | LangChain, LangGraph (ReAct), Claude Sonnet 4.6 |
| Tool protocol | MCP (stdio) via `mcp` + `langchain-mcp-adapters` |
| Database | MySQL via `mysql-connector-python` |
| Frontend | HTML5 / CSS3 / Vanilla JS |

## Key Files

| File | Purpose |
|---|---|
| `app/agent.py` | `SYSTEM_PROMPT`, `agent_session()` context manager |
| `app/main.py` | FastAPI — `/`, `/api/chat`, `/health` |
| `app/models.py` | Pydantic: `ChatRequest`, `ChatResponse` |
| `mcp_server/server.py` | Six MCP tools over stdio |
| `frontend/index.html` | Chat UI (single page) |
| `.env` | `ANTHROPIC_API_KEY`, MySQL connection vars |

## MCP Tools

| Tool | Description |
|---|---|
| `list_databases` | Show all MySQL databases |
| `list_tables` | Show tables in the configured DB |
| `describe_table` | Column schema + row count |
| `execute_query` | Run a SELECT statement |
| `get_table_sample` | First N rows of a table |
| `get_table_stats` | Min/max/avg/count for numeric columns |

## Development Commands

```bash
pip install -r requirements.txt
cp .env.example .env          # fill in credentials
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## Conventions

- Each `/api/chat` request spawns a fresh MCP subprocess — agent is stateless.
- Only SELECT queries permitted — enforced in both the system prompt and the MCP server.
- Model pinned to `claude-sonnet-4-6` in `app/agent.py`.
- Frontend is a single HTML file — no build step.
