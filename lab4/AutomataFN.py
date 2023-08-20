from lab4.AFNNode import AFNNode

class AFN(object):        

    def __init__(self, char=None):
        if char is not None:
            self.initial = AFNNode()
            self.terminal = AFNNode()
            self.initial.addTransition(char, self.terminal)
        else:
            self.initial = None
            self.terminal = None

    def eitherOr(self, afnA , afnB ):
        self.initial = AFNNode()
        self.initial.addTransition('𝜀', afnA.initial)
        self.initial.addTransition('𝜀', afnB.initial)

        self.terminal = AFNNode()
        afnA.terminal.addTransition('𝜀', self.terminal)
        afnB.terminal.addTransition('𝜀', self.terminal)
        

    def concatenate(self, afnA, afnB):
        self.initial = AFNNode()
        self.terminal = AFNNode()

        self.initial.addTransition('𝜀', afnA.initial)
        afnA.terminal.addTransition('𝜀', afnB.initial)
        afnB.terminal.addTransition('𝜀', self.terminal)
        

    def kleeneStar(self, afn):
        self.initial = AFNNode()
        self.terminal = AFNNode()

        self.initial.addTransition('𝜀', afn.initial)
        self.initial.addTransition('𝜀', self.terminal)
        afn.terminal.addTransition('𝜀', afn.initial)
        afn.terminal.addTransition('𝜀', self.terminal)
        

    def oneOrMore(self, afn):
        self.initial = AFNNode()
        self.terminal = AFNNode()

        self.initial.addTransition('𝜀', afn.initial)

        afn.terminal.addTransition('𝜀', afn.initial)
        afn.terminal.addTransition('𝜀', self.terminal)

    def zeroOrOne(self, afn):
        epsilon = AFN('𝜀')
        self.eitherOr(afn, epsilon)

      
