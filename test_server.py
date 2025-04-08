import pytest
from mcp.server.fastmcp import FastMCP
from server import add, subtract, get_greeting

# Test per la funzione add
def test_add():
    assert add(2, 3) == 5
    assert add(-1, 1) == 0
    assert add(0, 0) == 0
    assert add(100, 200) == 300

# Test per la funzione subtract
def test_subtract():
    assert subtract(5, 3) == 2
    assert subtract(1, 1) == 0
    assert subtract(0, 0) == 0
    assert subtract(100, 200) == -100

# Test per la funzione get_greeting
def test_get_greeting():
    assert get_greeting("Mario") == "Hello, Mario!"
    assert get_greeting("") == "Hello, !"
    assert get_greeting("123") == "Hello, 123!"

# Test per verificare i tipi di input
def test_add_type_error():
    with pytest.raises(TypeError):
        add("2", 3)
    with pytest.raises(TypeError):
        add(2, "3")

def test_subtract_type_error():
    with pytest.raises(TypeError):
        subtract("5", 3)
    with pytest.raises(TypeError):
        subtract(5, "3")

# Test per verificare il comportamento con valori limite
def test_add_edge_cases():
    assert add(2147483647, 1) == 2147483648  # Test con numeri grandi
    assert add(-2147483648, -1) == -2147483649

def test_subtract_edge_cases():
    assert subtract(2147483647, -1) == 2147483648
    assert subtract(-2147483648, 1) == -2147483649 