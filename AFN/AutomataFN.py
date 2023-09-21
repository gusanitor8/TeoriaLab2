from AFN.AFNNode import AFNNode


class AFN(object):

    def __init__(self, char=None):
        self.node_map = None
        self.nodes_visited = set()

        if char is not None:
            self.initial = AFNNode()
            self.terminal = AFNNode()
            self.initial.addTransition(char, self.terminal)
        else:
            self.initial = None
            self.terminal = None

    def getEclosure(self, afn_node: AFNNode):
        """
        Guarda en una variable del objeto, self.nodes_visited, el e-closure del ultimo nodo que le fue pasado como parametro al
        metodo

        :param afn_node: nodo de tipo AFNNode
        :return: None
        """
        transitions = afn_node.transitions['𝜀']
        if not transitions:
            self.nodes_visited.add(afn_node)
            return

        trans_num = len(transitions)
        node_counter = 0

        for node in transitions:

            if node in self.nodes_visited:
                node_counter += 1

                if node_counter == (trans_num - 1):
                    self.nodes_visited.add(afn_node)

                continue

            if node_counter == (trans_num - 1):
                self.nodes_visited.add(afn_node)

            node_counter += 1

            self.getEclosure(node)

    def getNodesVisited(self):
        """
        Devuelve los nodos guardados en self.nodes_visited
        :return:
        """
        return self.nodes_visited

    def clearNodesVisited(self):
        """
        Borra todos los nodos guardados en self.nodes_visited
        :return: None
        """
        self.nodes_visited = set()

    def setNodeMap(self, node_map):
        self.node_map = node_map

    def eitherOr(self, afnA, afnB):
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
