from anytree import Node

class Parser:
    def __init__(self):
        self.root = None

    def parse_program(self, tokens):
        self.root = Node("<program>")
        statement_list_node = Node("<statement_list>", parent=self.root)
        self.statement_list(tokens, statement_list_node)
        return self.root

    def statement_list(self, tokens, parent):
        while tokens:
            statement_node = Node("<statement>", parent=parent)
            self.statement(tokens, statement_node)

    def statement(self, tokens, parent):
        if tokens[0][0] == 'print':
            self.print_statement(tokens, parent)
        elif tokens[0][1] == 'IDENTIFIER':
            self.assignment_statement(tokens, parent)
        else:
            raise SyntaxError(f"Invalid statement at position {tokens[0]}")

    def print_statement(self, tokens, parent):
        node = Node("<print_statement>", parent=parent)
        self.match_token(tokens, 'KEYWORD', node)
        self.match_token(tokens, 'LPAREN', node)
        self.expression(tokens, node)
        self.match_token(tokens, 'RPAREN', node)
        self.match_token(tokens, 'SEMICOLON', node)

    def assignment_statement(self, tokens, parent):
        node = Node("<assignment_statement>", parent=parent)
        self.match_token(tokens, 'IDENTIFIER', node)
        self.match_token(tokens, 'ASSIGNMENT', node)
        self.expression(tokens, node)
        self.match_token(tokens, 'SEMICOLON', node)

    def expression(self, tokens, parent):
        node = Node("<expression>", parent=parent)
        self.term(tokens, node)
        self.expression_tail(tokens, node)

    def expression_tail(self, tokens, parent):
        if tokens and tokens[0][1] == 'OPERATOR':
            node = Node("<expression_tail>", parent=parent)
            self.operator(tokens, node)
            self.term(tokens, node)
            self.expression_tail(tokens, node)

    def operator(self, tokens, parent):
        Node(f"OPERATOR: {tokens[0][0]}", parent=parent)
        tokens.pop(0)

    def term(self, tokens, parent):
        node = Node("<term>", parent=parent)
        Node(f"{tokens[0][1]}: {tokens[0][0]}", parent=node)
        tokens.pop(0)

    def match_token(self, tokens, expected_type, parent):
        if tokens[0][1] == expected_type:
            Node(f"{expected_type}: {tokens[0][0]}", parent=parent)
            tokens.pop(0)
        else:
            raise SyntaxError(f"Expected token type {expected_type}, but received {tokens[0][1]}")
