import random

class Connection:
    def __init__(self, inputNode, outputNode, weight, innovationNumber):
        self.inputNode = inputNode
        self.outputNode = outputNode
        self.weight = weight
        self.innovationNumber = innovationNumber
        self.isEnabled = True

    def mutate(self):
        rnd = random.random()
        if rnd < 0.1: self.weight = random.random() * 2 - 1
        else: self.weight += random.gauss(0, 1) / 50.

    def clone(self, inputNode, outputNode):
        connection = Connection(inputNode, outputNode, self.weight, self.innovationNumber)
        connection.isEnabled = True
        return connection