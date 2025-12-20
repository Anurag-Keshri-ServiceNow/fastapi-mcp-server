import logging

from fastapi import FastAPI, Request
from mcp.server.fastmcp import FastMCP
from mcp.server.transport_security import TransportSecuritySettings

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

# Create the MCP server
mcp = FastMCP(
    "Hello World Server",
    transport_security=TransportSecuritySettings(
        enable_dns_rebinding_protection=True,
        # Add your specific gateway or domain here
        allowed_hosts=["localhost:*", "127.0.0.1:*", "fastapi-mcp-server-tp0z.onrender.com"],
        allowed_origins=["http://localhost:*", "https://fastapi-mcp-server-tp0z.onrender.com"],
    )
)

# Create FastAPI app
app = FastAPI(title="Hello World MCP Server")


@app.middleware("http")
async def log_requests(request: Request, call_next):
    """Log incoming requests with payload."""
    body = await request.body()
    logger.info(f"{request.method} {request.url.path}")
    if body:
        logger.info(f"Payload: {body.decode('utf-8', errors='replace')}")
    response = await call_next(request)
    logger.info(f"Response status: {response.status_code}")
    return response


@mcp.tool()
def hello(name: str = "World") -> str:
    """Say hello to someone.

    Args:
        name: The name to greet (default: World)
    """
    return f"Hello, {name}!"


@mcp.tool()
def add(a: int, b: int) -> int:
    """Add two numbers together.

    Args:
        a: First number
        b: Second number
    """
    return a + b


@mcp.resource("greeting://{name}")
def get_greeting(name: str) -> str:
    """Get a personalized greeting resource."""
    return f"Hello, {name}! Welcome to the MCP server."


# Mount the MCP server to the FastAPI app using SSE transport
app.mount("/mcp", mcp.sse_app())


@app.get("/")
async def root():
    """Root endpoint with server info."""
    return {
        "name": "Hello World MCP Server",
        "mcp_endpoint": "/mcp",
        "description": "A simple MCP server with hello world tools",
    }


def main():
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=3000)


if __name__ == "__main__":
    main()
