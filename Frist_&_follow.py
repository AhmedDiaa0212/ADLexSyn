from tabulate import tabulate

# Define the grammar
#This grammar is ambiguous.
grammar = {
    'S': ['aXb', 'X'],
    'X': ['cXb', 'b', 'bXZ'],
    'Z': ['n']
}

#This grammar is not  ambiguous.
"""grammar = {
    'S': ['aXb', 'X'],
    'X': ['cXb', 'b'],
    'Z': ['n']
}"""
# Print the grammar
print("\n- Grammar:")
for nonterminal, productions in grammar.items():
    print(f"{nonterminal} -> {' | '.join(productions)}")

# Define terminals and non-terminals
terminals = set()
non_terminals = set()
for lhs in grammar:
    non_terminals.add(lhs)
    for rhs in grammar[lhs]:
        for symbol in rhs:
            if symbol.islower():
                terminals.add(symbol)
            else:
                non_terminals.add(symbol)

# Add $ to the set of terminals
terminals.add("$")

# Define FIRST and FOLLOW sets
FIRST = {}
FOLLOW = {}
for non_terminal in non_terminals:
    FIRST[non_terminal] = set()
    FOLLOW[non_terminal] = set()

# Function to compute FIRST sets
def compute_first():
    for lhs in grammar:
        compute_first_recursive(lhs)

def compute_first_recursive(non_terminal):
    if non_terminal in FIRST[non_terminal]:
        return
    for rhs in grammar[non_terminal]:
        if rhs[0] in terminals:
            FIRST[non_terminal].add(rhs[0])
        elif rhs[0] in non_terminals:
            compute_first_recursive(rhs[0])
            FIRST[non_terminal] |= FIRST[rhs[0]]

# Function to compute FOLLOW sets
def compute_follow():
    FOLLOW['S'].add('$')
    for lhs in grammar:
        compute_follow_recursive(lhs)

def compute_follow_recursive(non_terminal):
    for lhs in grammar:
        for rhs in grammar[lhs]:
            if non_terminal in rhs:
                idx = rhs.index(non_terminal)
                if idx == len(rhs) - 1:
                    if lhs != non_terminal:
                        FOLLOW[non_terminal] |= FOLLOW[lhs]
                else:
                    next_symbol = rhs[idx + 1]
                    if next_symbol in non_terminals:
                        first_set = FIRST[next_symbol]
                        if "" in first_set:
                            FOLLOW[non_terminal] |= first_set - {""}
                            FOLLOW[non_terminal] |= FOLLOW[lhs]
                        else:
                            FOLLOW[non_terminal] |= first_set
                    elif next_symbol in terminals:
                        FOLLOW[non_terminal].add(next_symbol)

# Function to construct the parsing table
def construct_parsing_table():
    parsing_table = {non_terminal: {terminal: [] for terminal in terminals} for non_terminal in non_terminals}
    for lhs in grammar:
        for rhs in grammar[lhs]:
            first_set = set()
            idx = 0
            for symbol in rhs:
                if symbol in terminals:
                    first_set.add(symbol)
                    break
                elif "" not in FIRST[symbol]:
                    first_set |= FIRST[symbol]
                    break
                else:
                    first_set |= FIRST[symbol] - {""}
                    idx += 1
            for terminal in first_set:
                parsing_table[lhs][terminal].append(rhs)
            if "" in first_set or len(first_set) == 0:
                for terminal in FOLLOW[lhs]:
                    parsing_table[lhs][terminal].append(rhs)
    return parsing_table

# Compute FIRST and FOLLOW sets
compute_first()
compute_follow()

# Construct the parsing table
parsing_table = construct_parsing_table()

# Print the FIRST and FOLLOW sets
print("\nFIRST and FOLLOW sets:")
headers = ["Nonterminal", "FIRST", "FOLLOW"]
table_data = []
for non_terminal in non_terminals:
    table_data.append([non_terminal, FIRST[non_terminal], FOLLOW[non_terminal]])
print(tabulate(table_data, headers=headers,  tablefmt="fancy_grid", colalign=("left", "left")))

# Print the parsing table
print("\nParsing Table:")
headers = [""] + list(terminals)
table_data = []
for non_terminal in non_terminals:
    row = [non_terminal]
    for terminal in terminals:
        row.append(", ".join(parsing_table[non_terminal][terminal]))
    table_data.append(row)
print(tabulate(table_data, headers=headers,  tablefmt="fancy_grid", colalign=("left", "left")))

# Check if the grammar is ambiguous
ambiguous = False
for non_terminal in parsing_table:
    for terminal in parsing_table[non_terminal]:
        if len(parsing_table[non_terminal][terminal]) > 1:
            ambiguous = True
            break

# Print whether the grammar is ambiguous or not
if ambiguous:
    print("\nThe grammar is ambiguous.")
else:
    print("\nThe grammar is not ambiguous.")