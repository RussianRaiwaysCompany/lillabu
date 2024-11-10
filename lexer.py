import ply.lex as lex # WE LOVE FLEX & BISON !!!

class LexerRules:
    states = (
        ('SDATA', 'exclusive'),
        ('SROUTE', 'exclusive'),
        ('SORDER', 'exclusive'),
    )

    tokens = (
            'NUMBER',
            'TYPE',

            'DATA',
            'ROUTE',
            'ORDER',
            'TERM',

            'COMMENT',
    )

    def t_SDATA_SROUTE_SORDER_NUMBER(t):
        r'\d+'
        t.value = int(t.value)
        return t

    t_SDATA_SORDER_TYPE = r'(L1|L2|L3|L4|T4|T8|B1)'

    def t_ANY_error(t):
        raise RuntimeError( \
            f"Illegal character '{t.value[0]}' at line {t.lexer.lineno}")

    t_TERM = r'/'

    def t_ANY_COMMENT(t):
        r'--[^\n]*'

    def t_INITIAL_DATA(t):
        r'DATA'
        t.lexer.push_state('SDATA')
        return t

    def t_INITIAL_ROUTE(t):
        r'ROUTE'
        t.lexer.push_state('SROUTE')
        return t

    def t_INITIAL_ORDER(t):
        r'ORDER'
        t.lexer.push_state('SORDER')
        return t

    def t_ANY_TERM(t):
        r'/'
        t.lexer.pop_state()
        return t

    t_ANY_ignore = ' \t'

    def t_ANY_newline(t):
        r'\n+'
        t.lexer.lineno += len(t.value)

class Tokens:
    def __init__(self, lex_instance : lex.Lexer):
        self.lex_instance = lex_instance

    def __iter__(self):
        return self

    def __next__(self):
        token = self.lex_instance.token()
        if not token:
            raise StopIteration
        return token

def tokenize(data : str):
    lexer = lex.lex(module=LexerRules)
    lexer.input(data)
    return Tokens(lexer)


def tokenize_file(filename : str):
    try:
        with open(filename, "r") as file:
            lines = file.read()
    except OSError:
        raise ValueError(f"file {filename} not found")

    return tokenize(lines)

if __name__ == "__main__":
    import sys

    def dump_file(filename : str):
        try:
            with open(filename, "r") as file:
                print(file.read())
        except OSError:
            print(f"file {filename} not found")

    def dump_file_tokens(filename : str):
        try:
            tokens = tokenize_file(filename)
            for token in tokenize_file(filename):
                print(token)
        except Exception as e:
            print(e)

    def main():
        if len(sys.argv) != 2:
            print("usage: lexer.py <file to tokenize>")
            sys.exit(1)

        print("HERE IS SOURCE FILE:")
        dump_file(sys.argv[1])
        print("HERE IS ITS TOKENS:")
        dump_file_tokens(sys.argv[1])

    main()



