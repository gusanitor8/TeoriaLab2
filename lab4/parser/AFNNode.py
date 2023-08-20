from graphviz import Digraph

class AFNNode():
    last_id = 0        
    afn_graph = Digraph(format='png')

    def __init__(self):
        self.id = AFNNode.last_id
        AFNNode.last_id += 1
        self.transitions = {'𝜀': []}
        AFNNode.afn_graph.node(str(self.id), str(self.id))
        self.isInitial = False
        self.isTerminal = False

    def setTerminal(self):
        self.isTerminal = True
        AFNNode.afn_graph.node(str(self.id), shape='doublecircle')

    def setInitial(self):
        self.isInitial = True        
        AFNNode.afn_graph.edge('start', str(self.id))
        AFNNode.afn_graph.node('start', shape='point')


    def addTransition(self, char, node):
        if char == '𝜀':
            self.transitions['𝜀'].append(node)
            AFNNode.afn_graph.edge(str(self.id), str(node.id), label='𝜀')
            #print("(yo)" + str(self.id) + '--'+ '𝜀' +'-->' + str(node.id))
            
        else:            
            self.transitions[char] = node
            AFNNode.afn_graph.edge(str(self.id), str(node.id), label=char)
            #print("(yo)" + str(self.id) + '--'+ char +'-->' + str(node.id))
        
    def getEpsilonTransitions(self):
        if self.transitions['𝜀']:
            nodes = set()
            for node in self.transitions['𝜀']:
                eTrans = node.getEpsilonTransitions()
                nodes = nodes.union(eTrans)
            return nodes
        else:
            return {self}

    def printAFN(self):
        AFNNode.afn_graph.graph_attr['rankdir'] = 'LR'
        AFNNode.afn_graph.render('afn', view=True)