class Innovation:
    def __init__(self, inputNode, outputNode, number, prevInnovationNumbers):
        self.inputNode = inputNode
        self.outputNode = outputNode
        self.number = number
        self.prevInnovationNumbers = prevInnovationNumbers.copy()