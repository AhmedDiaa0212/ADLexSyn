import re
from tabulate import tabulate


class OrderedSymbolTable:
    def __init__(self):
        self.table = {}
        self.address_map = {'INT': 2, 'STR': 24, 'BOOL': 1}
        self.counter = 1

    def add_entry(self, name, datatype, line_decl, line_ref):
        if name not in self.table:
            self.table[name] = {
                'index': self.counter,
                'name': name,
                'address': None,
                'datatype': datatype,
                'dimension': 0,
                'line_decl': line_decl,
                'line_ref': [ref for ref in line_ref if ref != line_decl]
            }
            self.counter += 1

    def lexer(self, source_code, patterns):
        tokens = []
        for line in source_code.split('\n'):
            for pattern, token_type in patterns:
                matches = re.findall(pattern, line)
                if matches:
                    for match in matches:
                        tokens.append((match, token_type))
        return tokens

    def build_symbol_table(self, source_code, patterns):
        tokens = self.lexer(source_code, patterns)
        lines = source_code.strip().split('\n')

        identifiers = []  # List to store identifiers

        # Step 1: Extract all identifiers
        for token in tokens:
            if token[1] == 'IDENTIFIER':
                identifiers.append(token[0])

        # Step 2: Sort identifiers alphabetically
        identifiers.sort()

        # Step 3: Add entries to the symbol table in alphabetical order
        for identifier in identifiers:
            datatype = None
            line_decl = None
            line_ref = []

            # Find data type and declaration line for the current identifier
            for i, line in enumerate(lines):
                if identifier in line:
                    if line_decl is None:
                        line_decl = i + 1
                    line_ref.append(i + 1)
            for token in tokens:
                if token[0] == identifier:
                    for i in range(tokens.index(token), -1, -1):
                        if tokens[i][1] in [ 'STR', 'INT', 'BOOL']:
                            datatype = tokens[i][1]
                            break

            if datatype:
                self.add_entry(identifier, datatype, line_decl, line_ref)

        # Assign addresses
        address = 0
        for entry in self.table.values():
            entry['address'] = address
            address += self.address_map[entry['datatype']]


    def print_table(self):
        table_data = []
        for entry in self.table.values():
            table_data.append([
                entry['index'],
                entry['name'],
                entry['address'],
                entry['datatype'],
                entry['dimension'],
                entry['line_decl'],
                entry['line_ref']
            ])
        headers = ["Index", "Name", "Address", "DataType", "Dimension", "LineDecl", "LineRef"]
        print(tabulate(table_data, headers=headers, tablefmt="fancy_grid", colalign=("left", "left")))
