"""Entry point for cursorwise MCP server."""

from __future__ import annotations


def main() -> None:
    try:
        from dotenv import load_dotenv
        load_dotenv()
    except ImportError:
        pass  # python-dotenv is optional at runtime if env vars are set directly

    from cursorwise.server import mcp
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
