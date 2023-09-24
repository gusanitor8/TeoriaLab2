from graphviz import Graph

class Node:
    latest_id = 0
    tree_graph = Graph(format='png')

    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None

        Node.latest_id += 1
        self.id = Node.latest_id

    def printTree(self):
        Node.tree_graph.node(str(self.id), self.value)

        if self.left:
            Node.tree_graph.edge(str(self.id), str(self.left.id))
            self.left.printTree()
        
        if self.right:
            Node.tree_graph.edge(str(self.id), str(self.right.id))
            self.right.printTree()

    def renderTree(self):
        try:
            Node.tree_graph.render('example_tree', view=True)
        except Exception:
            pass

## File reader
def readfile(filename):
    with open(filename, 'r') as f:
        data = f.read().splitlines()
    return data    

## Regex Formater
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


#Gets Precedence of an operator
def getPrecedence(c):
    precedences = {
        '(': 4,
        ')': 4,
        '|': 0,
        '.': 2,
        '?': 3,
        '*': 3,
        '+': 3,
        '^': 1,
        '$': 1,
    }
    return precedences.get(c, 0)

#Converts infix to postfix
def infixToPostfix(formatedRegex):
    operators = ['|', '?', '+', '*', '^', '.', '(', ')']
    stack = []
    postfix = ""    
    isScapedChar = False

    for char in formatedRegex:
        if isScapedChar:
            postfix += char
            isScapedChar = False
            continue

        if char == '\\':
            stack.append(char)
            isScapedChar = True
            continue

        if char == '(':
            stack.append(char)    
        
        elif char in operators:
            peekedChar = stack[-1] if stack else None

            if char == ')':
                while peekedChar != '(':
                    postfix += stack.pop()
                    peekedChar = stack[-1] if stack else None
                stack.pop()
                continue

            peekedChar_pres = getPrecedence(peekedChar)
            char_pres = getPrecedence(char)

            if peekedChar == None:
                stack.append(char)     

            elif getPrecedence(peekedChar) >= getPrecedence(char) and (peekedChar != '('):
                postfix += stack.pop()
                stack.append(char)

            else:
                stack.append(char)
        else:
            postfix += char

    while len(stack) > 0:
        postfix += stack.pop()
            

    return postfix


def buildSyntaxTree(postfix_expr):
    stack = []
    operators = {'|':2 , '.':2, '?':1, '*':1, '+':1}

    for c in postfix_expr:
        if c not in operators:
            node = Node(c)
            stack.append(node)
        else:
            if operators[c] == 2:
                right_operand = stack.pop()    
                try:            
                    left_operand = stack.pop()
                except IndexError:
                    node = Node(c)
                    node.left = None
                    node.right = right_operand                    
                    stack.append(node)
                    continue
            
                node = Node(c)                
                node.right = right_operand
                node.left = left_operand
                stack.append(node)
                
            else:
                operand = stack.pop()
                node = Node(c)
                node.left = operand
                node.right = None
                stack.append(node)

                

    return stack.pop()


def getPostfixRegex():
    expressions = readfile('gramatica1.txt')
    
    postfixArr = []
    for regex in expressions:
        formatedRegex = formatRegEx(regex)
        postfix = infixToPostfix(formatedRegex)
        postfixArr.append(postfix)

    return postfixArr