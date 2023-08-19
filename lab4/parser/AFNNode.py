class AFNNode():
    last_id = 0    

    def __init__(self):
        self.id = AFNNode.last_id
        AFNNode.last_id += 1
        self.transitions = {'𝜀': []}

    def addTransition(self, char, node):
        if char == '𝜀':
            self.transitions['𝜀'].append(node)
            
        else:            
            self.transitions[char] = node
        


