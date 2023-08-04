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
        Node.tree_graph.render('example_tree', view=True)

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
        '|': 3,
        '.': 2,
        '?': 1,
        '*': 1,
        '+': 1,
        '^': 0,
    }
    return precedences.get(c, 0)

#Converts infix to postfix
def infixToPostfix(formatedRegex):
    operators = ['|', '?', '+', '*', '^', '.', '(', ')']
    stack = []
    postfix = ""

    for char in formatedRegex:
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

            if peekedChar == None:
                stack.append(char)            
            
            elif getPrecedence(peekedChar) >= getPrecedence(char) and not '(':
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
    operators = {'|', '.', '?', '*', '+'}

    for c in postfix_expr:
        if c not in operators:
            node = Node(c)
            stack.append(node)
        else:
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
            node.left = left_operand
            node.right = right_operand
            stack.append(node)

    return stack.pop()

def main():
    formatedRegex = formatRegEx('(a*|b)c')
    postfix = infixToPostfix(formatedRegex)
    print(postfix)

    tree = buildSyntaxTree(postfix)
    tree.printTree()
    tree.renderTree()
    print(tree.value)

main()


            


        
    