<p align="center">
  <h1 align="center">🧠 Cursorwise</h1>
  <p align="center">
    <strong>MCP server for Cursor IDE ↔ Flowise integration</strong><br>
    50 tools covering the full Flowise REST API via the Model Context Protocol
  </p>
  <p align="center">
    <a href="#-quick-start">Quick Start</a> •
    <a href="#-tools">Tools</a> •
    <a href="#%EF%B8%8F-configuration">Configuration</a> •
    <a href="#-documentation">Docs</a>
  </p>
</p>

---

## ✨ Features

| | Feature | Description |
|---|---|---|
| 🔧 | **50 MCP Tools** | Full CRUD coverage — chatflows, predictions, assistants, tools, variables, document stores, chunks, feedback, leads, credentials, marketplace, and nodes |
| ⚡ | **Async httpx** | Non-blocking HTTP client that runs cleanly inside the MCP asyncio event loop |
| 🔁 | **Lifespan-Managed Client** | Single shared connection across all tool calls — no reconnecting per request |
| 🛡️ | **Proxy-Aware** | Automatically bypasses corporate proxies for local Flowise calls |
| 📋 | **303 Node Reference** | Complete schema reference for every Flowise node ([view](FLOWISE_NODE_REFERENCE.md)) |

---

## 🚀 Quick Start

### 1. Add to Cursor

Create or edit `.cursor/mcp.json` in your workspace:

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

### 2. Restart MCP

Open **Cursor Settings → MCP** and click the refresh icon next to **cursorwise**, or reload the window (`Ctrl+Shift+P` → `Developer: Reload Window`).

### 3. Start using it

Ask the AI agent to interact with Flowise — list chatflows, create tools, query document stores, and more.

> 💡 **Corporate proxy?** Set the proxy env vars to empty strings as shown above to bypass the proxy for local Flowise calls.

---

## 📦 Installation (Alternative)

```bash
# Via uvx (recommended — used by Cursor MCP)
uvx --from git+https://github.com/jon-ribera/cursorwise.git cursorwise

# From source (for development)
git clone https://github.com/jon-ribera/cursorwise.git
cd cursorwise
pip install -e .
```

---

## ⚙️ Configuration

Set via environment variables or a `.env` file:

| Variable | Required | Default | Description |
|---|---|---|---|
| 🔑 `FLOWISE_API_KEY` | ✅ Yes | — | Bearer token for Flowise API |
| 🌐 `FLOWISE_API_ENDPOINT` | No | `http://localhost:3000` | Flowise instance URL |
| ⏱️ `FLOWISE_TIMEOUT` | No | `120` | HTTP timeout in seconds (predictions can be slow) |
| 📝 `CURSORWISE_LOG_LEVEL` | No | `WARNING` | Log verbosity (`DEBUG`, `INFO`, `WARNING`, `ERROR`) |

---

## 🔧 Tools

### Overview (50 tools across 16 groups)

| | Group | Tools | # |
|---|---|---|---|
| 💓 | **System** | `ping` · `list_nodes` · `get_node` | 3 |
| 🔄 | **Chatflows** | `list_chatflows` · `get_chatflow` · `get_chatflow_by_apikey` · `create_chatflow` · `update_chatflow` · `delete_chatflow` | 6 |
| 💬 | **Prediction** | `create_prediction` | 1 |
| 🤖 | **Assistants** | `list_assistants` · `get_assistant` · `create_assistant` · `update_assistant` · `delete_assistant` | 5 |
| 🛠️ | **Tools** | `list_tools` · `get_tool` · `create_tool` · `update_tool` · `delete_tool` | 5 |
| 📊 | **Variables** | `list_variables` · `create_variable` · `update_variable` · `delete_variable` | 4 |
| 🗄️ | **Doc Store** | `list_document_stores` · `get_document_store` · `create_document_store` · `update_document_store` · `delete_document_store` | 5 |
| 📄 | **Doc Chunks** | `get_document_chunks` · `update_document_chunk` · `delete_document_chunk` | 3 |
| ⚙️ | **Doc Ops** | `upsert_document` · `refresh_document_store` · `query_document_store` · `delete_document_loader` · `delete_vectorstore_data` | 5 |
| 📨 | **Chat Messages** | `list_chat_messages` · `delete_chat_messages` | 2 |
| ⭐ | **Feedback** | `list_feedback` · `create_feedback` · `update_feedback` | 3 |
| 👤 | **Leads** | `list_leads` · `create_lead` | 2 |
| 📐 | **Vector** | `upsert_vector` | 1 |
| 📜 | **History** | `list_upsert_history` · `delete_upsert_history` | 2 |
| 🔐 | **Credentials** | `list_credentials` · `create_credential` | 2 |
| 🏪 | **Marketplace** | `list_marketplace_templates` | 1 |

---

## 🏗️ Architecture

```
┌──────────────┐     stdio      ┌─────────────────────┐     httpx async     ┌──────────────┐
│  Cursor IDE  │ ◄────────────► │  Cursorwise MCP     │ ◄────────────────► │  Flowise     │
│  (AI Agent)  │    JSON-RPC    │  server.py (50 tools)│    REST API         │  (port 3000) │
└──────────────┘                │  client.py (httpx)   │                     └──────────────┘
                                │  config.py (env)     │
                                └─────────────────────┘
```

---

## 📚 Documentation

| Document | Description |
|---|---|
| 📘 [Node Schema Reference](FLOWISE_NODE_REFERENCE.md) | Complete schema for all 303 Flowise nodes — inputs, credentials, base classes |
| 📋 [API Tool Audit Report](API_TOOL_AUDIT_REPORT.md) | End-to-end test results for all 50 tools with bug fixes |
| 📄 [.env.example](.env.example) | Environment variable template |

---

## 🧩 Project Structure

```
cursorwise/
├── __init__.py       # Package init
├── __main__.py       # Entry point — launches MCP on stdio
├── config.py         # Settings dataclass from environment variables
├── client.py         # FlowiseClient — async httpx wrapper (52 API methods)
└── server.py         # FastMCP server — 50 @mcp.tool() definitions
```

---

## 📄 License

MIT — [Jon Ribera](mailto:riberajon@gmail.com)
