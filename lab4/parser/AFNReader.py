from AutomataFN import AFN
from AFNBuilder import AFNBuilder
from AFNNode import AFNNode

class AFNReader():
    def __init__(self, afn: AFN, string: str):
        self.afn = afn
        self.string = string
        

    def read(self):
        initial = [self.afn.initial]
        for char in self.string:
            temp = []
            for node in initial:
                eNodes = node.getEpsilonTransitions()

                for eNode in eNodes:
                    if char in eNode.transitions:
                        temp.append(eNode.transitions[char])
            initial = temp        

        final_nodes = set()
        for node in initial:
            nodes = node.getEpsilonTransitions()
            final_nodes = final_nodes.union(nodes)

        for node in final_nodes:
            if node == self.afn.terminal:
                return True
        return False


def testing():
    builder = AFNBuilder("at|c.")
    afn = builder.build()

    reader = AFNReader(afn, "ac")    
    print(reader.read())
    
testing()