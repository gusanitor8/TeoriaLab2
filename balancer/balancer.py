def readfile(filename):
    with open(filename, 'r') as f:
        data = f.readlines()
    return data    

def check_regex(string):
    stack = []
    opening_brackets = {'(', '[', '{'}
    closing_brackets = {')', ']', '}'}
    bracket_pairs = {'(': ')', '[': ']', '{': '}'}
    is_balanced = True

    for char in string:
        if char in opening_brackets:
            stack.append(char)
        elif char in closing_brackets:
            try:
                opening = stack.pop()
            except IndexError:
                print("Stack vacio, es decir, no hay apertura para el cierre -> " + char)
                is_balanced = False
                break
                    
            if char != bracket_pairs[opening]:
                print("Cierre no coincide con apertura")
                is_balanced = False
                break
            else:
                print("Cierre coincide" + opening + " " + char)

    if is_balanced:
        print("Expresion balanceada:  " + string)
    else:
        print("Expresion no balanceada:  " + string)

    return is_balanced

def controller():
    regex = readfile('./balancer/regex.txt')
    for string in regex:
        check_regex(string)         

    
controller()