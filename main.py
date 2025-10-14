#!/usr/bin/env python3
"""
async_calculator.py

Features:
- Class-based `Calculator` with async evaluation API.
- Safe expression evaluation using ast (no eval).
- Supports arithmetic, parentheses, power, modulus.
- Supports math functions: sin, cos, tan, sqrt, log, log10, factorial, abs, round, etc.
- Memory store/recall/clear.
- Batch mode: user can enter unlimited expressions (one per line) and evaluate them.
- Concurrent mode: evaluate many expressions concurrently using asyncio.gather.
- TUI with Rich for nice formatting and prompts.
"""

import ast
import asyncio
import math
import operator
from typing import Any, Dict

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.prompt import Prompt, Confirm

console = Console()


# ---------- Safe Evaluator using AST ----------
class SafeEvalError(Exception):
    pass


class SafeEvaluator(ast.NodeVisitor):
    """
    Evaluate a Python expression AST safely by allowing only a constrained
    set of nodes, operators, and names (math functions/constants).
    """

    ALLOWED_OPERATORS = {
        ast.Add: operator.add,
        ast.Sub: operator.sub,
        ast.Mult: operator.mul,
        ast.Div: operator.truediv,
        ast.Pow: operator.pow,
        ast.Mod: operator.mod,
        ast.FloorDiv: operator.floordiv,
        ast.USub: operator.neg,
        ast.UAdd: operator.pos,
    }

    def __init__(self, names: Dict[str, Any]):
        self._names = names

    def visit(self, node):
        method = f"visit_{node.__class__.__name__}"
        visitor = getattr(self, method, None)
        if visitor is None:
            raise SafeEvalError(f"Unsupported expression: {node.__class__.__name__}")
        return visitor(node)

    def visit_Expression(self, node: ast.Expression):
        return self.visit(node.body)

    def visit_BinOp(self, node: ast.BinOp):
        left = self.visit(node.left)
        right = self.visit(node.right)
        op_type = type(node.op)
        if op_type in self.ALLOWED_OPERATORS:
            return self.ALLOWED_OPERATORS[op_type](left, right)
        raise SafeEvalError(f"Operator not allowed: {op_type.__name__}")

    def visit_UnaryOp(self, node: ast.UnaryOp):
        operand = self.visit(node.operand)
        op_type = type(node.op)
        if op_type in self.ALLOWED_OPERATORS:
            return self.ALLOWED_OPERATORS[op_type](operand)
        raise SafeEvalError(f"Unary operator not allowed: {op_type.__name__}")

    def visit_Call(self, node: ast.Call):
        # Only simple function names allowed: e.g., sin(x), log(2)
        if not isinstance(node.func, ast.Name):
            raise SafeEvalError("Only direct function calls allowed (no attributes).")

        func_name = node.func.id
        func = self._names.get(func_name)
        if func is None or not callable(func):
            raise SafeEvalError(f"Function not allowed: {func_name}")
        args = [self.visit(arg) for arg in node.args]
        # no keywords supported
        return func(*args)

    def visit_Num(self, node: ast.Num):
        return node.n

    def visit_Constant(self, node: ast.Constant):
        # Python 3.8+ uses Constant for numbers/strings/None/...
        if isinstance(node.value, (int, float)):
            return node.value
        raise SafeEvalError(f"Constants of type {type(node.value).__name__} not allowed")

    def visit_Name(self, node: ast.Name):
        if node.id in self._names:
            val = self._names[node.id]
            # allow numbers/constants (like pi, e) and functions via Call nodes
            if isinstance(val, (int, float)):
                return val
            raise SafeEvalError(f"Name '{node.id}' is not a numeric constant")
        raise SafeEvalError(f"Name not allowed: {node.id}")

    def visit_List(self, node: ast.List):
        # allow list of numbers (useful if user wants something like sum([1,2,3])) only if sum allowed
        return [self.visit(elt) for elt in node.elts]

    def generic_visit(self, node):
        raise SafeEvalError(f"Disallowed expression element: {node.__class__.__name__}")


# ---------- Calculator Class ----------
class Calculator:
    def __init__(self):
        self.memory = 0.0
        self._names = self._make_names()

    def _make_names(self) -> Dict[str, Any]:
        """Produce allowed names mapping to math functions and constants."""
        names = {
            # constants
            "pi": math.pi,
            "e": math.e,
            # functions
            "sin": lambda x: math.sin(math.radians(x)),  # accept degrees by default
            "cos": lambda x: math.cos(math.radians(x)),
            "tan": lambda x: math.tan(math.radians(x)),
            "asin": lambda x: math.degrees(math.asin(x)),
            "acos": lambda x: math.degrees(math.acos(x)),
            "atan": lambda x: math.degrees(math.atan(x)),
            "sqrt": math.sqrt,
            "log": math.log,  # natural log
            "log10": math.log10,
            "abs": abs,
            "round": round,
            "floor": math.floor,
            "ceil": math.ceil,
            "fact": lambda n: math.factorial(int(n)),
            "factorial": lambda n: math.factorial(int(n)),
            "sum": sum,
            # memory access as a name
            "mem": self._get_memory_value,
        }
        return names

    def _get_memory_value(self):
        """Allow user to reference mem() if they want numeric memory in expression."""
        return self.memory

    def store_memory(self, value: float):
        self.memory = float(value)

    def recall_memory(self) -> float:
        return self.memory

    def clear_memory(self):
        self.memory = 0.0

    async def evaluate(self, expression: str) -> Any:
        """
        Async wrapper for evaluating a single expression.
        Returns the value or raises SafeEvalError/ValueError.
        """
        # short sleep to allow concurrency demonstration (non-blocking)
        await asyncio.sleep(0)
        result = self._eval_expression(expression)
        return result

    def _eval_expression(self, expression: str) -> Any:
        """
        Parse and evaluate a single expression using AST safely.
        """
        # Preprocess: allow user-friendly caret ^ for power -> replace with **
        # but ^ is bitwise XOR in python; we will not support XOR
        expr = expression.replace("^", "**")
        # allow 'mem' name to be used as mem() or mem
        # If user writes 'mem' as a bare name, SafeEvaluator will consider it a non-numeric name
        # so encourage mem() usage. We'll also replace bare 'mem' with 'mem()' when not followed by '('
        expr = self._replace_bare_mem(expr)

        try:
            node = ast.parse(expr, mode="eval")
        except SyntaxError as e:
            raise SafeEvalError(f"Syntax error: {e}")

        evaluator = SafeEvaluator(self._names)
        return evaluator.visit(node)

    def _replace_bare_mem(self, expr: str) -> str:
        # simple replacement: replace ' mem ' or start/end with mem, or before/after operators
        tokens = []
        cur = ""
        i = 0
        L = len(expr)
        while i < L:
            ch = expr[i]
            # detect 'mem' word
            if expr.startswith("mem", i) and (i + 3 == L or not expr[i + 3].isalnum()):
                # ensure previous char isn't alnum
                prev_ok = (i == 0) or (not expr[i - 1].isalnum())
                if prev_ok:
                    # replace with mem()
                    tokens.append("mem()")
                    i += 3
                    continue
            tokens.append(ch)
            i += 1
        return "".join(tokens)


# ---------- TUI / Interaction ----------
WELCOME = """
Welcome to Async Calculator ✨
You can type any infix expression using + - * / % ** parentheses and supported functions.
Examples:
  2 + 2
  3 * (4 + 5)
  sin(90) + cos(0)
  sqrt(25) + fact(5)
Use 'mem()' to reference stored memory. Use '^' as power too (it will be converted to **).
"""

MENU = """
[1] Evaluate single expression
[2] Batch mode (enter many expressions, finish with an empty line)
[3] Concurrent mode (enter how many expressions, then supply them; they'll run concurrently)
[4] Memory store (store last result into memory)
[5] Memory recall
[6] Memory clear
[0] Exit
"""


async def prompt_loop():
    calc = Calculator()
    last_result = None

    console.print(Panel(WELCOME, title="Async Calculator", expand=False))

    while True:
        console.print(Panel(MENU, title="Menu", expand=False))
        choice = Prompt.ask("Choose an option", choices=[str(i) for i in range(0, 7)], default="1")

        if choice == "0":
            console.print("Goodbye 👋")
            return

        elif choice == "1":
            expr = Prompt.ask("Enter expression")
            try:
                res = await calc.evaluate(expr)
                last_result = res
                console.print(Panel(f"[bold]Result:[/bold] {res}", title=expr))
            except Exception as e:
                console.print(Panel(f"[red]Error:[/red] {e}", title="Evaluation Failed"))

        elif choice == "2":
            console.print("[bold]Batch mode:[/bold] enter expressions one per line. End with an empty line.")
            expressions = []
            while True:
                line = Prompt.ask("> (empty line to finish)", default="")
                if line.strip() == "":
                    break
                expressions.append(line.strip())

            if not expressions:
                console.print("No expressions entered.")
                continue

            results = []
            for expr in expressions:
                try:
                    res = await calc.evaluate(expr)
                    results.append((expr, res, None))
                    last_result = res
                except Exception as e:
                    results.append((expr, None, str(e)))

            table = Table(title="Batch Results")
            table.add_column("Expression", style="cyan")
            table.add_column("Result", style="green")
            table.add_column("Error", style="red")
            for expr, res, err in results:
                table.add_row(expr, str(res) if err is None else "-", err or "-")
            console.print(table)

        elif choice == "3":
            # Concurrent mode
            n = Prompt.ask("How many expressions to evaluate concurrently?", default="3")
            try:
                n_int = max(1, int(n))
            except ValueError:
                console.print("[red]Invalid number; using 3[/red]")
                n_int = 3

            exprs = []
            for i in range(n_int):
                exprs.append(Prompt.ask(f"Expr #{i + 1}"))

            # schedule concurrent evaluations
            tasks = [asyncio.create_task(calc.evaluate(e)) for e in exprs]
            console.print("Evaluating concurrently...")
            results = []
            for i, t in enumerate(tasks, start=1):
                try:
                    val = await t
                    results.append((exprs[i - 1], val, None))
                    last_result = val
                except Exception as e:
                    results.append((exprs[i - 1], None, str(e)))

            table = Table(title="Concurrent Results")
            table.add_column("Expression", style="cyan")
            table.add_column("Result", style="green")
            table.add_column("Error", style="red")
            for expr, res, err in results:
                table.add_row(expr, str(res) if err is None else "-", err or "-")
            console.print(table)

        elif choice == "4":  # memory store
            if last_result is None:
                console.print("[red]No last result to store. Evaluate something first.[/red]")
            else:
                calc.store_memory(last_result)
                console.print(Panel(f"Stored [bold]{last_result}[/bold] into memory.", title="Memory Stored"))

        elif choice == "5":  # memory recall
            memval = calc.recall_memory()
            console.print(Panel(f"Memory: [bold]{memval}[/bold]", title="Memory Recall"))

        elif choice == "6":  # memory clear
            calc.clear_memory()
            console.print(Panel("Memory cleared.", title="Memory"))

        else:
            console.print("[red]Invalid choice[/red]")


def main():
    try:
        # Use asyncio.run for the async prompt loop
        asyncio.run(prompt_loop())
    except KeyboardInterrupt:
        console.print("\n[red]Interrupted by user. Bye![/red]")


if __name__ == "__main__":
    main()
