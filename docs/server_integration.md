# Integrazione FastAPI con MCP Server

Questo documento descrive l'integrazione tra il server FastAPI e il server MCP.

## Configurazione

- FastAPI server: porta 8001
- MCP server: porta 8000

## Endpoint FastAPI

### GET /tools
Elenca tutti i tool disponibili.

**Risposta:**
```json
[
  {
    "name": "add",
    "description": "Add two numbers",
    "parameters": {
      "a": "int",
      "b": "int"
    },
    "returns": "int"
  },
  {
    "name": "subtract",
    "description": "Subtract two numbers",
    "parameters": {
      "a": "int",
      "b": "int"
    },
    "returns": "int"
  },
  {
    "name": "get_todo_tool",
    "description": "",
    "parameters": {
      "item_id": "int"
    },
    "returns": "dict"
  }
]
```

### GET /todo/{item_id}
Restituisce un task TODO specifico.

**Parametri:**
- `item_id`: ID del task (intero)

**Risposta:**
```json
{
  "id": 1,
  "task": "Task 1"
}
```

## Tool MCP

### add
Somma due numeri interi.

**Parametri:**
- `a`: Primo numero
- `b`: Secondo numero

**Ritorno:**
- Somma dei due numeri

### subtract
Sottrae due numeri interi.

**Parametri:**
- `a`: Primo numero
- `b`: Secondo numero

**Ritorno:**
- Differenza tra i due numeri

### get_todo_tool
Recupera un task TODO specifico.

**Parametri:**
- `item_id`: ID del task (intero)

**Ritorno:**
- Dizionario contenente l'ID e il task

## Avvio dei Server

Per avviare entrambi i server:

```bash
python server.py
```

I server verranno avviati in thread separati:
- FastAPI sulla porta 8001
- MCP sulla porta 8000

## Note Tecniche

- I server vengono eseguiti in thread separati per permettere l'esecuzione concorrente
- È configurato CORS per permettere richieste da qualsiasi origine
- La terminazione dei server richiede l'uso di CTRL+C
- Il test di integrazione `test_server_ports` è attualmente disabilitato a causa di problemi con la terminazione automatica dei server 