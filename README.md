# FastAPI MCP Server

A minimal FastAPI server exposing MCP tools via SSE transport.

## Setup

```bash
uv sync
```

## Run

```bash
uv run python server.py
```

Server runs at `http://localhost:3000`

## Tools

| Tool | Description |
|------|-------------|
| `hello(name)` | Returns a greeting |
| `add(a, b)` | Adds two numbers |

## Connect from Claude Desktop

Add to `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "hello-world": {
      "url": "http://localhost:3000/mcp/sse"
    }
  }
}
```
# fastapi-mcp-server
