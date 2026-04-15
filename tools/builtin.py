"""Built-in tools for the MCP server."""

import json
import re
import subprocess
from base import tool


@tool(
    name="simple_search",
    description="Search the web using DuckDuckGo",
    schema={
        "type": "object",
        "properties": {
            "query": {"type": "string", "description": "Search query"},
            "num_results": {
                "type": "integer",
                "description": "Number of results (default: 5)",
            },
        },
        "required": ["query"],
    },
)
def simple_search(query: str, num_results: int = 5) -> str:
    """Search the web using DuckDuckGo."""
    try:
        from ddgs import DDGS

        results = []
        with DDGS() as ddgs:
            for r in ddgs.text(query, max_results=num_results):
                results.append(f"Title: {r['title']}\nURL: {r['href']}\n{r['body']}\n")

        if not results:
            return "No results found"
        return "\n---\n".join(results)
    except ImportError:
        return "Error: ddgs not installed. Run: pip install ddgs"
    except Exception as e:
        return f"Error performing search: {e}"


@tool(
    name="simple_fetch",
    description="Fetch and extract text content from a web page",
    schema={
        "type": "object",
        "properties": {
            "url": {"type": "string", "description": "URL to fetch"},
            "max_length": {
                "type": "integer",
                "description": "Max characters to return (default: 120000)",
            },
        },
        "required": ["url"],
    },
)
def simple_fetch(url: str, max_length: int = 120000) -> str:
    """Fetch content from a URL."""
    try:
        import httpx
        from selectolax.lexbor import LexborHTMLParser as HTMLParser

        headers = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'cache-control': 'no-cache',
            'pragma': 'no-cache',
            'user-agent': 'Mozilla/5.0 (X11; FreeBSD AMD64; rv:150.0) Gecko/20100101 Firefox/150.0',
        }
        with httpx.Client(headers=headers, http2=True, follow_redirects=True, timeout=10) as client:
            response = client.get(url)
            response.raise_for_status()

        tree = HTMLParser(response.text)
        for tag in tree.css("script, style, nav, footer, header"):
            tag.decompose()

        text = tree.text()
        if len(text) > max_length:
            text = (
                text[:max_length]
                + f"\n... [truncated, full content: {len(text)} chars]"
            )
        return text.strip()
    except ImportError:
        return "Error: httpx or selectolax not installed"
    except Exception as e:
        return f"Error fetching URL: {e}"


@tool(
    name="get_time",
    description="Get the current date and time",
    schema={
        "type": "object",
        "properties": {
            "timezone": {
                "type": "string",
                "description": "Timezone (e.g., 'UTC', 'America/New_York')",
            }
        },
        "required": [],
    },
)
def get_time(timezone: str = "UTC") -> str:
    """Get current time in specified timezone."""
    import datetime

    try:
        if timezone != "UTC":
            import zoneinfo

            tz = zoneinfo.ZoneInfo(timezone)
            now = datetime.datetime.now(tz)
        else:
            now = datetime.datetime.utcnow()
        return now.isoformat()
    except Exception as e:
        return f"Error: {e}"


@tool(
    name="calculate",
    description="Perform mathematical calculations",
    schema={
        "type": "object",
        "properties": {
            "expression": {
                "type": "string",
                "description": "Math expression (e.g., '2+2', 'sqrt(16)', 'sin(pi/2)')",
            }
        },
        "required": ["expression"],
    },
)
def calculate(expression: str) -> str:
    """Evaluate a mathematical expression."""
    try:
        import math

        allowed_names = {
            k: v for k, v in math.__dict__.items() if not k.startswith("_")
        }
        allowed_names.update(
            {"abs": abs, "round": round, "min": min, "max": max, "pow": pow}
        )

        result = eval(expression, {"__builtins__": {}, **allowed_names})
        return str(result)
    except Exception as e:
        return f"Error: {e}"


def register_builtin_tools():
    """Register all built-in tools with the registry."""
    from base import ToolRegistry

    builtin_tools = [
        simple_search,
        simple_fetch,
        get_time,
        calculate,
    ]

    for t in builtin_tools:
        ToolRegistry.register(
            name=t.__name__,
            description=t.__doc__ or "",
            func=t,
            input_schema=t.__annotations__ if hasattr(t, "__annotations__") else {},
        )
