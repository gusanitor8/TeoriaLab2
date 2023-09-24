from AFN.AutomataFN import AFN
from AFN.AFNNode import AFNNode


# from AFNBuilder import AFNBuilder
# from AFNNode import AFNNode

class AFNReader():
    def __init__(self, afn: AFN):
        self.afn = afn
        self.initial = afn.initial
        self.terminal = afn.terminal

        self.afn_node_map = afn.node_map
        self.afn_eclosure_map = {}


    def read(self, cadena: str):
        self.make_eclosure_map()

        next_nodes = self.afn_eclosure_map[self.initial]
        for char in cadena:
            next_nodes_char = set()
            for node in next_nodes:
                try:
                    if node.transitions[char]:
                        next_nodes_char.add(node.transitions[char])

                except KeyError:
                    continue

            new_next_nodes = set()

            for node in next_nodes_char:
                node_eclosure = self.afn_eclosure_map[node]
                new_next_nodes = new_next_nodes.union(node_eclosure)

            next_nodes = new_next_nodes

        if self.terminal in next_nodes:
            return True
        else:
            return False

    def make_eclosure_map(self):
        for node in self.afn_node_map.values():
            self.afn.getEclosure(node)
            node_eclosure: {AFNNode} = self.afn.getNodesVisited()
            node_eclosure.add(node)
            self.afn.clearNodesVisited()
            self.afn_eclosure_map[node] = node_eclosure
