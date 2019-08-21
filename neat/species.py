class Species:
    def __init__(self, firstGenome, fitness):
        self.EXCESS_COEFF = 1.5
        self.WEIGHT_DIFF_COEFF = 0.8
        self.COMPATIBILITY_THRESHOLD = 1.0

        self.speciesRepresentant = firstGenome
        self.genomes = [firstGenome]
        self.bestFitness = fitness
        self.averageFitness = 0
        self.staleness = 0

    def add(self, genome):
        self.genomes.append(genome)

    def belongsTo(self, genome):
        excessAndDisjoint = self.getExcessDisjoint(genome, self.speciesRepresentant)
        averageWeightDiff = self.averageWeightDiff(genome, self.speciesRepresentant)

        compatibility = (self.excessCoeff * excessAndDisjoint) + (self.weightDiffCoeff * averageWeightDiff)
        return compatibility < self.COMPATIBILITY_THRESHOLD

    def getExcessDisjoint(self, genome1, genome2):
        matching = 0
        for c1 in genome1.connections:
            for c2 in genome2.connections:
                if c1.innovationNumber == c2.innovationNumber:
                    matching += 1
                    break
        return len(genome1.connections) + len(genome2.connections) - 2 * matching

    def averageWeightDiff(self, genome1, genome2):
        matching = 0
        totalDiff = 0
        for c1 in genome1.connections:
            for c2 in genome2.connections:
                if c1.innovationNumber == c2.innovationNumber:
                    matching += 1
                    totalDiff += abs(c1.weight - c2.weight)
                    break
        if matching == 0: return 100
        return totalDiff/matching
    