
from base import tool

@tool(
    name="web_search_brave",
    description="Perform a web search using the Brave Search API. Supports all official Brave Web Search parameters.",
    schema={
        "type": "object",
        "properties": {
            "query": {"type": "string", "description": "The search query to send to Brave (required)"},
            "country": {"type": "string", "description": "Country code (ISO 3166-1 alpha-2)", "default": "US"},
            "search_lang": {"type": "string", "description": "Language for search results (ISO 639-1)", "default": "en"},
            "ui_lang": {
                "type": "string",
                "description": "UI locale - must be one of: en-US, en-GB, fr-FR, de-DE, etc.",
                "default": "en-US"
            },
            "count": {
                "type": "integer",
                "description": "Number of results to return (1-20)",
                "default": 10,
                "minimum": 1,
                "maximum": 20,
            },
            "offset": {"type": "integer", "description": "Zero-based offset", "default": 0, "minimum": 0},
            "safesearch": {
                "type": "string",
                "description": "Safe search level",
                "enum": ["off", "moderate", "strict"],
                "default": "off",
            },
            "freshness": {"type": "string", "description": "pd, pw, pm, py, or YYYY-MM-DD..YYYY-MM-DD"},
            "text_decorations": {"type": "boolean", "description": "Include text decorations", "default": True},
            "spellcheck": {"type": "boolean", "description": "Enable spell checking", "default": True},
            "result_filter": {"type": "string", "description": "Comma-separated result types (web,news,videos,...)"},
            "goggles_id": {"type": "string", "description": "Custom Brave Goggles ID"},
            "units": {"type": "string", "enum": ["metric", "imperial"]},
            "extra_snippets": {"type": "boolean", "default": False},
        },
        "required": ["query"],
    },
)
def web_search_brave(
    query: str,
    country: str = "US",
    search_lang: str = "en",
    ui_lang: str = "en-US",
    count: int = 10,
    offset: int = 0,
    safesearch: str = "off",
    freshness: str = None,
    text_decorations: bool = True,
    spellcheck: bool = True,
    result_filter: str = None,
    goggles_id: str = None,
    units: str = None,
    extra_snippets: bool = False,
) -> str:
    """
    Brave Web Search tool for diaMCP.
    """
    import os
    import requests

    api_key = os.getenv("BRAVE_API_KEY") or os.getenv("BRAVE_SEARCH_API_KEY")
    if not api_key:
        return "Error: BRAVE_API_KEY or BRAVE_SEARCH_API_KEY environment variable is not set."

    url = "https://api.search.brave.com/res/v1/web/search"

    headers = {
        "X-Subscription-Token": api_key,
        "Accept": "application/json",
        "User-Agent": "diaMCP-Tool/1.0",
    }

    params = {
        "q": query,
        "country": country,
        "search_lang": search_lang,
        "ui_lang": ui_lang,
        "count": count,
        "offset": offset,
        "safesearch": safesearch,
        "text_decorations": str(text_decorations).lower(),
        "spellcheck": str(spellcheck).lower(),
    }

    if freshness:
        params["freshness"] = freshness
    if result_filter:
        params["result_filter"] = result_filter
    if goggles_id:
        params["goggles_id"] = goggles_id
    if units:
        params["units"] = units
    if extra_snippets:
        params["extra_snippets"] = "true"

    try:
        resp = requests.get(url, headers=headers, params=params, timeout=20)
        resp.raise_for_status()
        data = resp.json()

        output = f"# Brave Search Results for: **{query}**\n\n"

        categories = [
            ("web", "Web Results"),
            ("news", "News Results"),
            ("videos", "Video Results"),
            ("images", "Image Results"),
            ("discussions", "Discussion Results"),
        ]

        has_results = False
        for key, title in categories:
            if key in data and "results" in data.get(key, {}) and data[key].get("results"):
                has_results = True
                output += f"## {title}\n\n"
                for i, r in enumerate(data[key]["results"], 1):
                    title_text = r.get("title", "Untitled")
                    url_link = r.get("url") or r.get("link", "")
                    desc = r.get("description") or r.get("snippet", "No description")
                    source = r.get("source", {}).get("name", "")

                    output += f"**{i}. {title_text}**\n"
                    if url_link:
                        output += f"**URL:** {url_link}\n"
                    if source:
                        output += f"**Source:** {source}\n"
                    output += f"{desc}\n\n"
                    output += "---\n\n"

        if not has_results:
            output += "No results found.\n"

        return output.strip()

    except requests.exceptions.HTTPError as e:
        error_body = e.response.text if hasattr(e.response, 'text') else str(e)
        if e.response.status_code == 401:
            return "Error: Invalid Brave API key."
        if e.response.status_code == 422:
            return f"Brave API Error (422):\n{error_body}"
        return f"HTTP Error {e.response.status_code}: {error_body}"
    except Exception as e:
        return f"Unexpected error: {str(e)}"
