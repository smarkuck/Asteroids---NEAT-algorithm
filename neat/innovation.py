class Innovation:
    def __init__(self, inputNode, outputNode, number, prevInnovationNumbers):
        self.inputNode = inputNode
        self.outputNode = outputNode
        self.number = number
        self.prevInnovationNumbers = list(prevInnovationNumbers)

    def matches(self, genome, inputNode, outputNode):
        if len(genome.connections) == len(self.prevInnovationNumbers):
            if inputNode.number == self.inputNode and outputNode.number == self.outputNode:
                for connection in genome.connections:
                    if connection.innovationNumber not in self.prevInnovationNumbers:
                        return False

                return True

        return False