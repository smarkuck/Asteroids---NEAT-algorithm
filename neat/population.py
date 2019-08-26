import math

from genome import Genome
from species import Species
from innovation_history import InnovationHistory

class Population:
    def __init__(self, size):
        self.genomes = []
        self.champion = None
        self.bestFitness = 0
        self.generation = 0
        self.species = []
        self.innovationHistory = InnovationHistory(32 * 4)

        for i in range(size):
            self.genomes.append(Genome(32, 4))
            self.genomes[i].connectNodes()

    def speciate(self):
        for s in self.species: del s.genomes[:]

        for genome in self.genomes:
            speciesFound = False
            for s in self.species:
                if s.belongsTo(genome):
                    s.add(genome)
                    speciesFound = True
                    break

            if not speciesFound: self.species.append(Species(genome))

    def sortSpecies(self):
        for s in self.species:
            s.sortSpecies()

        for i in range(len(self.species) - 1):
            maxIndex = i
            for j in range(i + 1, len(self.species)):
                if self.species[j].bestFitness > self.species[maxIndex].bestFitness:
                    maxIndex = j
            tmp = self.species[i]
            self.species[i] = self.species[maxIndex]
            self.species[maxIndex] = tmp

    def cullSpecies(self):
        for s in self.species:
            s.cull()
            s.fitnessSharing()
            s.setAverage()

    def setChampion(self):
        candidate = self.species[0].champion
        if candidate.fitness > self.bestFitness:
            self.bestFitness = candidate.fitness
            self.champion = candidate.clone()

    def killStaleSpecies(self):
        species = [self.species[0]]
        for i in range(1, len(self.species)):
            if self.species[i].staleness < 15:
                species.append(self.species[i])
        self.species = species

    def getAverageFitnessSum(self):
        averageSum = 0
        for s in self.species: averageSum += s.averageFitness
        return averageSum

    def killBadSpecies(self):
        averageSum = self.getAverageFitnessSum()

        species = [self.species[0]]
        for i in range(1, len(self.species)):
            if self.species[i].averageFitness/averageSum * len(self.genomes) >= 1:
                species.append(self.species[i])
        self.species = species

    def naturalSelection(self):
        self.speciate()
        self.sortSpecies()
        self.cullSpecies()
        self.setChampion()
        self.killStaleSpecies()
        self.killBadSpecies()

        averageSum = self.getAverageFitnessSum()
        nextGeneration = []
        for s in self.species:
            nextGeneration.append(s.champion.clone())
            numberOfChildren = int(math.floor(s.averageFitness/averageSum * len(self.genomes)) - 1)
            for i in range(numberOfChildren):
                nextGeneration.append(s.createGenome(self.innovationHistory))

        while len(nextGeneration) < len(self.genomes):
            nextGeneration.append(self.species[0].createGenome(self.innovationHistory))

        self.genomes = nextGeneration
        self.generation += 1

        print "champion data - nodes: %s, connections: %s, fitness: %s" % (len(self.champion.nodes), len(self.champion.connections), self.bestFitness)
        print "genomes in species:"
        for s in self.species: print len(s.genomes)
        print "generation: %s, mutations: %s, species: %s" %\
              (self.generation, len(self.innovationHistory.innovations), len(self.species))