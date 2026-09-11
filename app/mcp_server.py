"""MCP server exposing OmniRoute as tools and resources."""

import json
from mcp.server import Server
from mcp.types import (
    Tool,
    TextContent,
    ToolResult,
)

from app.omniroute.client import OmniRouteClient
from app.config import Settings

settings = Settings()  # type: ignore[call-arg]
client = OmniRouteClient(
    base_url=settings.omniroute_base_url,
    api_key=settings.omniroute_api_key,
)

server = Server("omniroute-mcp")


@server.list_tools()
async def list_tools() -> list[Tool]:
    """Expose OmniRoute operations as tools."""
    return [
        Tool(
            name="omniroute_list_agents",
            description="List all agents available in OmniRoute",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": [],
            },
        ),
        Tool(
            name="omniroute_get_agent",
            description="Fetch a single OmniRoute agent by ID",
            inputSchema={
                "type": "object",
                "properties": {
                    "agent_id": {
                        "type": "string",
                        "description": "The OmniRoute agent ID",
                    }
                },
                "required": ["agent_id"],
            },
        ),
        Tool(
            name="omniroute_add_agent",
            description="Import an existing OmniRoute agent with optional local alias",
            inputSchema={
                "type": "object",
                "properties": {
                    "agent_id": {
                        "type": "string",
                        "description": "OmniRoute agent ID to import",
                    },
                    "alias": {
                        "type": "string",
                        "description": "Optional local friendly name for this agent",
                    },
                },
                "required": ["agent_id"],
            },
        ),
        Tool(
            name="omniroute_create_agent",
            description="Register a brand-new agent in OmniRoute",
            inputSchema={
                "type": "object",
                "properties": {
                    "name": {
                        "type": "string",
                        "description": "Display name for the agent",
                    },
                    "description": {
                        "type": "string",
                        "description": "Agent description",
                    },
                    "endpoint_url": {
                        "type": "string",
                        "description": "HTTP endpoint the agent listens on",
                    },
                    "capabilities": {
                        "type": "array",
                        "description": "Agent capabilities",
                        "items": {
                            "type": "object",
                            "properties": {
                                "name": {"type": "string"},
                                "description": {"type": "string"},
                            },
                        },
                    },
                    "metadata": {
                        "type": "object",
                        "description": "Custom metadata",
                    },
                },
                "required": ["name", "endpoint_url"],
            },
        ),
        Tool(
            name="omniroute_delete_agent",
            description="Remove an agent from OmniRoute",
            inputSchema={
                "type": "object",
                "properties": {
                    "agent_id": {
                        "type": "string",
                        "description": "OmniRoute agent ID to delete",
                    }
                },
                "required": ["agent_id"],
            },
        ),
    ]


@server.call_tool()
async def call_tool(name: str, arguments: dict) -> ToolResult:
    """Execute OmniRoute operations."""
    try:
        if name == "omniroute_list_agents":
            agents = await client.list_agents()
            return ToolResult(
                content=[
                    TextContent(
                        type="text",
                        text=json.dumps(agents, indent=2),
                    )
                ],
            )

        elif name == "omniroute_get_agent":
            agent = await client.get_agent(arguments["agent_id"])
            return ToolResult(
                content=[
                    TextContent(
                        type="text",
                        text=json.dumps(agent, indent=2),
                    )
                ],
            )

        elif name == "omniroute_add_agent":
            agent = await client.get_agent(arguments["agent_id"])
            if "alias" in arguments:
                agent["alias"] = arguments["alias"]
            return ToolResult(
                content=[
                    TextContent(
                        type="text",
                        text=json.dumps(agent, indent=2),
                    )
                ],
            )

        elif name == "omniroute_create_agent":
            payload = {
                "name": arguments["name"],
                "endpoint_url": arguments["endpoint_url"],
                "description": arguments.get("description"),
                "capabilities": arguments.get("capabilities", []),
                "metadata": arguments.get("metadata", {}),
            }
            agent = await client.create_agent(payload)
            return ToolResult(
                content=[
                    TextContent(
                        type="text",
                        text=json.dumps(agent, indent=2),
                    )
                ],
            )

        elif name == "omniroute_delete_agent":
            await client.delete_agent(arguments["agent_id"])
            return ToolResult(
                content=[
                    TextContent(
                        type="text",
                        text=f"Agent {arguments['agent_id']} deleted successfully",
                    )
                ],
            )

        else:
            return ToolResult(
                content=[TextContent(type="text", text=f"Unknown tool: {name}")],
                is_error=True,
            )

    except Exception as e:
        return ToolResult(
            content=[TextContent(type="text", text=f"Error: {str(e)}")],
            is_error=True,
        )


async def main():
    """Run the MCP server."""
    async with server:
        print("OmniRoute MCP server running...")
        await server.wait_for_shutdown()


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
