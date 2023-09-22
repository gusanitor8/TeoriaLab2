from graphviz import Digraph


class AFDNode:
    last_id = 0
    afd_node_map = {}
    afd_graph = Digraph(format='png')

    def __init__(self, eclosure):
        self.id = AFDNode.last_id
        self.eclosure = eclosure
        self.transitions = {}

        self.initial = False
        self.terminal = False

        AFDNode.last_id += 1
        AFDNode.afd_node_map[self.id] = self

    def setTransition(self, key: str, afd_node):
        self.transitions[key] = afd_node
        AFDNode.afd_graph.edge(str(self.id), str(afd_node.id), label=key)

    def setInitial(self):
        self.initial = True
        AFDNode.afd_graph.edge('start', str(self.id))
        AFDNode.afd_graph.node('start', shape='point')

    def setTerminal(self):
        self.terminal = True
        AFDNode.afd_graph.node(str(self.id), shape='doublecircle')

    @classmethod
    def reset_graph(cls):
        cls.afd_graph = Digraph(format='png')

    def printAFD(self, filename:str):
        AFDNode.afd_graph.graph_attr['rankdir'] = 'LR'
        AFDNode.afd_graph.render(filename, directory="out2", view=True)
        AFDNode.reset_graph()
        self.reset()

    def reset(self):
        AFDNode.afd_node_map = {}
