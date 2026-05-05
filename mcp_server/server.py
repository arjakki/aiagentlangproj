import asyncio
import json
import os
import sys
from typing import Any

import mysql.connector
from dotenv import load_dotenv
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp import types

load_dotenv()


def get_connection():
    return mysql.connector.connect(
        host=os.getenv("MYSQL_HOST", "localhost"),
        port=int(os.getenv("MYSQL_PORT", "3306")),
        user=os.getenv("MYSQL_USER", "root"),
        password=os.getenv("MYSQL_PASSWORD", ""),
        database=os.getenv("MYSQL_DATABASE", ""),
    )


app = Server("mysql-mcp-server")


@app.list_tools()
async def list_tools() -> list[types.Tool]:
    return [
        types.Tool(
            name="list_databases",
            description="List all databases available on the MySQL server",
            inputSchema={"type": "object", "properties": {}, "required": []},
        ),
        types.Tool(
            name="list_tables",
            description="List all tables in the currently selected MySQL database",
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
                "Execute a read-only SELECT SQL query against the MySQL database "
                "and return the results as JSON. Only SELECT statements are permitted."
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
            description="Fetch a sample of rows from a table (default 10 rows)",
            inputSchema={
                "type": "object",
                "properties": {
                    "table_name": {"type": "string", "description": "Name of the table"},
                    "limit": {
                        "type": "integer",
                        "description": "Number of rows to return (default 10, max 100)",
                        "default": 10,
                    },
                },
                "required": ["table_name"],
            },
        ),
        types.Tool(
            name="get_table_stats",
            description="Return basic statistics (min, max, avg, count) for numeric columns in a table",
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
    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        if name == "list_databases":
            cursor.execute("SHOW DATABASES")
            rows = cursor.fetchall()
            databases = [row["Database"] for row in rows]
            return [types.TextContent(type="text", text=json.dumps(databases, indent=2))]

        elif name == "list_tables":
            cursor.execute("SHOW TABLES")
            rows = cursor.fetchall()
            tables = [list(row.values())[0] for row in rows]
            return [types.TextContent(type="text", text=json.dumps(tables, indent=2))]

        elif name == "describe_table":
            table = arguments["table_name"]
            cursor.execute(f"DESCRIBE `{table}`")
            columns = cursor.fetchall()
            cursor.execute(f"SELECT COUNT(*) AS row_count FROM `{table}`")
            count = cursor.fetchone()
            result = {"table": table, "columns": columns, "row_count": count["row_count"]}
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
            cursor.execute(query)
            rows = cursor.fetchall()
            return [
                types.TextContent(
                    type="text", text=json.dumps(rows, indent=2, default=str)
                )
            ]

        elif name == "get_table_sample":
            table = arguments["table_name"]
            limit = min(int(arguments.get("limit", 10)), 100)
            cursor.execute(f"SELECT * FROM `{table}` LIMIT {limit}")
            rows = cursor.fetchall()
            return [
                types.TextContent(
                    type="text", text=json.dumps(rows, indent=2, default=str)
                )
            ]

        elif name == "get_table_stats":
            table = arguments["table_name"]
            cursor.execute(f"DESCRIBE `{table}`")
            columns = cursor.fetchall()
            numeric_types = {"int", "bigint", "smallint", "tinyint", "float", "double", "decimal"}
            numeric_cols = [
                col["Field"]
                for col in columns
                if any(t in col["Type"].lower() for t in numeric_types)
            ]
            if not numeric_cols:
                return [
                    types.TextContent(
                        type="text",
                        text=f"No numeric columns found in table `{table}`.",
                    )
                ]
            stats_exprs = ", ".join(
                f"MIN(`{c}`) AS `{c}_min`, MAX(`{c}`) AS `{c}_max`, "
                f"AVG(`{c}`) AS `{c}_avg`, COUNT(`{c}`) AS `{c}_count`"
                for c in numeric_cols
            )
            cursor.execute(f"SELECT {stats_exprs} FROM `{table}`")
            row = cursor.fetchone()
            return [
                types.TextContent(
                    type="text", text=json.dumps(row, indent=2, default=str)
                )
            ]

        else:
            return [types.TextContent(type="text", text=f"Unknown tool: {name}")]

    except Exception as exc:
        return [types.TextContent(type="text", text=f"Error: {exc}")]
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()


async def main():
    async with stdio_server() as (read_stream, write_stream):
        await app.run(read_stream, write_stream, app.create_initialization_options())


if __name__ == "__main__":
    asyncio.run(main())
