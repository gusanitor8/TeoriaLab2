from AFN.AFNNode import AFNNode
import AFN.AutomataFN as automata


class AFNBuilder():
    def __init__(self, postfixRegex: str):
        self.postfixRegex = postfixRegex

        self.unaryOperators = ['?', '+', '*']
        self.binaryOperators = ['|', "."]
        self.alphabet = set()

        self.operatorFunctions = {
            "|": self.eitherOr,
            ".": self.concatenate,
            "*": self.kleeneStar,
            "+": self.oneOrMore,
            "?": self.zeroOrOne
        }
        self.stack = []

    def build(self):
        for char in self.postfixRegex:
            if char in self.binaryOperators:
                afnA = self.stack.pop()
                afnB = self.stack.pop()
                self.operatorFunctions[char](afnA, afnB)

            elif char in self.unaryOperators:
                afn = self.stack.pop()
                self.operatorFunctions[char](afn)

            else:
                self.stack.append(automata.AFN(char))
                if char != '𝜀':
                    self.alphabet.add(char)

        afn = self.stack[-1]
        afn.terminal.setTerminal()
        afn.initial.setInitial()
        afn.setNodeMap(AFNNode.node_map)
        return self.stack.pop()





    def eitherOr(self, afnA, afnB):
        afn = automata.AFN()
        afn.eitherOr(afnA, afnB)
        self.stack.append(afn)

    def concatenate(self, afnA, afnB):
        afn = automata.AFN()
        afn.concatenate(afnB, afnA)
        self.stack.append(afn)

    def kleeneStar(self, afnA):
        afn = automata.AFN()
        afn.kleeneStar(afnA)
        self.stack.append(afn)

    def oneOrMore(self, afnA):
        afn = automata.AFN()
        afn.oneOrMore(afnA)
        self.stack.append(afn)

    def zeroOrOne(self, afnA):
        afn = automata.AFN()
        afn.zeroOrOne(afnA)
        self.stack.append(afn)
