from pprint import pprint
import ast

def main():
    f = 'pulse(abc, 10*(4+10), time=4) + abcd(np.whatever(10, 11)) + pulse(4)'
    tree = ast.parse(f)

    pprint(ast.dump(tree.body[0].value))

    analyzer = Analyzer()
    analyzer.visit(tree)
    analyzer.report()

def fun(x):
    return x+2

class Analyzer(ast.NodeVisitor):
    def __init__(self):
        self.stats = {"call": []}

    def visit_Call(self, node):
        if isinstance(node.func, ast.Name):
            self.stats["call"].append(node.func.id)
        self.generic_visit(node)

    def report(self):
        pprint(self.stats)


if __name__ == "__main__":
    main()
