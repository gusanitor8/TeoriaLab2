import AFNNode
import AutomataFN as automata

class AFNBuilder():
    def __init__(self, postfixRegex : str):
        self.initial = None
        self.Terminal = None
        self.postfixRegex = postfixRegex
        
        self.unaryOperators = ['?', '+', '*']
        self.binaryOperators = ['|', "."]

        self.operatorFunctions = {
            "|": self.eitherOr,
            "." : self.concatenate,
            "*" : self.kleeneStar,
            "+" : self.oneOrMore,
            "?" : self.zeroOrOne
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


    def eitherOr(self, afnA, afnB):
        afn = automata.AFN()
        afn.eitherOr(afnA, afnB)
        self.stack.append(afn)

    def concatenate(self, afnA, afnB):
        afn = automata.AFN()
        afn.concatenate(afnA, afnB)
        self.stack.append(afn)

    def kleeneStar(self, afn):
        afn = automata.AFN()
        afn.kleeneStar(afn)
        self.stack.append(afn)

    def oneOrMore(self, afn):
        afn = automata.AFN()
        afn.oneOrMore(afn)
        self.stack.append(afn)

    def zeroOrOne(self, afn):
        afn = automata.AFN()
        afn.zeroOrOne(afn)
        self.stack.append(afn)
            

afnBuilder = AFNBuilder("at|c.")
afnBuilder.build()