import ast
import numpy
import units

####
# We accept calls to pulse, or sums of calls to pulse. Arguments can be
# whatever, but the top level expression is fairly restricted.
#
# !! danger danger danger this thing evals its input don't use it !!
####

class PulseParser(object):
    def __init__(self, vars={}):
        # User-provided variables
        self.vars = vars

        # acq4 units
        self.vars.update(units.allUnits)

        # numpy
        self.vars['np'] = numpy

    def addVar(self, var, value=None):
        """Add variable to eval namespace. If value is None'
        variable will evaluate to its own name as a string"""

        if value is None:
            self.vars[var] = var
        else:
            self.vars[var] = value

    def parse(self, text):
        text = text.replace("\n", '').replace("\r", '')

        expr = ast.parse(text, mode='eval');
    
        assert isinstance(expr, ast.Expression), \
            "Top level isn't Expression"

        calls = self.extractCalls(expr.body)
        pulses = list(map(self.callToPulse, calls))

        return pulses

    def callToPulse(self, call):
        """Converts an ast.Call with two arguments into a Pulse

        Note that the arguments will be evaluated. Input must be trusted.
        Possible to use ast.literal_eval for untrusted input, but
        input won't be able to e.g. call numpy
        """

        assert isinstance(call, ast.Call), "Expected ast.Call"
        assert isinstance(call.func, ast.Name)
        assert call.func.id == "pulse", "Only calls to pulse() supported"

        assert len(call.args + call.keywords) == 3, \
            "Expected 3 arguments"

        # Merge positional and keyword arguments into args dictionary
        args = {}
        keywords = {0: 'times', 1: 'widths', 2: 'values'}
        for index, value in enumerate(call.args):   # Positional args
            args[keywords[index]] = value
        
        for keyword in call.keywords:               # Keyword args
            args[keyword.arg] = keyword.value

        # Eval args
        for keyword, value in args.items():
            args[keyword] = self.evalArg(value)

        # Construct pulse
        return pulse(
            times=args['times'],
            widths=args['widths'],
            values=args['values']
        )

    def evalArg(self, arg):
        """Evaluates an AST node as an Expression"""
        return eval(compile(
            ast.Expression(arg), filename='', mode='eval'
        ), self.vars)

    def extractCalls(self, expr):
        """Extract calls to pulse().

        Expects either a bare ast.Call to pulse() or a sum of calls
        in the form of nested BinOps.

        Returns a list of ast.Call
        """

        assert isinstance(expr, ast.BinOp) or \
               isinstance(expr, ast.Call), \
               "Expected either a BinOp or Call"
    
        if isinstance(expr, ast.Call):
            return [expr]
        elif isinstance(expr, ast.BinOp):
            assert isinstance(expr.op, ast.Add), \
                "Only addition in top level"
            # The sum just flattens the list so we get [1,2,3,4]
            # instead of [[1,2],[3,4]] for "(1+2)+(3+4)"
            return sum([
                self.extractCalls(expr.left),
                self.extractCalls(expr.right)
            ], [])
        else:
            raise TypeError("Expected either a BinOp or Call")


def pulse(times, widths, values):
    return (times, widths, values)

