from tabulate import tabulate
from anytree import RenderTree
from p1_lexer import lexer
from p1_lexer import patterns
from p2_Parser import Parser
from p3_1_unordered_symbol_table import UnorderedSymbolTable
from p3_2_ordered_symbol_table import OrderedSymbolTable
from p3_3_hash_symbol_table import HashSymbolTable

def get_code_from_file(filename):
    """
    Reads and extracts code from a file.
    """
    try:
        # Open the file in read mode
        with open(filename, 'r') as file:
            # Read all the content from the file
            code = file.read()
            return code
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
        return None
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None

# Drive the code
output_file = "output.txt"  # Name of the file to save output

with open(output_file, 'w', encoding='utf-8') as f:  # Specify UTF-8 encoding
    # Redirect standard output to the file
    import sys
    class Tee:
        def __init__(self, *files):
            self.files = files
        def write(self, obj):
            for f in self.files:
                f.write(obj)
                f.flush()  # Ensure immediate flushing
        def flush(self):
            for f in self.files:
                f.flush()
    tee = Tee(sys.stdout, f)
    sys.stdout = tee
    
    # 1.Extract the code from the file
    print("\n---------------------------------------------------------------------------------")
    print("\t Extracted Code ")
    print("---------------------------------------------------------------------------------\n")
    extracted_code = get_code_from_file('test.txt')
    print(extracted_code)

    # 2. Tokenize the extracted code
    print("\n---------------------------------------------------------------------------------")
    print("\t Lexical Analysis ")
    print("---------------------------------------------------------------------------------\n")
    tokens = lexer(extracted_code)
    table_data = [[lexeme, token_type] for lexeme, token_type in tokens]
    table_headers = ["Lexemes", "Tokens"]
    table = tabulate(table_data, headers=table_headers, tablefmt="fancy_grid", colalign=("left", "left"))
    print(table)

    # 3. Parse the extracted tokens
    print("\n---------------------------------------------------------------------------------")
    print("\t Syntax Analysis ")
    print("---------------------------------------------------------------------------------\n")
    try:
        parser = Parser()
        root = parser.parse_program(tokens)
        print("Parsing successful")
        for pre, fill, node in RenderTree(root):
            print(f"{pre}{node.name}")
    except SyntaxError as e:
        print("Syntax Error:", str(e))

    # 4. Unordered symbol table
    print("\n---------------------------------------------------------------------------------")
    print("\t Unordered Symbol Table ")
    print("---------------------------------------------------------------------------------\n")
    Unordered_SymbolTable = UnorderedSymbolTable()
    Unordered_SymbolTable.build_symbol_table(extracted_code, patterns)
    Unordered_SymbolTable.print_table()

    # 5. ordered symbol table
    print("\n---------------------------------------------------------------------------------")
    print("\t ordered Symbol Table ")
    print("---------------------------------------------------------------------------------\n")
    Ordered_SymbolTable = OrderedSymbolTable()
    Ordered_SymbolTable.build_symbol_table(extracted_code, patterns)
    Ordered_SymbolTable.print_table()

    # 5. Hash symbol table
    print("\n---------------------------------------------------------------------------------")
    print("\t Hash Symbol Table ")
    print("---------------------------------------------------------------------------------\n")
    l = lexer(extracted_code)
    hash_table_obj = HashSymbolTable(l)
    hash_table_obj.print_hash_table()

# Reset standard output
sys.stdout = sys.__stdout__
print(f"Output saved to '{output_file}'")
