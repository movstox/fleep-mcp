#!/usr/bin/env python3
"""
Fleep MCP Server

An MCP server that provides tools for interacting with the Fleep.io API.
"""

import asyncio
import logging
from typing import Any, Dict, List, Optional

from mcp.server import Server
from mcp.server.models import InitializationOptions
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent, CallToolRequestParams, ServerCapabilities

from .fleep_client import FleepClient
from .tools.create_conversation import CreateConversationTool
from .tools.send_message import SendMessageTool

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize the MCP server
server = Server("fleep-mcp")

# Initialize Fleep client
fleep_client = FleepClient()

# Initialize tools
create_conversation_tool = CreateConversationTool(fleep_client)
send_message_tool = SendMessageTool(fleep_client)


@server.list_tools()
async def handle_list_tools() -> List[Tool]:
    """Return the list of available tools."""
    return [
        create_conversation_tool.get_tool_definition(),
        send_message_tool.get_tool_definition(),
    ]


@server.call_tool()
async def handle_call_tool(
    name: str, arguments: Optional[Dict[str, Any]] = None
) -> List[TextContent]:
    """Handle tool execution requests."""
    if arguments is None:
        arguments = {}
    
    try:
        if name == "create_conversation":
            result = await create_conversation_tool.execute(arguments)
            return [TextContent(type="text", text=str(result))]
        elif name == "send_message":
            result = await send_message_tool.execute(arguments)
            return [TextContent(type="text", text=str(result))]
        else:
            raise ValueError(f"Unknown tool: {name}")
    except Exception as e:
        logger.error(f"Error executing tool {name}: {e}")
        return [TextContent(type="text", text=f"Error: {str(e)}")]


async def main() -> None:
    """Main entry point for the MCP server."""
    logger.info("Starting Fleep MCP Server...")
    
    # Run the server using stdio transport
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="fleep-mcp",
                server_version="0.1.0",
                capabilities=ServerCapabilities(
                    tools={"listChanged": True}
                ),
            ),
        )

if __name__ == "__main__":
    asyncio.run(main())
