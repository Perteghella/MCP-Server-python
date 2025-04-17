# Integrazione FastAPI con MCP

## Introduzione
Questo documento descrive l'integrazione di FastAPI con il framework MCP, permettendo di esporre endpoint REST come strumenti AI.

## Configurazione
Per utilizzare FastAPI con MCP, è necessario:
1. Installare la dipendenza FastAPI (`pip install fastapi`)
2. Importare FastAPI nel server (`from fastapi import FastAPI`)

## Esempio di Utilizzo
```python
# Creazione dell'app FastAPI
app = FastAPI()

# Definizione di un endpoint REST
@app.get("/todo/{item_id}")
async def get_todo(item_id: int):
    return {"id": item_id, "task": f"Task {item_id}"}

# Esposizione dell'endpoint come tool MCP
@mcp.tool()
async def get_todo_tool(item_id: int):
    return await get_todo(item_id)
```

## Funzionalità
- Gli endpoint FastAPI possono essere esposti come strumenti AI
- Supporto per operazioni asincrone
- Integrazione trasparente con il sistema di trasporto MCP

## Best Practices
1. Utilizzare tipi di dati appropriati per i parametri
2. Implementare gestione degli errori
3. Documentare gli endpoint con docstring
4. Utilizzare operazioni asincrone quando appropriato 