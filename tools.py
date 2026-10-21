import ast
import operator
import os


# =========================================================
# Calculator Tool
# =========================================================

_ALLOWED_OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
    ast.Mod: operator.mod,
    ast.USub: operator.neg,
}


def _safe_calculate(node):
    """
    Safely evaluate a basic mathematical expression.
    """

    if isinstance(node, ast.Constant):

        if isinstance(node.value, (int, float)):

            return node.value

        raise ValueError(
            "Only numbers are allowed."
        )

    if isinstance(node, ast.BinOp):

        left = _safe_calculate(node.left)
        right = _safe_calculate(node.right)

        operator_type = type(node.op)

        if operator_type not in _ALLOWED_OPERATORS:

            raise ValueError(
                "Unsupported mathematical operation."
            )

        if (
            operator_type is ast.Div
            and right == 0
        ):

            raise ValueError(
                "Cannot divide by zero."
            )

        return _ALLOWED_OPERATORS[
            operator_type
        ](left, right)

    if isinstance(node, ast.UnaryOp):

        operand = _safe_calculate(node.operand)

        operator_type = type(node.op)

        if operator_type not in _ALLOWED_OPERATORS:

            raise ValueError(
                "Unsupported unary operation."
            )

        return _ALLOWED_OPERATORS[
            operator_type
        ](operand)

    raise ValueError(
        "Invalid mathematical expression."
    )


def calculator(expression: str):

    """
    Perform a safe mathematical calculation.
    """

    try:

        tree = ast.parse(
            expression,
            mode="eval"
        )

        result = _safe_calculate(
            tree.body
        )

        return {
            "success": True,
            "result": result
        }

    except Exception as e:

        return {
            "success": False,
            "error": str(e)
        }


# =========================================================
# File Reader Tool
# =========================================================

def read_file(filename: str):

    """
    Read a text file from the data folder.
    """

    try:

        # Security:
        # Only allow files inside data folder.

        safe_filename = os.path.basename(
            filename
        )

        file_path = os.path.join(
            "data",
            safe_filename
        )

        if not os.path.exists(file_path):

            return {
                "success": False,
                "error": (
                    f"File '{safe_filename}' "
                    "was not found."
                )
            }

        with open(
            file_path,
            "r",
            encoding="utf-8"
        ) as file:

            content = file.read()

        return {
            "success": True,
            "filename": safe_filename,
            "content": content
        }

    except Exception as e:

        return {
            "success": False,
            "error": str(e)
        }


# =========================================================
# Search Tool
# =========================================================

def search(query: str):

    """
    Simple research search tool.

    This first version is a learning tool.
    Later we can connect it to a real web search API.
    """

    if not query.strip():

        return {
            "success": False,
            "error": (
                "Search query cannot be empty."
            )
        }

    # Learning/demo response
    return {
        "success": True,
        "query": query,
        "result": (
            f"Search requested for: {query}. "
            "For this first version, connect "
            "a real web-search provider in the "
            "next upgrade."
        )
    }


# =========================================================
# Tool Registry
# =========================================================

AVAILABLE_FUNCTIONS = {

    "calculator": calculator,

    "read_file": read_file,

    "search": search
}