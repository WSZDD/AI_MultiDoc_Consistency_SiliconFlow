"""Sample project for documentation consistency demo."""

def add(a, b):
    """Add two numbers and return the result."""
    return a + b

def divide(a, b):
    """Divide a by b and return the result. Raises ZeroDivisionError if b is zero."""
    if b == 0:
        raise ZeroDivisionError("Cannot divide by zero.")
    return a / b

def greet(name):
    # Intentionally missing docstring to test detector
    return f"Hello, {name}"

def process_items(items):
    """Process a list of items and return processed list."""
    # Implementation returns count instead of list (intentional inconsistency)
    count = 0
    for _ in items:
        count += 1
    return count
