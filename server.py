# server.py
from fastapi import FastAPI
from mcp.server.fastmcp import FastMCP

# Create an MCP server
mcp = FastMCP("Demo")


# Add an addition tool
@mcp.tool()
def add(a: int, b: int) -> int:
    """Add two numbers"""
    return a + b


# Subtract an addition tool
@mcp.tool()
def subtract(a: int, b: int) -> int:
    """Subtract two numbers"""
    return a - b


# Add a dynamic greeting resource
@mcp.resource("greeting://{name}")
def get_greeting(name: str) -> str:
    """Get a personalized greeting"""
    return f"Hello, {name}!"

# FastAPI app

app = FastAPI()

@app.get("/todo/{item_id}")
async def get_todo(item_id: int):
    return {"id": item_id, "task": f"Task {item_id}"}

@mcp.tool()
async def get_todo_tool(item_id: int):
    return await get_todo(item_id)

# Run the server
if __name__ == "__main__":
    print("Starting FastMCP server...")
    mcp.run(transport="sse")


