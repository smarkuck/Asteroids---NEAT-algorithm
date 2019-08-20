from node import Node
from connection import Connection
import random

class Genome:
    def __init__(self, inputSize, outputSize):
        self.inputSize = inputSize
        self.outputSize = outputSize
        self.layers = 2
        self.nextNodeNumber = 0
        self.nodes = []
        self.connections = []
        self.feedforwardNodeOrder = []

        for i in range(inputSize):
            node = Node(self.nextNodeNumber)
            self.nodes.append(node)
            self.nextNodeNumber += 1

        for i in range(outputSize):
            node = Node(self.nextNodeNumber)
            node.layer = 1
            self.nodes.append(node)
            self.nextNodeNumber += 1

        connectionNumber = 0
        for i in range(inputSize):
            for j in range(outputSize):
                rnd = random.random() * 2 - 1
                self.connections.append(
                    Connection(self.nodes[i], self.nodes[self.inputSize + j], rnd, connectionNumber))
                connectionNumber += 1

    def connectNodes(self):
        for node in self.nodes: del node.outputConnections[:]
        for connection in self.connections:
            connection.inputNode.outputConnections.append(connection)
        self.createFeedforwardNodeOrder()

    def createFeedforwardNodeOrder(self):
        del self.feedforwardNodeOrder[:]
        for i in range(self.layers):
            for node in self.nodes:
                if node.layer == i: self.feedforwardNodeOrder.append(node)

    def feedforward(self, input):
        for i in range(self.inputSize):
            self.nodes[i].input = input[i]

        for node in self.feedforwardNodeOrder:
            node.process()

        output = []
        for i in range(self.outputSize):
            output.append(self.nodes[i + self.inputSize].output)

        for node in self.nodes:
            node.input = 0

        return output