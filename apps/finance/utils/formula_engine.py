import ast
import operator as op

_ALLOWED_NAMES = {
    'min': min,
    'max': max,
    'sum': sum,
    'abs': abs,
    'round': round,
}

_ALLOWED_OPERATORS = {
    ast.Add: op.add,
    ast.Sub: op.sub,
    ast.Mult: op.mul,
    ast.Div: op.truediv,
    ast.Pow: op.pow,
    ast.USub: op.neg,
}


def safe_eval(expr: str, variables: dict):
    """ارزیابی ایمن یک عبارت ریاضی ساده با استفاده از AST."""

    def _eval(node):
        if isinstance(node, ast.Num):  # عدد ساده
            return node.n
        if isinstance(node, ast.Constant):
            return node.value
        if isinstance(node, ast.Name):  # متغیرها و توابع مجاز
            if node.id in variables:
                return variables[node.id]
            if node.id in _ALLOWED_NAMES:
                return _ALLOWED_NAMES[node.id]
            raise ValueError(f'نام مجاز نیست: {node.id}')
        if isinstance(node, ast.BinOp):
            return _ALLOWED_OPERATORS[type(node.op)](_eval(node.left), _eval(node.right))
        if isinstance(node, ast.UnaryOp):
            return _ALLOWED_OPERATORS[type(node.op)](_eval(node.operand))
        if isinstance(node, ast.Call):
            func = _eval(node.func)
            args = [_eval(a) for a in node.args]
            return func(*args)
        raise TypeError(node)

    tree = ast.parse(expr, mode='eval').body
    return _eval(tree) 