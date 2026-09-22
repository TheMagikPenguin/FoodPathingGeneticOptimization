from organism import *
import random as rand

class Generation:
    #Initialization of a generation. It's really just a list of organisms
    def  __init__(self, spawn, amntOfOrganisms : int, mutateRate):
        self.organisms = []
        self.totalFitness = 0
        self.initialX = spawn[0]
        self.initialY = spawn[1]
        self.amntOfOrganisms = amntOfOrganisms
        self.mutateRate = mutateRate

    #If it is the first generation or came from a generation that didnt find anything it'll run this random function that just makes many new organisms
    def randGeneration(self, geneLength):
        for i in range(self.amntOfOrganisms):
            n = Organism(i+1, self.initialX, self.initialY, geneLength)
            n.generateNewDirections()
            self.organisms.append(n)

    def runGeneration(self, foods):
        for o in self.organisms:
            o.organismMovement(foods)
        self.fitnessSummation()

    #Mass mutates a generation when theyre being made
    def mutateGeneration(self, mutateRate):
        for o in self.organisms:
            o.mutate(mutateRate)

    #Sums the total fitness of a generation
    def fitnessSummation(self):
        self.totalFitness = 0
        for o in self.organisms:
            self.totalFitness += o.fitness
        return self.totalFitness

    #Chooses organisms as parents based on a probability of (food found by organims)/(food found by the whole generation of organisms)
    def fitnessProportionateSelection(self):
        tf = self.totalFitness
        if tf > 0:
            selectionChances = []
            for o in self.organisms:
                chance = o.fitness/tf
                selectionChances.append(chance)
            parent1 = rand.choices(self.organisms, weights = selectionChances, cum_weights = None, k = 1)[0]
            if parent1.fitness == tf:
                return parent1, parent1
            parent2 = parent1
            while parent2 == parent1:
                parent2 = rand.choices(self.organisms, weights = selectionChances, cum_weights = None, k = 1)[0]
            return parent1, parent2
        else:
            return
    
    #The part where genes are crossed
    def twoPointCrossover(self, geneLength):
        nextGen = Generation((self.initialX, self.initialY), self.amntOfOrganisms, self.mutateRate)
        if self.totalFitness != 0:
            #This happens if there is an even number of organisms in a generation
            if len(self.organisms) % 2 == 0: 
                for c in range(len(self.organisms)//2):
                    #Chooses parents
                    parent1, parent2 = self.fitnessProportionateSelection()
                    offspring1 = Organism((2*c) + 1, self.initialX, self.initialY, geneLength)
                    offspring2 = Organism((2*c) + 2, self.initialX, self.initialY, geneLength)
                    choosingBoolean = True
                    while choosingBoolean == True:
                        cPoint1 = rand.randint(0, len(parent1.directions[0]) - 1)
                        cPoint2 = rand.randint(0, len(parent1.directions[0]) - 1)
                        if abs(cPoint1 - cPoint2) > 1:
                            if cPoint1 > cPoint2:
                                cPoint1, cPoint2 = cPoint2, cPoint1
                                choosingBoolean = False
                    #First chunk of the offsprings' genes
                    for g in range(0, cPoint1):
                        offspring1.directions[0].append(parent1.directions[0][g])
                        offspring1.directions[1].append(parent1.directions[1][g])
                        offspring2.directions[0].append(parent2.directions[0][g])
                        offspring2.directions[1].append(parent2.directions[1][g])
                    #Second chunk of the offsprings' genes
                    for g in range(cPoint1, cPoint2):
                        offspring1.directions[0].append(parent2.directions[0][g])
                        offspring1.directions[1].append(parent2.directions[1][g])
                        offspring2.directions[0].append(parent1.directions[0][g])
                        offspring2.directions[1].append(parent1.directions[1][g])
                    #Third chunk of the offsprings' genes
                    for g in range(cPoint2, len(parent1.directions[0])):
                        offspring1.directions[0].append(parent1.directions[0][g])
                        offspring1.directions[1].append(parent1.directions[1][g])
                        offspring2.directions[0].append(parent2.directions[0][g])
                        offspring2.directions[1].append(parent2.directions[1][g])
                    nextGen.organisms.append(offspring1)
                    nextGen.organisms.append(offspring2)
            else:
                #This is the same as before but for an odd number of organisms where the final organism is produced asexually from the most fit organism in the previous generation
                for c in range(len(self.organisms)//2):
                    parent1, parent2 = self.fitnessProportionateSelection()
                    offspring1 = Organism((2*c) + 1, self.initialX, self.initialY, geneLength)
                    offspring2 = Organism((2*c) + 2, self.initialX, self.initialY, geneLength)
                    choosingBoolean = True
                    while choosingBoolean == True:
                        cPoint1 = rand.randint(0, len(parent1.directions[0]) - 1)
                        cPoint2 = rand.randint(0, len(parent1.directions[0]) - 1)
                        if abs(cPoint1 - cPoint2) > 1:
                            if cPoint1 > cPoint2:
                                cPoint1, cPoint2 = cPoint2, cPoint1
                                choosingBoolean = False
                    #First chunk of the offsprings' genes
                    for g in range(0, cPoint1):
                        offspring1.directions[0].append(parent1.directions[0][g])
                        offspring1.directions[1].append(parent1.directions[1][g])
                        offspring2.directions[0].append(parent2.directions[0][g])
                        offspring2.directions[1].append(parent2.directions[1][g])
                    #Second chunk of the offsprings' genes
                    for g in range(cPoint1, cPoint2):
                        offspring1.directions[0].append(parent2.directions[0][g])
                        offspring1.directions[1].append(parent2.directions[1][g])
                        offspring2.directions[0].append(parent1.directions[0][g])
                        offspring2.directions[1].append(parent1.directions[1][g])
                    #Third chunk of the offsprings' genes
                    for g in range(cPoint2, len(parent1.directions[0])):
                        offspring1.directions[0].append(parent1.directions[0][g])
                        offspring1.directions[1].append(parent1.directions[1][g])
                        offspring2.directions[0].append(parent2.directions[0][g])
                        offspring2.directions[1].append(parent2.directions[1][g])
                    nextGen.organisms.append(offspring1)
                    nextGen.organisms.append(offspring2)
                #Since we're still missing one organism we'll just send the strongest organism of out current generation into the next to promote strength
                theChosenOne = Organism(None, 500, 550, geneLength)
                maxFit = -1
                spotOfChosen = 0
                for o in self.organisms:
                    if o.fitness > maxFit:
                        maxFit = o.fitness
                        spotOfChosen = self.organisms.index(o)
                        theChosenOne.id = o.id
                for i in range(len(self.organisms[spotOfChosen].directions[0])):
                    theChosenOne.directions[0].append(self.organisms[spotOfChosen].directions[0][i])
                    theChosenOne.directions[1].append(self.organisms[spotOfChosen].directions[1][i])
                theChosenOne.x = self.initialX
                theChosenOne.y = self.initialY
                theChosenOne.geneLength = geneLength
                nextGen.organisms.append(theChosenOne)
        else:
            nextGen.randGeneration()
        return nextGen
    
    #Dunderscore String Method was used during development for testing
    def __str__(self):
        result = ""
        #Runs string dunderscore for all organisms
        for o in self.organisms:
            result +=  f'{o}\n'
        return result