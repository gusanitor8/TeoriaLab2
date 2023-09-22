from AFN.AutomataFN import AFN
from AFN.AFNNode import AFNNode
from AFD.AFDNode import AFDNode
from AFD.AFD import AFD
from typing import Dict


class AFDBuilder:
    def __init__(self, afn: AFN, alphabet: {str}):
        self.afn = afn
        self.afn_initial = afn.initial
        self.afn_terminal = afn.terminal

        self.afd_initial = None
        self.afd_terminals = set()

        self.afn_node_map: Dict[
            int, AFNNode] = afn.node_map  # mapa cuya llave es el id del AFNNode y el valor es el AFNNode
        self.afn_eclosure_map = {}  # este atributo tiene como llave el id de un nodo AFN y como valor sus nodos de e-closure
        self.alphabet = alphabet

        self.map_eclosureTransitions_id = {}
        self.map_id_node = {}
        self.afd_node_stack = []

        self.make_afn_eclosure_map()

    def build(self):
        # Tomamos el id del nodo inicial del AFN posteriormente obtenemos el eclosure del mismo
        initial_id = self.afn.initial.id
        initial_eclosure = self.afn_eclosure_map[initial_id]

        # Se crea y se agrega el nodo a los hash maps de nodos del objeto
        initial_afd_node = AFDNode(initial_eclosure)
        self.check_node_(initial_afd_node)
        self.afd_node_stack.append(initial_afd_node)
        self.add_afdNode(initial_afd_node)

        while len(self.afd_node_stack) > 0:
            afd_node: AFDNode = self.afd_node_stack.pop()
            afd_node_eclosure = afd_node.eclosure

            for char in self.alphabet:
                char_transitions_from_eclosure = self.get_nodes_from_eclosure(afd_node_eclosure, char)

                if not char_transitions_from_eclosure:
                    continue

                eclosure_transitions = self.get_eclosure_from_afn_node_set(char_transitions_from_eclosure)

                if frozenset(eclosure_transitions) not in self.map_eclosureTransitions_id:
                    new_afd_node = AFDNode(eclosure_transitions)
                    self.check_node_(new_afd_node)
                    self.afd_node_stack.append(new_afd_node)
                    self.add_afdNode(new_afd_node)
                    afd_node.setTransition(char, new_afd_node)
                else:
                    new_node_id = self.map_eclosureTransitions_id[frozenset(eclosure_transitions)]
                    new_afd_node = self.map_id_node[new_node_id]
                    afd_node.setTransition(char, new_afd_node)

        initial_afd_node.printAFD("test")
        return AFD(alphabet=self.alphabet, afd_node_map=self.map_id_node, initial=self.afd_initial,
                   terminals=self.afd_terminals)

    def check_node_(self, afd_node: AFDNode):
        eclosure_nodes = afd_node.eclosure

        if self.afn_initial in eclosure_nodes:
            afd_node.setInitial()
            self.afd_initial = afd_node

        if self.afn_terminal in eclosure_nodes:
            afd_node.setTerminal()
            self.afd_terminals.add(afd_node)

    def get_nodes_from_eclosure(self, afn_eclosure_nodes: {AFNNode}, char) -> {AFNNode}:
        """
        Dado un caracter y un conjunto de AFNNodes se determine a que conjunto de AFNNodes se puede
        llegar a partir de ese caracter

        :param afn_eclosure_nodes: recibe un conjunto de AFNNodes
        :param char: el caracter del que buscamos la transicion en el AFNNode
        :return: devuelve un conjunto de AFNNodes
        """
        set_of_afn_nodes = set()

        for node in afn_eclosure_nodes:
            try:
                if node.transitions[char]:
                    set_of_transitions = {node.transitions[char]}
                    set_of_transitions = frozenset(set_of_transitions)
                    set_of_afn_nodes = set_of_afn_nodes.union(set_of_transitions)
            except KeyError:
                print("El nodo AFN " + str(node.id) + "no tiene transiciones con " + char)
                pass
            except TypeError:
                set_of_transitions = set(node.transitions[char])
                set_of_transitions = frozenset(set_of_transitions)
                set_of_afn_nodes = set_of_afn_nodes.union(set_of_transitions)
                pass

        return set_of_afn_nodes

    def add_afdNode(self, afd_node: AFDNode):
        """
        Agrega el AFDNode a un hash map donde la llave es el conjunto de AFNNodes y el valor es el id del AFDNode,
        adicionalmente agrega el AFDNode a un hash map donde la llave es su id y el valor es el AFDNode

        :param eclosure_transitions: conjunto de ADNNodes
        :return: None
        """
        eclosure_transitions = afd_node.eclosure
        self.map_eclosureTransitions_id[frozenset(eclosure_transitions)] = afd_node.id
        self.map_id_node[afd_node.id] = afd_node

    def get_eclosure_from_afn_node_set(self, afn_node_set: {AFNNode}) -> {AFNNode}:
        """
        Dado un conjunto de nodos AFN se encuentran los nodos a los que se puede llegar
        a partir de la e-closure de cada uno de ellos

        :param afn_node_set: el conjunto de nodos AFN de los que queremos encontrar su e-closure
        :return: el conjunto de nodos AFN
        """

        afn_nodes: {AFNNode} = set()

        for node in afn_node_set:
            node_id = node.id
            eclosure: {AFNNode} = self.afn_eclosure_map[node_id]
            afn_nodes = afn_nodes.union(eclosure)

        return afn_nodes

    def make_afn_eclosure_map(self):
        """
        La funcion hace un hash map de el id de todos los AFNNodes y el valor son los
        AFNNodes de la e-closure de cada nodo

        :return: None
        """
        for node in self.afn_node_map.values():
            self.afn.getEclosure(node)
            node_eclosure: {AFNNode} = self.afn.getNodesVisited()
            self.afn.clearNodesVisited()
            self.afn_eclosure_map[node.id] = node_eclosure
