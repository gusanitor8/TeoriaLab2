def readfile(filename):
    with open(filename, 'r') as f:
        data = f.read().splitlines()
    return data    

def getPrecedence(c):
    precedences = {
        '(': 1,
        '|': 2,
        '.': 3,
        '?': 4,
        '*': 4,
        '+': 4,
        '^': 5,
    }
    return precedences.get(c, 0)

def formatRegEx(regex):
    allOperators = ['|', '?', '+', '*', '^']
    binaryOperators = ['^', '|']
    res = ""

    for i in range(len(regex)):
        c1 = regex[i]

        if i + 1 < len(regex):
            c2 = regex[i + 1]

            res += c1

            if c1 != '(' and c2 != ')' and c2 not in allOperators and c1 not in binaryOperators:
                res += '.'

    res += regex[-1]

    return res


def formatRegEx(regex):
    allOperators = ['|', '?', '+', '*', '^']
    binaryOperators = ['^', '|']
    res = ""

    for i in range(len(regex)):
        c1 = regex[i]

        if i + 1 < len(regex):
            c2 = regex[i + 1]
            res += c1

            isScapedChar = (c1 == '\\')
            if isScapedChar:
                res += c2
                i += 1

            if c1 != '(' and c2 != ')' and c2 not in allOperators and c1 not in binaryOperators:
                res += '.'

    res += regex[-1]

    return res

def is_operator(c):
    return c in {'|', '?', '+', '*', '^'}

def infixToPostfix(regex):
    postfix = ""
    stack = []
    formattedRegEx = formatRegEx(regex)

    for c in formattedRegEx:
        if c == '(':
            stack.append(c)
        elif c == ')':
            while stack and stack[-1] != '(':
                postfix += stack.pop()

            # Check if there's a matching '(' in the stack
            if stack and stack[-1] == '(':
                stack.pop()  # Pop the '('
            else:
                raise ValueError("Mismatched parentheses in the regular expression.")
        elif is_operator(c):
            while stack:
                peekedChar = stack[-1]
                if is_operator(peekedChar):
                    peekedCharPrecedence = getPrecedence(peekedChar)
                    currentCharPrecedence = getPrecedence(c)

                    if peekedCharPrecedence >= currentCharPrecedence:
                        postfix += stack.pop()
                    else:
                        break
                else:
                    break

            stack.append(c)
        else:  # Operand (literal or character class)
            postfix += c
            while stack and stack[-1] not in {'(', '|'}:
                # Implicit concatenation
                postfix += stack.pop()

    while stack:
        postfix += stack.pop()

    return postfix


# Example usage:
regex = "(\*a|b)c*"
postfix_expression = infixToPostfix(regex)
print(postfix_expression)  # Output: "ab|c*."

# def controller():
#     regex = readfile('./shuntingYard/regex.txt')
#     for string in regex:
#         print(infixToPostfix(string))

# controller()
