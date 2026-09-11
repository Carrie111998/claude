"""Entrypoint for running the MCP server as a module."""

import asyncio
from app.mcp_server import main

if __name__ == "__main__":
    asyncio.run(main())
