class HashSymbolTable:
    def __init__(self, lexer_output):
        self.lexer_output = lexer_output

        # Extract identifiers from lexer output and insert them into the hash table
        variable_names = [token[0] for token in self.lexer_output if token[1] == 'IDENTIFIER']
        hash_max = len(variable_names)
        self.hash_table = [[] for _ in range(hash_max)]

        for var_name in variable_names:
            hash_value = self.hash_function(var_name)
            self.hash_table[hash_value].append(var_name)

    def hash_function(self, var_name):
        ascii_first_letter = ord(var_name[1])
        return (len(var_name) + ascii_first_letter) % len(self.hash_table)

    def print_hash_table(self):
        for index, entry in enumerate(self.hash_table):
            print(f"{index} -> [{'  ->  '.join(entry)}]")