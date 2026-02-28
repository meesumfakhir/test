import ast
import operator as op


def add(a, b):
    """Return the sum of a and b."""
    return a + b


def subtract(a, b):
    """Return the difference of a and b."""
    return a - b


def multiply(a, b):
    """Return the product of a and b."""
    return a * b


def divide(a, b):
    """Return a divided by b. Raises ValueError if b is zero."""
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b


_OPERATORS = {
    ast.Add: op.add,
    ast.Sub: op.sub,
    ast.Mult: op.mul,
    ast.Div: op.truediv,
    ast.USub: op.neg,
}


def _eval_node(node):
    if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
        return node.value
    if isinstance(node, ast.BinOp) and type(node.op) in _OPERATORS:
        left = _eval_node(node.left)
        right = _eval_node(node.right)
        if isinstance(node.op, ast.Div) and right == 0:
            raise ValueError("Cannot divide by zero")
        return _OPERATORS[type(node.op)](left, right)
    if isinstance(node, ast.UnaryOp) and type(node.op) in _OPERATORS:
        return _OPERATORS[type(node.op)](_eval_node(node.operand))
    raise ValueError(f"Unsupported expression element: {ast.dump(node)}")


def calculate(expression):
    """Evaluate a simple arithmetic expression string (+, -, *, /)."""
    try:
        tree = ast.parse(expression, mode="eval")
        return _eval_node(tree.body)
    except ValueError:
        raise
    except Exception:
        raise ValueError(f"Invalid expression: {expression}")


if __name__ == "__main__":
    print("Simple Calculator")
    print("-----------------")
    while True:
        expr = input("Enter expression (or 'quit' to exit): ").strip()
        if expr.lower() in ("quit", "exit", "q"):
            break
        try:
            print(f"= {calculate(expr)}")
        except ValueError as e:
            print(f"Error: {e}")
