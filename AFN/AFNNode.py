from graphviz import Digraph

class AFNNode():
    last_id = 0        
    afn_graph = Digraph(format='png')
    node_map = {}

    def __init__(self):
        self.id = AFNNode.last_id
        self.transitions = {'𝜀': []}
        self.isInitial = False
        self.isTerminal = False

        AFNNode.last_id += 1
        AFNNode.afn_graph.node(str(self.id), str(self.id))
        AFNNode.node_map[self.id] = self  # se agrega al listado de nodos global

    def reset(self):
        AFNNode.last_id = 0

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

    def getEclosure(self):
        """
        La funcion devuelve un conjunto de los nodos a los que se puede llegar a
        través de un solo paso de epsilon

        :return: Devuelve un conjunto de AFNNodes
        """
        if self.transitions['𝜀']:
            eclosure_transitions = self.transitions['𝜀'].copy()
            eclosure_transitions.append(self)
            eclosure_transitions = set(eclosure_transitions)

            return eclosure_transitions
        else:
            return {self}

    @classmethod
    def reset_graph(cls):
        cls.afn_graph = Digraph(format='png')

    def printAFN(self, filename:str):
        AFNNode.afn_graph.graph_attr['rankdir'] = 'LR'
        AFNNode.afn_graph.render(filename, directory="out", view=True)
        AFNNode.reset_graph()
        self.reset()
