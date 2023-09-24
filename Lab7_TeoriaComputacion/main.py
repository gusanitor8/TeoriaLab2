'''
Laboratorio 7 - Teoría de la Computacion
Universidad del Valle de Guatemala
Maria Marta Ramirez
Gustavo Andres Gonzalez
'''
# Importar modulo de Python para trabajar con expresiones regulares
import re

def is_valid_production(production):
    # Definir la regex para validar producciones
    regex_production = r'^[A-Za-zΑ-Ωα-ω0-9_]+(\s*->\s*[A-Za-zΑ-Ωα-ω0-9_]+(\s*\|\s*[A-Za-zΑ-Ωα-ω0-9_]+)*)?$'
    return bool(re.match(regex_production, production))

def load_grammar(file_name):
    grammar = {}
    
    try:
        with open(file_name, 'r', encoding='utf-8') as file:
            for line in file:
                line = line.strip()
                if is_valid_production(line):
                    parts = line.split('->')
                    non_terminal = parts[0].strip()
                    productions = parts[1].split('|')
                    grammar[non_terminal] = [p.strip() for p in productions]
                else:
                    print(f"Error: Producción no válida en línea '{line}'")
                    return None
    except FileNotFoundError:
        print(f"Error: No se encontró el archivo '{file_name}'")
        return None
    
    return grammar

def remove_unreachable_symbols(grammar):
    reachable = set()  # Conjunto para almacenar símbolos alcanzables
    stack = ['S']  # Comenzar con el símbolo inicial
    
    while stack:
        symbol = stack.pop()
        if symbol not in reachable:
            reachable.add(symbol)
            
            # Obtener las producciones del símbolo
            productions = grammar.get(symbol, [])
            
            for production in productions:
                # Usar conjuntos para obtener todos los símbolos mayúsculas de la producción
                symbols_in_production = set(production) & set(grammar.keys())
                
                # Agregar los símbolos alcanzables a la pila
                stack |= symbols_in_production

    # Eliminar símbolos no alcanzables del diccionario de gramática
    grammar = {symbol: productions for symbol, productions in grammar.items() if symbol in reachable}

    return grammar

def remove_unproductive_symbols(grammar):
    productive = set()  # Conjunto para almacenar símbolos productivos
    
    while True:
        prev_len = len(productive)
        for symbol, productions in grammar.items():
            # Verificar si el símbolo es productivo
            is_productive = any(all(p_char in productive for p_char in production) for production in productions)
            if is_productive:
                productive.add(symbol)
        
        if len(productive) == prev_len:
            break

    # Eliminar símbolos no productivos del diccionario de gramática
    grammar = {symbol: productions for symbol, productions in grammar.items() if symbol in productive}

    return grammar

def eliminate_epsilon_productions(grammar):
    epsilon_producing = set()  # Conjunto para almacenar símbolos que producen ε
    
    # Encontrar símbolos que producen ε
    for symbol, productions in grammar.items():
        if 'ε' in productions:
            epsilon_producing.add(symbol)
    
    print('')
    print('Producciones ε encontradas:')
    for symbol in epsilon_producing:
        print(symbol)
    print('')

    # Eliminar producciones ε
    for symbol, productions in grammar.items():
        grammar[symbol] = [production for production in productions if production != 'ε']

    print('----------------------------------------------------------------')
    print('')
    print('Las producciones ε han sido eliminadas con éxito.')
    print('El resultado es:')
    display_grammar(grammar)
    print('')

    
    # Actualizar producciones afectadas por símbolos que producen ε
    for symbol, productions in grammar.items():
        for eps_symbol in epsilon_producing:
            for production in productions[:]:  # Iterar sobre una copia
                if eps_symbol in production:
                    count = production.count(eps_symbol)  # Número de reemplazos a hacer
                    replacements_done = 1
                    while replacements_done <= count:
                        new_productions = [production.replace(eps_symbol, '', replacements_done)]
                        grammar[symbol].extend(new_productions)
                        replacements_done += 1

    print('----------------------------------------------------------------')
    print('')
    print('Se ha creado A -> L[A1] = L[A] - ε')
    display_grammar(grammar)
    print('')
    
    # Si el símbolo inicial produce ε, agregar un nuevo símbolo inicial
    if 'S' in epsilon_producing:
        grammar['S0'] = ['ε']
    
    # Eliminar cadenas vacías en las producciones
    for symbol, productions in grammar.items():
        grammar[symbol] = [production for production in productions if production != '']

def display_grammar(grammar):
    """
    Imprime la gramática en un formato legible.
    
    Args:
        grammar (dict): Gramática en forma de diccionario.
    """
    for symbol, productions in grammar.items():
        production_str = ' | '.join(productions)
        print(f"{symbol} -> {production_str}")

def main():
    # Reemplazar con el nombre del archivo
    file_name = 'gramatica1.txt'
    cfg = load_grammar(file_name)

    if cfg is not None:
        print('----------------------------------------------------------------')
        print('-----------------------Gramática Inicial------------------------')
        print('----------------------------------------------------------------')
        print('')

        display_grammar(cfg)
        print('')
        print('----------------------------------------------------------------')
        
        eliminate_epsilon_productions(cfg)
        
        print('----------------------------------------------------------------')
        print('-------------------------Resultado final------------------------')
        print('----------------------------------------------------------------')
        print('')

        display_grammar(cfg)
        print('')
        print('----------------------------------------------------------------')

if __name__ == "__main__":
    main()
