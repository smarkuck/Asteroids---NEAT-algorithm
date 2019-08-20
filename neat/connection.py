import random

class Connecton:
    def __init__(self, inputNode, outputNode, weight, innovation):
        self.inputNode = inputNode
        self.outputNode = outputNode
        self.weight = weight
        self.innovation = innovation
        self.isEnabled = True

    def mutate(self):
        rnd = random.random()
        if rnd < 0.1: self.weight = random.random() * 2 - 1
        else: self.weight += random.gauss(0, 1) / 50.

    def clone(self, inputNode, outputNode):
        connection = Connecton(inputNode, outputNode, self.weight, self.innovation)
        connection.isEnabled = True
        return connection