import re

# Define the regular expressions for different tokens
patterns = [
        (r'\b(print)\b', 'KEYWORD'),
        (r'\b(\d+)\b', 'INT'),
        (r'\b(true|false)\b', 'BOOL'),
        (r'\$[A-Za-z_][A-Za-z0-9_]*', 'IDENTIFIER'),  
        (r'"([^"]*)"', 'STR'),  # Match double-quoted string specifically
        (r'(\+|-|\*|/|==|!=|<|>|<=|>=)', 'OPERATOR'),
        (r'=', 'ASSIGNMENT'),
        (r';', 'SEMICOLON'),
        (r'\(', 'LPAREN'),
        (r'\)', 'RPAREN'),
    ]

def lexer(code):
    tokens = []
    code = code.strip()
    while code:
        for pattern, token_type in patterns:
            match = re.match(pattern, code)
            if match:
                lexeme = match.group(0)
                tokens.append((lexeme, token_type))
                code = code[len(lexeme):].strip()
                break
        else:
            raise ValueError('Invalid character: ' + code[0])
    return tokens