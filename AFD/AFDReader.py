from AFD.AFD import AFD


class AFDReader:

    def __init__(self, afd: AFD):
        self.afd: AFD = afd

    def readAFD(self, expression: str):
        next_node = self.afd.initial_node

        try:
            for char in expression:
                next_node = next_node.transitions[char]

            return next_node in self.afd.terminals

        except KeyError:
            return False
