import asyncio
import os
from typing import Any
from base import tool

from ddgs import DDGS
from ddgs.utils import _expand_proxy_tb_alias

@tool(
    name="search_text",
    description="Perform a text search using DDGS.",
    schema={
        "type": "object",
        "properties": {
            "query": {"type": "string", "description": "Search query string"},
            "region": {"type": "string", "description": "Region for search (e.g., us-en, uk-en, ru-ru)", "default": "us-en"},
            "safesearch": {"type": "string", "description": "Safe search setting (on, moderate, off)", "default": "off"},
            "timelimit": {"type": "string", "description": "Time limit (d, w, m, y) or custom date range", "nullable": True},
            "max_results": {"type": "integer", "description": "Maximum number of results to return", "default": 10},
            "page": {"type": "integer", "description": "Page number of results", "default": 1},
            "backend": {"type": "string", "description": "Search backend (auto, or specific engine)", "default": "auto"},
        },
        "required": ["query"],
    },
)
async def search_text(
    query: str,
    region: str = "us-en",
    safesearch: str = "off",
    timelimit: str | None = None,
    max_results: int = 10,
    page: int = 1,
    backend: str = "auto",
) -> list[dict[str, Any]]:
    """Perform a text search using DDGS.

    Args:
        query: Search query string
        region: Region for search (e.g., us-en, uk-en, ru-ru)
        safesearch: Safe search setting (on, moderate, off)
        timelimit: Time limit (d, w, m, y) or custom date range
        max_results: Maximum number of results to return
        page: Page number of results
        backend: Search backend (auto, or specific engine)
    Returns:
        List of search results with title, href, and body

    """
    results = await asyncio.to_thread(
        lambda: DDGS(proxy=_expand_proxy_tb_alias(os.environ.get("DDGS_PROXY"))).text(
            query=query,
            region=region,
            safesearch=safesearch,
            timelimit=timelimit,
            max_results=max_results,
            page=page,
            backend=backend,
        )
    )
    return list(results)


@tool(
    name="search_images",
    description="Perform an image search using DDGS.",
    schema={
        "type": "object",
        "properties": {
            "query": {"type": "string", "description": "Image search query string"},
            "region": {"type": "string", "description": "Region for search (e.g., us-en, uk-en, ru-ru)", "default": "us-en"},
            "safesearch": {"type": "string", "description": "Safe search setting (on, moderate, off)", "default": "off"},
            "timelimit": {"type": "string", "description": "Time limit (d, w, m, y) or custom date range", "nullable": True},
            "max_results": {"type": "integer", "description": "Maximum number of results to return", "default": 10},
            "page": {"type": "integer", "description": "Page number of results", "default": 1},
            "backend": {"type": "string", "description": "Search backend (auto, or specific engine)", "default": "auto"},
            "size": {"type": "string", "description": "Image size (Small, Medium, Large, Wallpaper)", "nullable": True},
            "color": {"type": "string", "description": "Image color filter", "nullable": True},
            "type_image": {"type": "string", "description": "Image type (photo, clipart, gif, transparent, line)", "nullable": True},
            "layout": {"type": "string", "description": "Image layout (Square, Tall, Wide)", "nullable": True},
            "license_image": {"type": "string", "description": "Image license filter", "nullable": True},
        },
        "required": ["query"],
    },
)
async def search_images(
    query: str,
    region: str = "us-en",
    safesearch: str = "off",
    timelimit: str | None = None,
    max_results: int = 10,
    page: int = 1,
    backend: str = "auto",
    size: str | None = None,
    color: str | None = None,
    type_image: str | None = None,
    layout: str | None = None,
    license_image: str | None = None,
) -> list[dict[str, Any]]:
    """Perform an image search using DDGS.

    Args:
        query: Image search query string
        region: Region for search (e.g., us-en, uk-en, ru-ru)
        safesearch: Safe search setting (on, moderate, off)
        timelimit: Time limit (d, w, m, y) or custom date range
        max_results: Maximum number of results to return
        page: Page number of results
        backend: Search backend (auto, or specific engine)
        size: Image size (Small, Medium, Large, Wallpaper)
        color: Image color filter
        type_image: Image type (photo, clipart, gif, transparent, line)
        layout: Image layout (Square, Tall, Wide)
        license_image: Image license filter

    Returns:
        List of image search results with title, image URL, and source

    """
    results = await asyncio.to_thread(
        lambda: DDGS(proxy=_expand_proxy_tb_alias(os.environ.get("DDGS_PROXY"))).images(
            query=query,
            region=region,
            safesearch=safesearch,
            timelimit=timelimit,
            max_results=max_results,
            page=page,
            backend=backend,
            size=size,
            color=color,
            type_image=type_image,
            layout=layout,
            license_image=license_image,
        )
    )
    return list(results)


@tool(
    name="search_news",
    description="Perform a news search using DDGS.",
    schema={
        "type": "object",
        "properties": {
            "query": {"type": "string", "description": "News search query string"},
            "region": {"type": "string", "description": "Region for search (e.g., us-en, uk-en, ru-ru)", "default": "us-en"},
            "safesearch": {"type": "string", "description": "Safe search setting (on, moderate, off)", "default": "off"},
            "timelimit": {"type": "string", "description": "Time limit (d, w, m, y) or custom date range", "nullable": True},
            "max_results": {"type": "integer", "description": "Maximum number of results to return", "default": 10},
            "page": {"type": "integer", "description": "Page number of results", "default": 1},
            "backend": {"type": "string", "description": "Search backend (auto, or specific engine)", "default": "auto"},
        },
        "required": ["query"],
    },
)
async def search_news(
    query: str,
    region: str = "us-en",
    safesearch: str = "off",
    timelimit: str | None = None,
    max_results: int = 10,
    page: int = 1,
    backend: str = "auto",
) -> list[dict[str, Any]]:
    """Perform a news search using DDGS.

    Args:
        query: News search query string
        region: Region for search (e.g., us-en, uk-en, ru-ru)
        safesearch: Safe search setting (on, moderate, off)
        timelimit: Time limit (d, w, m, y) or custom date range
        max_results: Maximum number of results to return
        page: Page number of results
        backend: Search backend (auto, or specific engine)
    Returns:
        List of news results with title, URL, source, and date

    """
    results = await asyncio.to_thread(
        lambda: DDGS(proxy=_expand_proxy_tb_alias(os.environ.get("DDGS_PROXY"))).news(
            query=query,
            region=region,
            safesearch=safesearch,
            timelimit=timelimit,
            max_results=max_results,
            page=page,
            backend=backend,
        )
    )
    return list(results)


@tool(
    name="search_videos",
    description="Perform a video search using DDGS.",
    schema={
        "type": "object",
        "properties": {
            "query": {"type": "string", "description": "Video search query string"},
            "region": {"type": "string", "description": "Region for search (e.g., us-en, uk-en, ru-ru)", "default": "us-en"},
            "safesearch": {"type": "string", "description": "Safe search setting (on, moderate, off)", "default": "off"},
            "timelimit": {"type": "string", "description": "Time limit (d, w, m) or custom date range", "nullable": True},
            "max_results": {"type": "integer", "description": "Maximum number of results to return", "default": 10},
            "page": {"type": "integer", "description": "Page number of results", "default": 1},
            "backend": {"type": "string", "description": "Search backend (auto, or specific engine)", "default": "auto"},
            "resolution": {"type": "string", "description": "Video resolution (high, standard)", "nullable": True},
            "duration": {"type": "string", "description": "Video duration (short, medium, long)", "nullable": True},
            "license_videos": {"type": "string", "description": "Video license (creativeCommon, youtube)", "nullable": True},
        },
        "required": ["query"],
    },
)
async def search_videos(
    query: str,
    region: str = "us-en",
    safesearch: str = "off",
    timelimit: str | None = None,
    max_results: int = 10,
    page: int = 1,
    backend: str = "auto",
    resolution: str | None = None,
    duration: str | None = None,
    license_videos: str | None = None,
) -> list[dict[str, Any]]:
    """Perform a video search using DDGS.

    Args:
        query: Video search query string
        region: Region for search (e.g., us-en, uk-en, ru-ru)
        safesearch: Safe search setting (on, moderate, off)
        timelimit: Time limit (d, w, m) or custom date range
        max_results: Maximum number of results to return
        page: Page number of results
        backend: Search backend (auto, or specific engine)
        resolution: Video resolution (high, standard)
        duration: Video duration (short, medium, long)
        license_videos: Video license (creativeCommon, youtube)

    Returns:
        List of video search results with title, URL, and metadata

    """
    results = await asyncio.to_thread(
        lambda: DDGS(proxy=_expand_proxy_tb_alias(os.environ.get("DDGS_PROXY"))).videos(
            query=query,
            region=region,
            safesearch=safesearch,
            timelimit=timelimit,
            max_results=max_results,
            page=page,
            backend=backend,
            resolution=resolution,
            duration=duration,
            license_videos=license_videos,
        )
    )
    return list(results)


@tool(
    name="search_books",
    description="Perform a book search using DDGS.",
    schema={
        "type": "object",
        "properties": {
            "query": {"type": "string", "description": "Books search query string"},
            "max_results": {"type": "integer", "description": "Maximum number of results to return", "default": 10},
            "page": {"type": "integer", "description": "Page number of results", "default": 1},
            "backend": {"type": "string", "description": "Search backend (auto, or specific engine)", "default": "auto"},
        },
        "required": ["query"],
    },
)
async def search_books(
    query: str,
    max_results: int = 10,
    page: int = 1,
    backend: str = "auto",
) -> list[dict[str, Any]]:
    """Perform a book search using DDGS.
    Args:
        query: Books search query string
        max_results: Maximum number of results to return
        page: Page number of results
        backend: Search backend (auto, or specific engine)
    Returns:
        List of book search results with title, author, and metadata
    """
    results = await asyncio.to_thread(
        lambda: DDGS(proxy=_expand_proxy_tb_alias(os.environ.get("DDGS_PROXY"))).books(
            query=query,
            max_results=max_results,
            page=page,
            backend=backend,
        )
    )
    return list(results)

@tool(
    name="extract_content",
    description="Extract content from a URL.",
    schema={
        "type": "object",
        "properties": {
            "url": {"type": "string", "description": "The URL to fetch and extract content from."},
            "fmt": {"type": "string", "description": "Output format: \"text_markdown\", \"text_plain\", \"text_rich\", \"text\" (raw HTML), \"content\" (raw bytes).", "default": "text_markdown"},
        },
        "required": ["url"],
    },
)
async def extract_content(
    url: str,
    fmt: str = "text_markdown",
) -> dict[str, str | bytes]:
    """Extract content from a URL.

    Args:
        url: The URL to fetch and extract content from.
        fmt: Output format: "text_markdown", "text_plain", "text_rich", "text" (raw HTML), "content" (raw bytes).

    Returns:
        Dictionary with url and content keys.
    """
    return await asyncio.to_thread(
        lambda: DDGS(proxy=_expand_proxy_tb_alias(os.environ.get("DDGS_PROXY"))).extract(
            url=url,
            fmt=fmt,
        )
    )
