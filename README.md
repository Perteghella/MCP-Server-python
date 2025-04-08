# MCP Server Demo in python

This repository contains a simple implementation of a Model Communication Protocol (MCP) server using Python. The server is designed to demonstrate the basic functionality of an MCP server and can be used for testing and development purposes.

The server uses `uvicorn` by default, running on port `8000`. To expose the server over the network, use the `sse` transport.

---

## Setup Instructions

### 1. Create and Activate a Virtual Environment
Run the following commands to set up your Python environment:
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

---

## Starting the Server

To start the server, run:
```bash
python3 server.py
```

### Verify the Server is Running
You can verify that the server is running on port `8000` using the following commands:

- Check active connections:
  ```bash
  netstat -n | grep 8000
  ```

- Check processes using the port:
  ```bash
  lsof -i :8000
  ```

- Test the server with `curl`:
  ```bash
  curl http://0.0.0.0:8000/sse
  ```

---

## Tools Using the Server

To integrate this server with tools like Cursor or Claude, use the following `mcp.json` configuration file:

```json
{
  "mcpServers": {
    "demo-server": {
      "transport": "sse",
      "url": "http://localhost:8000/sse"
    }
  }
}
```

---

## Notes

- By default, the server uses `stdio` transport. To expose it over the network, ensure you configure it to use `sse` transport.
- The server runs on `localhost` and listens on port `8000` using uvicorn.

Feel free to contribute or open issues if you encounter any problems!
