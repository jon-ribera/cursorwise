"""Cursorwise MCP server -- 50 tools for full Flowise API coverage."""

import json
import logging
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from dataclasses import dataclass
from mcp.server.fastmcp import Context, FastMCP

from cursorwise.client import FlowiseClient
from cursorwise.config import Settings

logger = logging.getLogger("cursorwise.server")


@dataclass
class AppContext:
    client: FlowiseClient


@asynccontextmanager
async def app_lifespan(server: FastMCP) -> AsyncIterator[AppContext]:
    settings = Settings.from_env()
    logging.basicConfig(level=getattr(logging, settings.log_level, logging.WARNING))
    client = FlowiseClient(settings)
    logger.info("Cursorwise connected to %s", settings.api_endpoint)
    try:
        yield AppContext(client=client)
    finally:
        await client.close()
        logger.info("Cursorwise client closed.")


mcp = FastMCP("Cursorwise", lifespan=app_lifespan)


def _j(obj: object) -> str:
    return json.dumps(obj, default=str)


def _c(ctx: Context) -> FlowiseClient:
    return ctx.request_context.lifespan_context.client


# === SYSTEM ===

@mcp.tool()
async def ping(ctx: Context) -> str:
    """Health-check the Flowise instance."""
    return _j(await _c(ctx).ping())


@mcp.tool()
async def list_nodes(ctx: Context) -> str:
    """List all available node types in Flowise."""
    data = await _c(ctx).list_nodes()
    if isinstance(data, list):
        s = [{"name": n.get("name"), "category": n.get("category"), "label": n.get("label")} for n in data]
        return _j(s)
    return _j(data)


@mcp.tool()
async def get_node(name: str, ctx: Context = None) -> str:
    """Get full schema for a specific Flowise node by name."""
    return _j(await _c(ctx).get_node(name))


# === CHATFLOWS ===

@mcp.tool()
async def list_chatflows(ctx: Context) -> str:
    """List all chatflows."""
    data = await _c(ctx).list_chatflows()
    if isinstance(data, list):
        s = [{"id": c.get("id"), "name": c.get("name"), "type": c.get("type")} for c in data]
        return _j(s)
    return _j(data)


@mcp.tool()
async def get_chatflow(chatflow_id: str, ctx: Context = None) -> str:
    """Get full details of a chatflow by ID."""
    return _j(await _c(ctx).get_chatflow(chatflow_id))


@mcp.tool()
async def get_chatflow_by_apikey(apikey: str, ctx: Context = None) -> str:
    """Look up a chatflow by its API key."""
    return _j(await _c(ctx).get_chatflow_by_apikey(apikey))


@mcp.tool()
async def create_chatflow(name: str, flow_data: str = "{}", description: str = "", chatflow_type: str = "CHATFLOW", ctx: Context = None) -> str:
    """Create a new chatflow. flow_data is a JSON string."""
    return _j(await _c(ctx).create_chatflow(name, flow_data, description, chatflow_type))


@mcp.tool()
async def update_chatflow(chatflow_id: str, name: str = None, flow_data: str = None, description: str = None, deployed: bool = None, is_public: bool = None, chatbot_config: str = None, category: str = None, ctx: Context = None) -> str:
    """Update a chatflow. Only pass fields to change."""
    return _j(await _c(ctx).update_chatflow(chatflow_id, name, flow_data, description, deployed, is_public, chatbot_config, category))


@mcp.tool()
async def delete_chatflow(chatflow_id: str, ctx: Context = None) -> str:
    """Delete a chatflow by ID."""
    return _j(await _c(ctx).delete_chatflow(chatflow_id))


# === PREDICTION ===

@mcp.tool()
async def create_prediction(chatflow_id: str, question: str, override_config: str = None, history: str = None, streaming: bool = False, ctx: Context = None) -> str:
    """Send a message to a chatflow and get an AI response."""
    return _j(await _c(ctx).create_prediction(chatflow_id, question, override_config, history, streaming))


# === ASSISTANTS ===

@mcp.tool()
async def list_assistants(ctx: Context) -> str:
    """List all assistants."""
    return _j(await _c(ctx).list_assistants())


@mcp.tool()
async def get_assistant(assistant_id: str, ctx: Context = None) -> str:
    """Get details of an assistant by ID."""
    return _j(await _c(ctx).get_assistant(assistant_id))


@mcp.tool()
async def create_assistant(name: str, description: str = "", model: str = "gpt-4", instructions: str = "", credential: str = None, ctx: Context = None) -> str:
    """Create a new OpenAI assistant in Flowise."""
    return _j(await _c(ctx).create_assistant(name, description, model, instructions, credential))


@mcp.tool()
async def update_assistant(assistant_id: str, details: str = None, credential: str = None, ctx: Context = None) -> str:
    """Update an assistant. details is a JSON string."""
    return _j(await _c(ctx).update_assistant(assistant_id, details, credential))


@mcp.tool()
async def delete_assistant(assistant_id: str, ctx: Context = None) -> str:
    """Delete an assistant by ID."""
    return _j(await _c(ctx).delete_assistant(assistant_id))


# === TOOLS ===

@mcp.tool()
async def list_tools(ctx: Context) -> str:
    """List all custom tools in Flowise."""
    return _j(await _c(ctx).list_tools())


@mcp.tool()
async def get_tool(tool_id: str, ctx: Context = None) -> str:
    """Get a custom tool by ID."""
    return _j(await _c(ctx).get_tool(tool_id))


@mcp.tool()
async def create_tool(name: str, description: str, schema: str = None, func: str = None, color: str = "#4CAF50", ctx: Context = None) -> str:
    """Create a new custom tool in Flowise. Color defaults to green (#4CAF50)."""
    return _j(await _c(ctx).create_tool(name, description, schema, func, color))


@mcp.tool()
async def update_tool(tool_id: str, name: str = None, description: str = None, schema: str = None, func: str = None, ctx: Context = None) -> str:
    """Update a custom tool by ID."""
    return _j(await _c(ctx).update_tool(tool_id, name, description, schema, func))


@mcp.tool()
async def delete_tool(tool_id: str, ctx: Context = None) -> str:
    """Delete a custom tool by ID."""
    return _j(await _c(ctx).delete_tool(tool_id))


# === VARIABLES ===

@mcp.tool()
async def list_variables(ctx: Context) -> str:
    """List all Flowise variables."""
    return _j(await _c(ctx).list_variables())


@mcp.tool()
async def create_variable(name: str, value: str = "", var_type: str = "string", ctx: Context = None) -> str:
    """Create a new variable."""
    return _j(await _c(ctx).create_variable(name, value, var_type))


@mcp.tool()
async def update_variable(var_id: str, name: str = None, value: str = None, var_type: str = None, ctx: Context = None) -> str:
    """Update a variable by ID."""
    return _j(await _c(ctx).update_variable(var_id, name, value, var_type))


@mcp.tool()
async def delete_variable(var_id: str, ctx: Context = None) -> str:
    """Delete a variable by ID."""
    return _j(await _c(ctx).delete_variable(var_id))


# === DOCUMENT STORE ===

@mcp.tool()
async def list_document_stores(ctx: Context) -> str:
    """List all document stores."""
    return _j(await _c(ctx).list_document_stores())


@mcp.tool()
async def get_document_store(store_id: str, ctx: Context = None) -> str:
    """Get details of a document store by ID."""
    return _j(await _c(ctx).get_document_store(store_id))


@mcp.tool()
async def create_document_store(name: str, description: str = "", ctx: Context = None) -> str:
    """Create a new document store."""
    return _j(await _c(ctx).create_document_store(name, description))


@mcp.tool()
async def update_document_store(store_id: str, name: str = None, description: str = None, ctx: Context = None) -> str:
    """Update a document store by ID."""
    return _j(await _c(ctx).update_document_store(store_id, name, description))


@mcp.tool()
async def delete_document_store(store_id: str, ctx: Context = None) -> str:
    """Delete a document store by ID."""
    return _j(await _c(ctx).delete_document_store(store_id))


# === DOCUMENT CHUNKS ===

@mcp.tool()
async def get_document_chunks(store_id: str, loader_id: str, page_no: int = 1, ctx: Context = None) -> str:
    """Get chunks from a document loader within a store."""
    return _j(await _c(ctx).get_document_chunks(store_id, loader_id, page_no))


@mcp.tool()
async def update_document_chunk(store_id: str, loader_id: str, chunk_id: str, page_content: str = None, metadata: str = None, ctx: Context = None) -> str:
    """Update a specific chunk. metadata is a JSON string."""
    return _j(await _c(ctx).update_document_chunk(store_id, loader_id, chunk_id, page_content, metadata))


@mcp.tool()
async def delete_document_chunk(store_id: str, loader_id: str, chunk_id: str, ctx: Context = None) -> str:
    """Delete a specific chunk."""
    return _j(await _c(ctx).delete_document_chunk(store_id, loader_id, chunk_id))


# === DOCUMENT OPS ===

@mcp.tool()
async def upsert_document(store_id: str, loader: str = None, splitter: str = None, embedding: str = None, vector_store: str = None, record_manager: str = None, metadata: str = None, replace_existing: bool = False, doc_id: str = None, ctx: Context = None) -> str:
    """Upsert a document into a store. Config params are JSON strings."""
    return _j(await _c(ctx).upsert_document(store_id, loader, splitter, embedding, vector_store, record_manager, metadata, replace_existing, doc_id))


@mcp.tool()
async def refresh_document_store(store_id: str, items: str = None, ctx: Context = None) -> str:
    """Re-process and upsert all documents in a store."""
    return _j(await _c(ctx).refresh_document_store(store_id, items))


@mcp.tool()
async def query_document_store(store_id: str, query: str, ctx: Context = None) -> str:
    """Run a retrieval query against a document store vector index."""
    return _j(await _c(ctx).query_document_store(store_id, query))


@mcp.tool()
async def delete_document_loader(store_id: str, loader_id: str, ctx: Context = None) -> str:
    """Delete a document loader and its chunks from a store."""
    return _j(await _c(ctx).delete_document_loader(store_id, loader_id))


@mcp.tool()
async def delete_vectorstore_data(store_id: str, ctx: Context = None) -> str:
    """Delete vector store data from a document store."""
    return _j(await _c(ctx).delete_vectorstore_data(store_id))


# === CHAT MESSAGES ===

@mcp.tool()
async def list_chat_messages(chatflow_id: str, chat_type: str = None, order: str = None, chat_id: str = None, session_id: str = None, start_date: str = None, end_date: str = None, ctx: Context = None) -> str:
    """List chat messages for a chatflow."""
    return _j(await _c(ctx).list_chat_messages(chatflow_id, chat_type, order, chat_id, session_id, start_date, end_date))


@mcp.tool()
async def delete_chat_messages(chatflow_id: str, chat_id: str = None, chat_type: str = None, session_id: str = None, hard_delete: bool = False, ctx: Context = None) -> str:
    """Delete chat messages for a chatflow."""
    return _j(await _c(ctx).delete_chat_messages(chatflow_id, chat_id, chat_type, session_id, hard_delete))


# === FEEDBACK ===

@mcp.tool()
async def list_feedback(chatflow_id: str, chat_id: str = None, sort_order: str = "asc", ctx: Context = None) -> str:
    """List feedback for a chatflow."""
    return _j(await _c(ctx).list_feedback(chatflow_id, chat_id, sort_order))


@mcp.tool()
async def create_feedback(chatflow_id: str, chat_id: str, message_id: str, rating: str, content: str = "", ctx: Context = None) -> str:
    """Create feedback for a message. rating: THUMBS_UP or THUMBS_DOWN."""
    return _j(await _c(ctx).create_feedback(chatflow_id, chat_id, message_id, rating, content))


@mcp.tool()
async def update_feedback(feedback_id: str, rating: str = None, content: str = None, ctx: Context = None) -> str:
    """Update existing feedback."""
    return _j(await _c(ctx).update_feedback(feedback_id, rating, content))


# === LEADS ===

@mcp.tool()
async def list_leads(chatflow_id: str, ctx: Context = None) -> str:
    """List all leads for a chatflow."""
    return _j(await _c(ctx).list_leads(chatflow_id))


@mcp.tool()
async def create_lead(chatflow_id: str, chat_id: str, name: str = None, email: str = None, phone: str = None, ctx: Context = None) -> str:
    """Create a new lead for a chatflow."""
    return _j(await _c(ctx).create_lead(chatflow_id, chat_id, name, email, phone))


# === VECTOR UPSERT ===

@mcp.tool()
async def upsert_vector(chatflow_id: str, stop_node_id: str = None, override_config: str = None, ctx: Context = None) -> str:
    """Upsert vector embeddings for a chatflow."""
    return _j(await _c(ctx).upsert_vector(chatflow_id, stop_node_id, override_config))


# === UPSERT HISTORY ===

@mcp.tool()
async def list_upsert_history(chatflow_id: str, order: str = "ASC", start_date: str = None, end_date: str = None, ctx: Context = None) -> str:
    """Get upsert history for a chatflow."""
    return _j(await _c(ctx).list_upsert_history(chatflow_id, order, start_date, end_date))


@mcp.tool()
async def delete_upsert_history(chatflow_id: str, ids: str = None, ctx: Context = None) -> str:
    """Soft-delete upsert history records."""
    return _j(await _c(ctx).delete_upsert_history(chatflow_id, ids))


# === CREDENTIALS ===

@mcp.tool()
async def list_credentials(ctx: Context) -> str:
    """List all saved credentials (names and types, values encrypted)."""
    return _j(await _c(ctx).list_credentials())


@mcp.tool()
async def create_credential(name: str, credential_name: str, encrypted_data: str, ctx: Context = None) -> str:
    """Create a new credential."""
    return _j(await _c(ctx).create_credential(name, credential_name, encrypted_data))


# === MARKETPLACE ===

@mcp.tool()
async def list_marketplace_templates(ctx: Context) -> str:
    """List all marketplace templates available for import."""
    data = await _c(ctx).list_marketplace_templates()
    if isinstance(data, list):
        s = [{"name": t.get("name"), "type": t.get("type"), "description": t.get("description", "")[:120]} for t in data]
        return _j(s)
    return _j(data)
