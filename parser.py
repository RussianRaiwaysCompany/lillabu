import ply.yacc as yacc
import ply.lex as lex
import lexer

class DataUnit:
    def __init__(self, type : str, count : int, cost : int):
        self.type = type
        self.count = count
        self.cost = cost

    def __str__(self):
        return f"DATA type = {self.type}, count = {self.count}, cost = {self.cost}"

class RouteUnit:
    def __init__(self, x : int, y : int, cost : int):
        self.x = x
        self.y = y
        self.cost = cost

    def __str__(self):
        return f"ROUTE x = {self.x}, y = {self.y}, cost = {self.cost}"

class OrderUnit:
    def __init__(self, type : str, dir : int):
        self.type = type
        self.dir = dir

    def __str__(self):
        return f"ORDER type = {self.type}, dir = {self.dir}"

class ParserRules:
    tokens = lexer.LexerRules.tokens

    def p_RESULT(p):
        """RESULT : DATASECTION ROUTESECTION ORDERSECTION 
                  | DATASECTION ROUTESECTION"""
        if len(p) == 4:
            p[0] = (p[1], p[2], p[3])
        else:
            p[0] = (p[1], p[2], None)

    def p_DENTRY(p):
        'DENTRY : TYPE NUMBER NUMBER'
        p[0] = DataUnit(p[1], p[2], p[3])

    def p_RENTRY(p):
        'RENTRY : NUMBER NUMBER NUMBER'
        p[0] = RouteUnit(p[1], p[2], p[3])

    def p_OENTRY(p):
        'OENTRY : TYPE NUMBER'
        p[0] = OrderUnit(p[1], p[2])

    def p_DATALIST(p):
        """DATALIST : DENTRY DATALIST 
                    | DENTRY"""
        if len(p) == 3:
            p[0] = [p[1]] + p[2]
        else:
            p[0] = [p[1]]

    def p_ROUTELIST(p):
        """ROUTELIST : RENTRY ROUTELIST 
                     | RENTRY"""
        if len(p) == 3:
            p[0] = [p[1]] + p[2]
        else:
            p[0] = [p[1]]

    def p_ORDERLIST(p):
        """ORDERLIST : OENTRY ORDERLIST 
                     | OENTRY"""
        if len(p) == 3:
            p[0] = [p[1]] + p[2]
        else:
            p[0] = [p[1]]

    def p_DATASECTION(p):
        'DATASECTION : DATA DATALIST TERM'
        p[0] = p[2]

    def p_ROUTESECTION(p):
        'ROUTESECTION : ROUTE ROUTELIST TERM'
        p[0] = p[2]

    def p_ORDERSECTION(p):
        'ORDERSECTION : ORDER ORDERLIST TERM'
        p[0] = p[2]

    def p_error(p):
        if p:
            print(f"Syntax error at '{p.value}' on line {p.lexer.lineno}")

def parse(data : str):
    l = lex.lex(module=lexer.LexerRules)
    parser = yacc.yacc(module=ParserRules)
    return parser.parse(data, l)

if __name__ == "__main__":
    import sys

    def main():
        if len(sys.argv) != 2:
            print("usage: parser.py <file to parse>")
            sys.exit(1)

        with open(sys.argv[1], "r") as file:
            data, route, order = parse(file.read())

        for entry in data:
            print(entry)

        for entry in route:
            print(entry)

        if order:
            for entry in order:
                print(entry)

    main()

