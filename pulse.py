import ast
import numpy

####
# We accept calls to pulse, or sums of calls to pulse. Arguments can be
# whatever, but the top level expression is fairly restricted.
#
# !! danger danger danger this thing evals its input don't use it !!
####

def parse(text):
    expr = ast.parse(text, mode='eval');
    
    assert isinstance(expr, ast.Expression), "Top level isn't Expression"

    calls = extractCalls(expr.body)
    pulses = list(map(callToPulse, calls))

    return pulses

def callToPulse(call):
    """Converts an ast.Call with two arguments into a Pulse

    Note that the arguments will be evaluated. Input must be trusted.
    Possible to use ast.literal_eval for untrusted input, but
    input won't be able to e.g. call numpy
    """

    assert isinstance(call, ast.Call), "Expected ast.Call"
    assert isinstance(call.func, ast.Name)  # np.whatever() vs whatever()
    assert call.func.id == "pulse", "Only calls to pulse() supported"

    assert len(call.args) == 2, "Expected 2 arguments"

    time = evalArg(call.args[0])
    width = evalArg(call.args[1])

    return Pulse(time, width)

def evalArg(arg):
    """Evaluates an AST node as an Expression"""
    return eval(compile(ast.Expression(arg), filename='', mode='eval'),
                {'np': numpy})

def extractCalls(expr):
    """Extract calls to pulse().

    Expects either a bare ast.Call to pulse() or a sum of calls
    in the form of nested BinOps.

    Returns a list of ast.Call
    """

    assert isinstance(expr, ast.BinOp) or isinstance(expr, ast.Call), \
         "Expected either a BinOp or Call"
    
    if isinstance(expr, ast.Call):
        return [expr]
    elif isinstance(expr, ast.BinOp):
        assert isinstance(expr.op, ast.Add), "Only addition in top level"
        # The sum just flattens the list so we get [1,2,3,4] instead of
        # [[1,2],[3,4]] for "(1+2)+(3+4)"
        return sum(
            [extractCalls(expr.left), extractCalls(expr.right)], []
        )
    else:
        raise TypeError("Expected either a BinOp or Call")

class Pulse(object):
    def __init__(self, time, width):
        self.time = time
        self.width = width

    def __eq__(self, other):
        return self.width == other.width and self.time == other.time
