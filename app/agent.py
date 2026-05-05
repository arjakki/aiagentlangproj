import os
import sys
from contextlib import asynccontextmanager

from dotenv import load_dotenv
from langchain_anthropic import ChatAnthropic
from langchain_core.messages import SystemMessage
from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent

load_dotenv()

_MCP_SERVER = os.path.join(os.path.dirname(os.path.dirname(__file__)), "mcp_server", "server.py")

SYSTEM_PROMPT = """You are a helpful MySQL database assistant. You have access to tools that let \
you explore and query a MySQL database.

When answering questions:
1. First explore the schema (list_tables, describe_table) if you need to understand the structure.
2. Write precise SELECT queries via execute_query to fetch the data the user needs.
3. Present results clearly — use markdown tables for tabular data, bullet lists for summaries.
4. Explain what the data means in plain language after showing it.
5. If a query returns many rows, summarise the key findings instead of dumping everything.

Rules:
- Only SELECT queries are allowed — never attempt INSERT, UPDATE, DELETE, or DDL.
- If the user asks for something that would require a write, explain why it is not permitted.
- When in doubt about a table name or column, call describe_table first.
"""


@asynccontextmanager
async def agent_session():
    python = sys.executable
    async with MultiServerMCPClient(
        {
            "mysql": {
                "command": python,
                "args": [_MCP_SERVER],
                "transport": "stdio",
            }
        }
    ) as client:
        tools = client.get_tools()
        model = ChatAnthropic(
            model="claude-sonnet-4-6",
            temperature=0,
            anthropic_api_key=os.getenv("ANTHROPIC_API_KEY"),
        )
        agent = create_react_agent(
            model,
            tools,
            state_modifier=SystemMessage(content=SYSTEM_PROMPT),
        )
        yield agent
