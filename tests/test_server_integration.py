import pytest
from fastapi.testclient import TestClient
from server import app, mcp, add, subtract, get_todo_tool, ServerManager
import threading
import time
import socket
import os
import signal
import sys

# Importa requests solo se necessario
try:
    import requests
except ImportError:
    pytest.skip("Il modulo requests non è installato", allow_module_level=True)

client = TestClient(app)

def test_fastapi_endpoints():
    """Test degli endpoint FastAPI"""
    # Test /tools endpoint
    response = client.get("/tools")
    assert response.status_code == 200
    tools = response.json()
    assert len(tools) > 0
    assert all("name" in tool for tool in tools)
    assert all("description" in tool for tool in tools)
    assert all("parameters" in tool for tool in tools)
    assert all("returns" in tool for tool in tools)

    # Test /todo endpoint
    response = client.get("/todo/1")
    assert response.status_code == 200
    assert response.json() == {"id": 1, "task": "Task 1"}

def test_mcp_tools():
    """Test dei tool MCP"""
    # Test add tool
    result = add(2, 3)
    assert result == 5

    # Test subtract tool
    result = subtract(5, 3)
    assert result == 2

@pytest.mark.asyncio
async def test_get_todo_tool():
    """Test del tool get_todo_tool"""
    result = await get_todo_tool(1)
    assert result == {"id": 1, "task": "Task 1"}

def is_port_in_use(port):
    """Verifica se una porta è in uso"""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(('localhost', port)) == 0

def kill_process_on_port(port):
    """Termina il processo che sta usando una porta"""
    try:
        # Trova il PID del processo che usa la porta
        if sys.platform == 'darwin':  # macOS
            pid = int(os.popen(f'lsof -ti:{port}').read().strip())
        else:  # Linux/Unix
            pid = int(os.popen(f'fuser {port}/tcp').read().strip())
        # Termina il processo
        os.kill(pid, signal.SIGTERM)
        # Attendi che il processo termini
        time.sleep(1)
    except:
        pass

# TODO: questo test non funziona - Diabilitato perchè per interrompere il server si deve usare CTRL+C
def _test_server_ports():
    """Test che verifica che le porte siano disponibili"""
    print("\nInizio test_server_ports")
    
    # Pulisci eventuali processi in esecuzione sulle porte
    print("Killing processes on ports 8001 and 8000")
    kill_process_on_port(8001)
    kill_process_on_port(8000)
    
    # Attendi che le porte siano libere
    print("Attendo 1 secondo per le porte libere")
    time.sleep(1)
    
    # Verifica che le porte non siano già in uso
    print("Verifico che le porte siano libere")
    if is_port_in_use(8001):
        pytest.skip("La porta 8001 è ancora in uso dopo il tentativo di pulizia")
    if is_port_in_use(8000):
        pytest.skip("La porta 8000 è ancora in uso dopo il tentativo di pulizia")

    # Crea un'istanza di ServerManager
    print("Avvio i server")
    server_manager = ServerManager()
    
    # Avvia i server in thread separati
    fastapi_thread = threading.Thread(target=server_manager.run_fastapi)
    fastapi_thread.daemon = True
    fastapi_thread.start()

    mcp_thread = threading.Thread(target=server_manager.run_mcp)
    mcp_thread.daemon = True
    mcp_thread.start()

    # Attendi che i server siano avviati
    print("Attendo 1 secondo per l'avvio dei server")
    time.sleep(1)

    try:
        print("Verifico che le porte siano in uso")
        # Verifica che le porte siano ora in uso
        assert is_port_in_use(8001), "FastAPI non è in ascolto sulla porta 8001"
        assert is_port_in_use(8000), "MCP non è in ascolto sulla porta 8000"

        print("Verifico endpoint FastAPI")
        # Verifica FastAPI
        response = requests.get("http://localhost:8001/tools")
        assert response.status_code == 200

        print("Verifico endpoint MCP")
        # Verifica MCP (dovrebbe essere in ascolto sulla porta 8000)
        response = requests.get("http://localhost:8000/sse")
        assert response.status_code == 200  # L'endpoint SSE dovrebbe essere disponibile
    except Exception as e:
        print(f"Errore durante il test: {str(e)}")
        raise
    finally:
        print("Inizio fase di terminazione")
        # Imposta il flag di terminazione
        server_manager.should_exit = True
        
        # Chiudi esplicitamente i server
        if server_manager.fastapi_server:
            server_manager.fastapi_server.should_exit = True
        if server_manager.mcp_server:
            server_manager.mcp_server.should_exit = True
        
        # Attendi che i thread terminino
        print("Attendo terminazione thread FastAPI")
        if fastapi_thread.is_alive():
            fastapi_thread.join(timeout=1.0)
            
        print("Attendo terminazione thread MCP")
        if mcp_thread.is_alive():
            mcp_thread.join(timeout=1.0)
            
        # Pulisci le porte
        print("Pulisco le porte")
        kill_process_on_port(8001)
        kill_process_on_port(8000)
        
        # Attendi un momento per assicurarsi che tutto sia terminato
        print("Attendo 0.5 secondi per la terminazione finale")
        time.sleep(0.5)
        
        print("Fine test_server_ports") 