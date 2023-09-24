import re


# Function to validate if a line of production is valid
def es_linea_valida(linea):
    # Utilizamos una regex para validar el formato de la producción
    # La regex verifica que la línea tenga el formato
    # "no_terminal -> cuerpo_de_producción"
    estructura = r'^[A-Z]\s*->\s*([A-Za-z0-9ε]+(\s*\|\s*[A-Za-z0-9ε]+)*)?$'
    return re.match(estructura, linea) is not None


# Function to load a grammar from a text file
def cargar_gramatica(archivo):
    gramatica = {}
    with open(archivo, 'r', encoding='utf-8') as file:
        for linea in file:
            # Eliminamos espacios en blanco al inicio y al final de la línea
            linea = linea.rstrip()
            if es_linea_valida(linea):
                partes = linea.split('->')
                no_terminal = partes[0].rstrip()
                cuerpo = partes[1]
                producciones = cuerpo.rstrip().split('|')
                gramatica[no_terminal] = [p.rstrip().strip() for p in producciones]
            else:
                print(f"Error: Línea inválida en el archivo: {linea}")
                return None
    return gramatica


def split_string_to_list(string):
  list1 = []
  for n in range(len(string)):
    list1.append(string[n])
  return list1


def remove_unreachable_symbols(grammar):
    reachable = set()  # Set to store reachable symbols
    stack = ['S']  # Start with the start symbol
    while stack:
        symbol = stack.pop()
        if symbol not in reachable:
            reachable.add(symbol)
            # Split the production into individual symbols and check if each symbol is uppercase
            for production in grammar.get(symbol, []):
                productionSymnols = split_string_to_list(production)
                for symbol_in_production in productionSymnols:
                    if symbol_in_production.isupper():
                        stack.append(symbol_in_production)

    # Remove unreachable symbols
    for symbol in list(grammar.keys()):
        if symbol not in reachable:
            del grammar[symbol]


def remove_unproductive_symbols(grammar):
    productive = set()  # Set to store productive symbols
    
    while True:
        prev_len = len(productive)
        for symbol, productions in grammar.items():
            if len(productions) == 1 and len(split_string_to_list(productions[0])) == 1 and split_string_to_list(productions[0])[0] == symbol:
               pass
            else:
                for production in productions:
                    p_chars = split_string_to_list(production)
                    pass
        if len(productive) == prev_len:
            break
    
    # Remove unproductive symbols
    for symbol in list(grammar.keys()):
        if symbol not in productive:
            del grammar[symbol]


def eliminate_epsilon_productions(grammar):
    epsilon_producing = set()  # Set to store epsilon-producing symbols
    
    # Find epsilon-producing symbols
    for symbol, productions in grammar.items():
        if 'ε' in productions:
            epsilon_producing.add(symbol)
    print('----------------------------------------------------------------')
    print(f'''
Epsilum productions found:
{epsilon_producing}
''')
    print('----------------------------------------------------------------')
    # Remove epsilon productions
    for symbol, productions in grammar.items():
        grammar[symbol] = [production for production in productions if production != 'ε']

    print('----------------------------------------------------------------')
    print('Epsilum productions removed, result:')
    print_grammar(grammar)
    print('----------------------------------------------------------------')
    # Update productions affected by epsilon-producing symbols
    for symbol, productions in grammar.items():
        for eps_symbol in epsilon_producing:
            for production in productions[:]:  # Iterate over a copy
                if eps_symbol in production:
                    cicles = production.count(eps_symbol) #replacements for epsilon production to do
                    r = 1 # replacements done
                    while r <= cicles:
                        new_productions = [production.replace(eps_symbol, '', r)]
                        grammar[symbol].extend(new_productions)
                        r += 1

    print('----------------------------------------------------------------')
    print('Created G1 -> L[G1] = L[G] - ε')
    print_grammar(grammar)
    print('----------------------------------------------------------------')
    # If start symbol is epsilon-producing, add a new start symbol
    if 'S' in epsilon_producing:
        grammar['S0'] = ['ε']
    # remover espacios vaciós en producciones
    for symbol, productions in grammar.items():
        grammar[symbol] = [pproduction for pproduction in productions if pproduction != '']


def print_grammar(grammar):
    for symbol, productions in grammar.items():
        production_str = ' | '.join(productions)
        print(f"{symbol} -> {production_str}")


nombre_archivo = 'gramatica1.txt'  # Reemplaza con el nombre de tu archivo
cfg = cargar_gramatica(nombre_archivo)
print('-------------------------Gramatica Inicial---------------------------------------')
print_grammar(cfg)
eliminate_epsilon_productions(cfg)
print('-------------------------Resultado final---------------------------------------')
print_grammar(cfg)
