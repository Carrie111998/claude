"""MCP server exposing OmniRoute as tools and resources."""

import json
from mcp.server import Server
from mcp.types import Tool, TextContent

from app.omniroute.client import OmniRouteClient
from app.config import Settings

settings = Settings()  # type: ignore[call-arg]

# Use multi-endpoint support
endpoint_map = {
    "public": settings.omniroute_base_url,
    "cloudflare": settings.omniroute_cloudflare_url,
    "local": settings.omniroute_local_url,
    "network": settings.omniroute_network_url,
}
base_url = endpoint_map.get(settings.omniroute_endpoint, settings.omniroute_base_url)
client = OmniRouteClient(
    base_url=base_url,
    api_key=settings.omniroute_api_key,
)

server = Server("omniroute-mcp")


@server.list_tools()
async def list_tools() -> list[Tool]:
    """Expose OmniRoute operations as tools."""
    return [
        Tool(
            name="local_list_agents",
            description="List all locally stored agents",
            inputSchema={
                "type": "object",
                "properties": {
                    "skip": {
                        "type": "integer",
                        "description": "Number of agents to skip",
                        "default": 0,
                    },
                    "limit": {
                        "type": "integer",
                        "description": "Maximum number of agents to return",
                        "default": 100,
                    },
                },
                "required": [],
            },
        ),
        Tool(
            name="local_get_agent",
            description="Get a locally stored agent by ID",
            inputSchema={
                "type": "object",
                "properties": {
                    "agent_id": {
                        "type": "string",
                        "description": "The local agent ID",
                    }
                },
                "required": ["agent_id"],
            },
        ),
        Tool(
            name="omniroute_list_models",
            description="List all available models in OmniRoute",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": [],
            },
        ),
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
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    """Execute agent operations (local and OmniRoute)."""
    try:
        if name == "local_list_agents":
            from app.db import SessionLocal
            from app.services import AgentService

            db = SessionLocal()
            try:
                skip = arguments.get("skip", 0)
                limit = arguments.get("limit", 100)
                agents = AgentService.list_agents(db, skip=skip, limit=limit)
                agent_list = [
                    {
                        "id": a.id,
                        "name": a.name,
                        "alias": a.alias,
                        "endpoint_url": a.endpoint_url,
                        "status": a.status,
                    }
                    for a in agents
                ]
                return [
                    TextContent(
                        type="text",
                        text=json.dumps(agent_list, indent=2),
                    )
                ]
            finally:
                db.close()

        elif name == "local_get_agent":
            from app.db import SessionLocal
            from app.services import AgentService

            db = SessionLocal()
            try:
                agent = AgentService.get_agent(db, arguments["agent_id"])
                if not agent:
                    return [TextContent(type="text", text="Agent not found")]
                return [
                    TextContent(
                        type="text",
                        text=json.dumps(
                            {
                                "id": agent.id,
                                "name": agent.name,
                                "alias": agent.alias,
                                "endpoint_url": agent.endpoint_url,
                                "status": agent.status,
                                "created_at": agent.created_at.isoformat(),
                            },
                            indent=2,
                        ),
                    )
                ]
            finally:
                db.close()

        elif name == "omniroute_list_models":
            models = await client.list_models()
            return [
                TextContent(
                    type="text",
                    text=json.dumps(models, indent=2),
                )
            ]

        elif name == "omniroute_list_agents":
            agents = await client.list_agents()
            return [
                TextContent(
                    type="text",
                    text=json.dumps(agents, indent=2),
                )
            ]

        elif name == "omniroute_get_agent":
            agent = await client.get_agent(arguments["agent_id"])
            return [
                TextContent(
                    type="text",
                    text=json.dumps(agent, indent=2),
                )
            ]

        elif name == "omniroute_add_agent":
            agent = await client.get_agent(arguments["agent_id"])
            if "alias" in arguments:
                agent["alias"] = arguments["alias"]
            return [
                TextContent(
                    type="text",
                    text=json.dumps(agent, indent=2),
                )
            ]

        elif name == "omniroute_create_agent":
            payload = {
                "name": arguments["name"],
                "endpoint_url": arguments["endpoint_url"],
                "description": arguments.get("description"),
                "capabilities": arguments.get("capabilities", []),
                "metadata": arguments.get("metadata", {}),
            }
            agent = await client.create_agent(payload)
            return [
                TextContent(
                    type="text",
                    text=json.dumps(agent, indent=2),
                )
            ]

        elif name == "omniroute_delete_agent":
            await client.delete_agent(arguments["agent_id"])
            return [
                TextContent(
                    type="text",
                    text=f"Agent {arguments['agent_id']} deleted successfully",
                )
            ]

        else:
            return [TextContent(type="text", text=f"Unknown tool: {name}")]

    except Exception as e:
        return [TextContent(type="text", text=f"Error: {str(e)}")]


async def main():
    """Run the MCP server."""
    async with server:
        print("OmniRoute MCP server running...")
        await server.wait_for_shutdown()


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
