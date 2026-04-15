"""MCP Server with dynamic tool discovery - HTTP/streamable-http for llama.cpp webui."""

import sys
import os
import logging
import datetime
import platform
from pathlib import Path

from mcp.server.fastmcp import FastMCP

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("diamcp")

APP_DIR = Path(__file__).parent
APP_TOOLS_DIR = APP_DIR / "tools"

sys.path.insert(0, str(APP_DIR))
sys.path.insert(0, str(APP_TOOLS_DIR))

from base import ToolRegistry
from builtin import register_builtin_tools

mcp = FastMCP(
    "do-it-all-mcp",
    host="0.0.0.0",
    port=8000,
    stateless_http=True,
    json_response=True,
)


@mcp.resource("diamcp://context/time")
def get_time_resource() -> str:
    """Current date and time in ISO format."""
    return datetime.datetime.now().isoformat()


@mcp.resource("diamcp://context/system")
def get_system_resource() -> str:
    """System information for context."""
    info = {
        "platform": platform.platform(),
        "python_version": platform.python_version(),
        "hostname": platform.node(),
    }
    return "\n".join(f"{k}: {v}" for k, v in info.items())


@mcp.resource("diamcp://tools/list")
def get_tools_list() -> str:
    """List of all available tools with descriptions."""
    tools = ToolRegistry.get_all()
    lines = ["Available tools:"]
    for name, tool_def in sorted(tools.items()):
        lines.append(f"- {name}: {tool_def.description[:60]}")
    return "\n".join(lines)


@mcp.prompt(title="Startup Context")
def startup_context() -> str:
    """Get the LLM to call essential tools on startup."""
    return (
        "When starting a new task, first call the following tools to understand your environment:\n"
        "1. get_time - to know the current date/time\n"
        "2. get_system_info - to understand the system you're running on\n"
        "Then proceed with the user's request."
    )


@mcp.prompt(title="Web Research")
def web_research() -> str:
    """Guide for web research tasks."""
    return (
        "For web research tasks:\n"
        "1. Use web_search_brave and web_search_ddg to find relevant pages\n"
        "2. Use web_fetch to extract content from promising URLs\n"
        "3. Use calculate for any math needed\n"
        "4. Summarize findings for the user\n"
        "5. Format beautifully, use markdown, cite sources with links"
    )


def discover_tools_from_dir(tools_dir: Path, source_name: str):
    """Discover and load Python tools from a directory."""
    if not tools_dir.exists():
        return

    for filepath in tools_dir.glob("*.py"):
        if filepath.name.startswith("_"):
            continue
        if filepath.name == "base.py":
            continue

        try:
            import importlib.util

            spec = importlib.util.spec_from_file_location(filepath.stem, filepath)
            if spec and spec.loader:
                module = importlib.util.module_from_spec(spec)
                sys.modules[filepath.stem] = module
                spec.loader.exec_module(module)
                logger.info(f"Loaded tools from {source_name}/{filepath.name}")
        except Exception as e:
            logger.error(f"Failed to load {source_name}/{filepath.name}: {e}")


def discover_user_tools():
    """Discover and load Python tools from tools/ and workspace directories."""
    discover_tools_from_dir(APP_TOOLS_DIR, "tools")


def register_tools():
    """Register all tools from registry with FastMCP."""
    for name, tool_def in ToolRegistry.get_all().items():
        try:
            mcp.add_tool(
                tool_def.func, name=tool_def.name, description=tool_def.description
            )
            logger.info(f"Registered tool: {tool_def.name}")
        except Exception as e:
            logger.error(f"Failed to register tool {tool_def.name}: {e}")


def main():
    """Start the MCP server."""
    register_builtin_tools()
    discover_user_tools()
    register_tools()

    logger.info(f"diaMCP Server starting on 0.0.0.0:8000")
    logger.info(f"Tools loaded: {len(ToolRegistry.get_all())}")

    mcp.run(transport="streamable-http")


if __name__ == "__main__":
    main()
