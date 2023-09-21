from AFN.AutomataFN import AFN
from AFN.AFNNode import AFNNode
from AFD.AFDNode import AFDNode
from typing import Dict


class AFDBuilder:
    def __init__(self, afn: AFN, alphabet: {str}):
        self.afn = afn
        self.afn_node_map: Dict[
            int, AFNNode] = afn.node_map  # mapa cuya llave es el id del AFNNode y el valor es el AFNNode
        self.afn_eclosure_map = {}
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
        self.afd_node_stack.append(initial_afd_node)
        self.add_afdNode(initial_afd_node)

        while len(self.afd_node_stack) > 0:
            afd_node : AFDNode = self.afd_node_stack.pop()
            afd_node_eclosure = afd_node.eclosure

            for char in self.alphabet:
                char_transitions_from_eclosure = self.get_nodes_from_eclosure(afd_node_eclosure, char)

                if not char_transitions_from_eclosure:
                    continue

                if frozenset(char_transitions_from_eclosure) not in self.map_eclosureTransitions_id:
                    next_afd_node = AFDNode(char_transitions_from_eclosure)
                    self.add_afdNode(next_afd_node)
                    self.afd_node_stack.append(next_afd_node)
                    afd_node.setTransition(char,next_afd_node)
                else:
                    next_afd_node_id = self.map_eclosureTransitions_id[frozenset(char_transitions_from_eclosure)]
                    next_afd_node : AFDNode = self.map_id_node[next_afd_node_id]
                    afd_node.setTransition(char, next_afd_node)

        initial_afd_node.printAFD("test")





    def get_nodes_from_eclosure(self, afn_eclosure_nodes: {AFNNode}, char) -> {AFNNode}:
        """
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
