import random
from node import Node
from connection import Connection
from innovation import Innovation

class Genome:
    def __init__(self, inputSize, outputSize):
        self.inputSize = inputSize
        self.outputSize = outputSize
        self.layers = 2
        self.nextNodeNumber = 0
        self.nodes = []
        self.connections = []
        self.feedforwardNodeOrder = []
        self.fitness = 0

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

    def mutate(self, innovationHistory):
        rnd = random.random()
        if rnd < 0.8:
            for connection in self.connections:
                connection.mutate()

        rnd = random.random()
        if rnd < 0.05:
            self.addConnection(innovationHistory)

        rnd = random.random()
        if rnd < 0.03:
            self.addNode(innovationHistory)

    def addConnection(self, innovationHistory):
        if self.fullyConnected():
            print "fully connected"
            return

        randomNode1 = self.nodes[random.randrange(0, len(self.nodes))]
        randomNode2 = self.nodes[random.randrange(0, len(self.nodes))]

        while randomNode1.layer == randomNode2.layer or randomNode1.isConnectedTo(randomNode2):
            randomNode1 = self.nodes[random.randrange(0, len(self.nodes))]
            randomNode2 = self.nodes[random.randrange(0, len(self.nodes))]

        if randomNode1.layer > randomNode2.layer:
            tmp = randomNode1
            randomNode1 = randomNode2
            randomNode2 = tmp

        connectionInnovationNumber = self.getInnovationNumber(innovationHistory, randomNode1, randomNode2)
        self.connections.append(Connection(randomNode1, randomNode2, random.random() * 2 - 1, connectionInnovationNumber))
        self.connectNodes()

    def fullyConnected(self):
        maxConnections = 0
        nodesInLayers = [0] * self.layers

        for node in self.nodes:
            nodesInLayers[node.layer] += 1

        for i in range(self.layers - 1):
            nodesInFront = 0
            for j in range(i + 1, self.layers):
                nodesInFront += nodesInLayers[j]

            maxConnections += nodesInLayers[i] * nodesInFront

        return True if maxConnections == len(self.connections) else False

    def getInnovationNumber(self, innovationHistory, inputNode, outputNode):
        isNew = True
        connectionInnovationNumber = innovationHistory.nextInnovationNumber

        for innovation in innovationHistory.innovations:
            if innovation.matches(self, inputNode, outputNode):
                isNew = False
                connectionInnovationNumber = innovation.number
                break

        if isNew:
            innovationNumbers = []
            for connection in self.connections:
                innovationNumbers.append(connection.innovationNumber)

            innovationHistory.innovations.append(Innovation(inputNode.number, outputNode.number, connectionInnovationNumber, innovationNumbers))
            innovationHistory.nextInnovationNumber += 1

        return connectionInnovationNumber

    def addNode(self, innovationHistory):
        randomConnection = self.connections[random.randrange(0, len(self.connections))]
        randomConnection.isEnabled = False

        newNodeNumber = self.nextNodeNumber
        newNode = Node(newNodeNumber)
        self.nodes.append(newNode)
        self.nextNodeNumber += 1

        connectionInnovationNumber = self.getInnovationNumber(innovationHistory, randomConnection.inputNode, newNode)
        self.connections.append(Connection(randomConnection.inputNode, newNode, 1, connectionInnovationNumber))

        connectionInnovationNumber = self.getInnovationNumber(innovationHistory, newNode, randomConnection.outputNode)
        self.connections.append(Connection(newNode, randomConnection.outputNode, randomConnection.weight, connectionInnovationNumber))
        newNode.layer = randomConnection.inputNode.layer + 1

        if newNode.layer == randomConnection.outputNode.layer:
            for i in range(len(self.nodes) - 1):
                if self.nodes[i].layer >= newNode.layer:
                    self.nodes[i].layer += 1
            self.layers += 1

        self.connectNodes()

    def findConnection(self, genome, innovationNumber):
        for connection in genome.connections:
            if connection.innovationNumber == innovationNumber:
                return connection
        return None

    def getNode(self, number):
        for node in self.nodes:
            if node.number == number:
                return node
        return None

    def crossover(self, genome):
        child = Genome(self.inputSize, self.outputSize)
        del child.nodes[:]
        del child.connections[:]
        del child.feedforwardNodeOrder[:]
        child.layers = self.layers
        child.nextNodeNumber = self.nextNodeNumber
        child.fitness = 0

        childConnections = []
        isEnabled = []

        for connection in self.connections:
            setEnabled = True

            secondParentConnection = self.findConnection(genome, connection.innovationNumber)
            if secondParentConnection is not None:
                if not connection.isEnabled or not secondParentConnection.isEnabled:
                    if random.random() < 0.75:
                        setEnabled = False

                if random.random() < 0.5:
                    childConnections.append(connection)
                else:
                    childConnections.append(secondParentConnection)

            else:
                childConnections.append(connection)
                setEnabled = connection.isEnabled

            isEnabled.append(setEnabled)

        for node in self.nodes:
            child.nodes.append(node.clone())

        for i in range(len(childConnections)):
            child.connections.append(childConnections[i].clone(
                child.getNode(childConnections[i].inputNode.number),
                child.getNode(childConnections[i].outputNode.number)))
            child.connections[i].isEnabled = isEnabled[i]

        child.connectNodes()
        return child

    def clone(self):
        clone = Genome(self.inputSize, self.outputSize)
        del clone.nodes[:]
        del clone.connections[:]
        del clone.feedforwardNodeOrder[:]

        for node in self.nodes:
            clone.nodes.append(node.clone())

        for connection in self.connections:
            clone.connections.append(connection.clone(clone.getNode(connection.inputNode.number), clone.getNode(connection.outputNode.number)))

        clone.layers = self.layers
        clone.nextNodeNumber = self.nextNodeNumber
        clone.fitness = 0

        clone.connectNodes()

        return clone