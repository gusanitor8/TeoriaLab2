from AFD.AFD import AFD


class AFDReducer:
    def __init__(self, afd: AFD):
        self.afd: AFD = afd
        self.alphabet = afd.alphabet
        self.afd_node_map = afd.states

        self.initial_group = self.initial_group()

    def initial_group(self):
        group = {1:[], 2:[]}

        for node in self.afd_node_map.values():
            if node.terminal:
                group[1].append(node)
            else:
                group[2].append(node)

        return group


    def reduce(self):
        self.make_block(self.initial_group)
        pass

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

