from AFD.AFD import AFD
from AFD.AFDNode import AFDNode


class AFDReducer:
    def __init__(self, afd: AFD):
        self.afd: AFD = afd
        self.alphabet = afd.alphabet
        self.afd_node_map = afd.states

        self.reduced_initial = None
        self.reduced_terminals = set()

        self.initial_group = self.create_initial_group()
        self.node_block_map = None

    def create_initial_group(self):
        group = {1: [], 2: []}

        for node in self.afd_node_map.values():
            if node.terminal:
                group[1].append(node)
            else:
                group[2].append(node)

        return group

    def reduce(self):
        self.make_block(self.initial_group)
        self.node_block_map = self.create_node_block_map()
        reduced_afd = self.create_afd()
        reduced_afd.initial_node.printAFD("test_reduced")



    def reformat_block(self, block):
        """
        Este metodo toma el bloque que devuelve la funcion make block y cambia las llaves que son tuplas
        por numeros enteros para que sea mas facil de manejar

        :return: un hashmap con llaves enteras
        """

        new_dict = {}
        counter = 0

        for value in block.values():
            new_dict[counter] = value
            counter += 1

        return new_dict

    def make_block(self, group):
        block = {}

        for node_key in self.afd_node_map:
            node = self.afd_node_map[node_key]
            tupla = []
            for key in group:
                subgroup = group[key]
                for char in self.alphabet:
                    if node.transitions[char] in subgroup:
                        num = key
                        tupla.append(num)

            tupla = tuple(tupla)

            try:
                block[tupla].append(node)
            except KeyError:
                block[tupla] = [node]

        reformated_block = self.reformat_block(block)

        if not reformated_block == self.initial_group:
            self.initial_group = reformated_block
            self.make_block(reformated_block)

    def create_node_block_map(self):
        """
        Genera un hash map donde la llave es un nodo y el valor es el gupo al que pertenece

        :return:
        """
        node_block_map = {}

        for subgroup_key in self.initial_group:
            subgroup = self.initial_group[subgroup_key]

            for node in subgroup:
                node_block_map[node] = subgroup_key

        return node_block_map

    def create_afd(self):
        afd_map = {}

        for subgroup_key in self.initial_group:
            subgroup = self.initial_group[subgroup_key]
            afd_node = AFDNode(subgroup)
            afd_map[subgroup_key] = afd_node

            # Revisa si es nodo inicial
            if self.afd.initial_node in subgroup:
                self.reduced_initial = afd_node
                afd_node.setInitial()

            # Revisa si el nodo es terminal
            for terminal in self.afd.terminals:
                if terminal in subgroup:
                    self.reduced_terminals.add(afd_node)
                    afd_node.setTerminal()

        for subgroup_key in afd_map:
            this_node = afd_map[subgroup_key]

            subgroup = self.initial_group[subgroup_key]
            iterator = iter(subgroup)
            first_afd_node: AFDNode = next(iterator)


            for char in self.alphabet:
                transition_afd = first_afd_node.transitions[char]

                block_num = self.node_block_map[transition_afd]
                new_afd = afd_map[block_num]

                this_node.setTransition(char, new_afd)

        reduced_afd = AFD(afd_map, self.alphabet, self.reduced_initial, self.reduced_terminals)
        return reduced_afd



