from AFD.AFDNode import AFDNode


class AFD:
    def __init__(self, afd_node_map, alphabet: {str}, initial: AFDNode, terminals: {AFDNode}):
        self.initial_node: AFDNode = initial
        self.terminals: {AFDNode} = terminals

        self.alphabet: {str} = alphabet
        self.states = afd_node_map

    def setInitial(self, initial_node: AFDNode):
        self.initial_node = initial_node

    def setTerminals(self, terminals: {AFDNode}):
        self.terminals = terminals
