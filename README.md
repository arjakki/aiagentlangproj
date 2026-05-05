# MySQL AI Agent

A web-based chat application that lets you query a **MySQL database in plain English** using a LangChain ReAct agent backed by Claude Sonnet 4.6, exposed through an MCP server.

## Architecture

```
Browser (chat UI)
    └─ POST /api/chat
FastAPI (app/main.py)
    └─ LangChain ReAct agent (app/agent.py)
        └─ MCP stdio subprocess (mcp_server/server.py)
            └─ MySQL database
```

## Quick Start

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure environment

```bash
cp .env.example .env
```

Edit `.env`:

```env
ANTHROPIC_API_KEY=sk-ant-...

MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_USER=root
MYSQL_PASSWORD=your-password
MYSQL_DATABASE=your-database
```

### 3. Run

```bash
# Windows
start.bat

# macOS / Linux
./start.sh
```

Then open **http://localhost:8000** in your browser.

## What you can ask

- *"What tables are in this database?"*
- *"Show me the first 10 rows of the customers table"*
- *"How many orders were placed last month?"*
- *"What are the top 5 products by revenue?"*
- *"Describe the schema of the users table"*

## MCP Tools

| Tool | What it does |
|---|---|
| `list_databases` | List all MySQL databases |
| `list_tables` | List tables in the connected database |
| `describe_table` | Column types + row count |
| `execute_query` | Run any SELECT query |
| `get_table_sample` | Preview N rows |
| `get_table_stats` | Numeric column statistics |

> Only `SELECT` statements are allowed — writes are blocked at the MCP layer.

## Tech Stack

- **LangChain / LangGraph** — ReAct agent loop
- **Claude Sonnet 4.6** — LLM via `langchain-anthropic`
- **MCP** — tool protocol between agent and database
- **FastAPI + Uvicorn** — async web server
- **mysql-connector-python** — MySQL driver
- **Vanilla HTML/CSS/JS** — zero-build frontend
