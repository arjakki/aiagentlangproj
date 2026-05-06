import asyncio
import json
import os
import sqlite3
from typing import Any

from dotenv import load_dotenv
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp import types

load_dotenv()

_DB_PATH = os.getenv(
    "DB_PATH",
    os.path.join(os.path.dirname(os.path.dirname(__file__)), "ed_database.db"),
)


def get_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(_DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def rows_to_dicts(rows: list[sqlite3.Row]) -> list[dict]:
    return [dict(r) for r in rows]


app = Server("sqlite-mcp-server")


@app.list_tools()
async def list_tools() -> list[types.Tool]:
    return [
        types.Tool(
            name="list_tables",
            description="List all tables in the SQLite database",
            inputSchema={"type": "object", "properties": {}, "required": []},
        ),
        types.Tool(
            name="describe_table",
            description="Return the column schema and row count for a specific table",
            inputSchema={
                "type": "object",
                "properties": {
                    "table_name": {
                        "type": "string",
                        "description": "Name of the table to describe",
                    }
                },
                "required": ["table_name"],
            },
        ),
        types.Tool(
            name="execute_query",
            description=(
                "Execute a read-only SELECT SQL query against the SQLite database "
                "and return results as JSON. Only SELECT statements are permitted."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "A valid SQL SELECT statement",
                    }
                },
                "required": ["query"],
            },
        ),
        types.Tool(
            name="get_table_sample",
            description="Fetch a sample of rows from a table (default 10, max 100)",
            inputSchema={
                "type": "object",
                "properties": {
                    "table_name": {"type": "string", "description": "Name of the table"},
                    "limit": {
                        "type": "integer",
                        "description": "Number of rows to return",
                        "default": 10,
                    },
                },
                "required": ["table_name"],
            },
        ),
        types.Tool(
            name="get_table_stats",
            description="Return min/max/avg/count statistics for numeric columns in a table",
            inputSchema={
                "type": "object",
                "properties": {
                    "table_name": {"type": "string", "description": "Name of the table"}
                },
                "required": ["table_name"],
            },
        ),
    ]


@app.call_tool()
async def call_tool(name: str, arguments: dict[str, Any]) -> list[types.TextContent]:
    try:
        conn = get_connection()
        cur = conn.cursor()

        if name == "list_tables":
            cur.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
            tables = [row["name"] for row in cur.fetchall()]
            return [types.TextContent(type="text", text=json.dumps(tables, indent=2))]

        elif name == "describe_table":
            table = arguments["table_name"]
            cur.execute(f"PRAGMA table_info(\"{table}\")")
            columns = rows_to_dicts(cur.fetchall())
            cur.execute(f"SELECT COUNT(*) AS row_count FROM \"{table}\"")
            count = dict(cur.fetchone())["row_count"]
            result = {"table": table, "columns": columns, "row_count": count}
            return [types.TextContent(type="text", text=json.dumps(result, indent=2, default=str))]

        elif name == "execute_query":
            query = arguments["query"].strip()
            first_word = query.split()[0].upper() if query else ""
            if first_word != "SELECT":
                return [
                    types.TextContent(
                        type="text",
                        text="Error: Only SELECT queries are permitted for safety.",
                    )
                ]
            cur.execute(query)
            rows = rows_to_dicts(cur.fetchall())
            return [types.TextContent(type="text", text=json.dumps(rows, indent=2, default=str))]

        elif name == "get_table_sample":
            table = arguments["table_name"]
            limit = min(int(arguments.get("limit", 10)), 100)
            cur.execute(f"SELECT * FROM \"{table}\" LIMIT {limit}")
            rows = rows_to_dicts(cur.fetchall())
            return [types.TextContent(type="text", text=json.dumps(rows, indent=2, default=str))]

        elif name == "get_table_stats":
            table = arguments["table_name"]
            cur.execute(f"PRAGMA table_info(\"{table}\")")
            columns = rows_to_dicts(cur.fetchall())
            numeric_affinity = {"integer", "real", "numeric"}
            numeric_cols = [
                col["name"]
                for col in columns
                if any(t in col["type"].lower() for t in numeric_affinity)
            ]
            if not numeric_cols:
                return [
                    types.TextContent(
                        type="text",
                        text=f"No numeric columns found in table \"{table}\".",
                    )
                ]
            stats_exprs = ", ".join(
                f'MIN("{c}") AS "{c}_min", MAX("{c}") AS "{c}_max", '
                f'AVG("{c}") AS "{c}_avg", COUNT("{c}") AS "{c}_count"'
                for c in numeric_cols
            )
            cur.execute(f'SELECT {stats_exprs} FROM "{table}"')
            row = dict(cur.fetchone())
            return [types.TextContent(type="text", text=json.dumps(row, indent=2, default=str))]

        else:
            return [types.TextContent(type="text", text=f"Unknown tool: {name}")]

    except Exception as exc:
        return [types.TextContent(type="text", text=f"Error: {exc}")]
    finally:
        conn.close()


async def main():
    async with stdio_server() as (read_stream, write_stream):
        await app.run(read_stream, write_stream, app.create_initialization_options())


if __name__ == "__main__":
    asyncio.run(main())
