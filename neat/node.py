import math

class Node:
    def __init__(self, number):
        self.number = number
        self.input = 0
        self.output = 0
        self.outputConnections = []
        self.layer = 0

    def process(self):
        if self.layer == 0: self.output = self.input
        else: self.output = self.sigmoid(self.input)

        for connection in self.outputConnections:
            if connection.isEnabled:
                connection.outputNode.input += connection.weight * self.output

    def sigmoid(self, z):
        return 1 / (1 + math.exp(-z))

    def clone(self):
        node = Node(self.number)
        node.layer = self.layer
        return node

    def isConnectedTo(self, node):
        if node.layer == self.layer: return False

        if node.layer < self.layer:
            for connection in node.outputConnections:
                if connection.outputNode == self: return True
        else:
            for connection in self.outputConnections:
                if connection.outputNode == node: return True

        return False