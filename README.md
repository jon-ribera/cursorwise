# Cursorwise

MCP server for **Cursor IDE <-> Flowise** integration. Provides 50 tools covering the full Flowise REST API surface via the Model Context Protocol.

## Features

- **50 MCP tools** -- chatflows, predictions, assistants, tools, variables, document stores, chunks, feedback, leads, credentials, marketplace, nodes, and more
- **Async httpx** -- non-blocking HTTP client that works cleanly within the MCP asyncio event loop
- **Lifespan-managed client** -- single shared connection across all tool calls
- **Proxy-aware** -- bypasses corporate proxies for local Flowise calls out of the box

## Installation

```bash
# Via uvx (recommended for Cursor MCP)
uvx --from git+https://github.com/jon-ribera/cursorwise.git cursorwise

# Or from source (editable, for development)
git clone https://github.com/jon-ribera/cursorwise.git
cd cursorwise
pip install -e .
```

## Configuration

Set environment variables (or create a `.env` file):

| Variable | Required | Default | Description |
|---|---|---|---|
| `FLOWISE_API_KEY` | Yes | - | Bearer token for Flowise API |
| `FLOWISE_API_ENDPOINT` | No | `http://localhost:3000` | Flowise instance URL |
| `FLOWISE_TIMEOUT` | No | `120` | HTTP timeout in seconds |
| `CURSORWISE_LOG_LEVEL` | No | `WARNING` | Log verbosity (DEBUG, INFO, WARNING, ERROR) |

## Cursor IDE Integration

Add to `.cursor/mcp.json` in your workspace:

```json
{
  "mcpServers": {
    "cursorwise": {
      "command": "uvx",
      "args": ["--from", "git+https://github.com/jon-ribera/cursorwise.git", "cursorwise"],
      "env": {
        "FLOWISE_API_KEY": "your-api-key",
        "FLOWISE_API_ENDPOINT": "http://localhost:3000",
        "PYTHONUNBUFFERED": "1",
        "http_proxy": "",
        "https_proxy": "",
        "HTTP_PROXY": "",
        "HTTPS_PROXY": ""
      }
    }
  }
}
```

> **Note:** If you're behind a corporate proxy and connecting to a local Flowise instance, set the proxy env vars to empty strings as shown above to bypass the proxy for local calls.

## Tool List (50)

| Group | Tools | Count |
|---|---|---|
| System | `ping`, `list_nodes`, `get_node` | 3 |
| Chatflows | `list_chatflows`, `get_chatflow`, `get_chatflow_by_apikey`, `create_chatflow`, `update_chatflow`, `delete_chatflow` | 6 |
| Prediction | `create_prediction` | 1 |
| Assistants | `list_assistants`, `get_assistant`, `create_assistant`, `update_assistant`, `delete_assistant` | 5 |
| Tools | `list_tools`, `get_tool`, `create_tool`, `update_tool`, `delete_tool` | 5 |
| Variables | `list_variables`, `create_variable`, `update_variable`, `delete_variable` | 4 |
| Doc Store | `list_document_stores`, `get_document_store`, `create_document_store`, `update_document_store`, `delete_document_store` | 5 |
| Doc Chunks | `get_document_chunks`, `update_document_chunk`, `delete_document_chunk` | 3 |
| Doc Ops | `upsert_document`, `refresh_document_store`, `query_document_store`, `delete_document_loader`, `delete_vectorstore_data` | 5 |
| Chat Msgs | `list_chat_messages`, `delete_chat_messages` | 2 |
| Feedback | `list_feedback`, `create_feedback`, `update_feedback` | 3 |
| Leads | `list_leads`, `create_lead` | 2 |
| Vector | `upsert_vector` | 1 |
| History | `list_upsert_history`, `delete_upsert_history` | 2 |
| Credentials | `list_credentials`, `create_credential` | 2 |
| Marketplace | `list_marketplace_templates` | 1 |

## Architecture

```
Cursor IDE -> stdio -> Cursorwise MCP Server -> httpx async -> Flowise REST API
```

## License

MIT
