# server.py
from fastapi import FastAPI
from mcp.server.fastmcp import FastMCP
from typing import List, Dict, Any
import inspect
import uvicorn
import asyncio
from fastapi.middleware.cors import CORSMiddleware
import threading
import anyio
import signal
import sys
import os
import time

# Create an MCP server
mcp = FastMCP("Demo")

# FastAPI app
app = FastAPI()

# Configura CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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

@app.get("/todo/{item_id}")
async def get_todo(item_id: int):
    return {"id": item_id, "task": f"Task {item_id}"}

@mcp.tool()
async def get_todo_tool(item_id: int):
    return await get_todo(item_id)

@app.get("/tools", response_model=List[Dict[str, Any]])
async def list_tools():
    """Endpoint per elencare tutti i tool disponibili"""
    tools = []
    # Ottieni tutti i tool registrati
    registered_tools = {
        "add": add,
        "subtract": subtract,
        "get_todo_tool": get_todo_tool
    }
    
    for name, func in registered_tools.items():
        tool_data = {
            "name": name,
            "description": func.__doc__ or "",
            "parameters": {
                param_name: str(param.annotation)
                for param_name, param in inspect.signature(func).parameters.items()
            },
            "returns": str(inspect.signature(func).return_annotation)
        }
        tools.append(tool_data)
    return tools

class ServerManager:
    def __init__(self):
        self.should_exit = False
        self.fastapi_server = None
        self.mcp_server = None
        self.fastapi_thread = None
        self.mcp_thread = None
        self.is_test = any('pytest' in arg for arg in sys.argv)

    def run_fastapi(self):
        """Avvia il server FastAPI"""
        config = uvicorn.Config(app, host="0.0.0.0", port=8001)
        self.fastapi_server = uvicorn.Server(config)
        asyncio.run(self.fastapi_server.serve())

    def run_mcp(self):
        """Avvia il server MCP"""
        try:
            self.mcp_server = mcp.run(transport="sse")
        except KeyboardInterrupt:
            print("\nTerminazione del server MCP...")
            self.should_exit = True

    def shutdown(self):
        """Chiude entrambi i server"""
        print("\nTerminazione dei server...")
        
        # Imposta il flag di terminazione
        self.should_exit = True
        
        # Chiudi il server FastAPI
        if self.fastapi_server:
            self.fastapi_server.should_exit = True
            if self.fastapi_thread and self.fastapi_thread.is_alive():
                self.fastapi_thread.join(timeout=1.0)
        
        # Chiudi il server MCP
        if self.mcp_server:
            if self.mcp_thread and self.mcp_thread.is_alive():
                self.mcp_thread.join(timeout=1.0)
        
        # Se siamo in un test, non forziamo la terminazione
        if self.is_test:
            return
        
        # Altrimenti, forza la terminazione solo se necessario
        if any(t.is_alive() for t in [self.fastapi_thread, self.mcp_thread] if t):
            print("Forzando la terminazione...")
            os._exit(0)
        else:
            sys.exit(0)

def signal_handler(signum, frame):
    """Gestisce i segnali di terminazione"""
    server_manager.shutdown()

# Run both servers
if __name__ == "__main__":
    print("Starting both FastAPI and MCP servers...")
    
    server_manager = ServerManager()
    
    # Registra il gestore di segnali
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    # Avvia FastAPI in un thread separato
    server_manager.fastapi_thread = threading.Thread(target=server_manager.run_fastapi)
    server_manager.fastapi_thread.daemon = True
    server_manager.fastapi_thread.start()
    
    # Avvia MCP in un thread separato
    server_manager.mcp_thread = threading.Thread(target=server_manager.run_mcp)
    server_manager.mcp_thread.daemon = True
    server_manager.mcp_thread.start()
    
    try:
        # Mantieni il thread principale attivo
        while not server_manager.should_exit:
            time.sleep(0.1)
    except KeyboardInterrupt:
        server_manager.shutdown()


