#Importing classes (OOB) and libraries (pygame and random)
import random as rand
from food import *
import pygame

class Organism(pygame.sprite.Sprite):
    def __init__(self, id_num : int, x, y, geneLength : int):
        #Inherit from the Sprite class
        super().__init__()
        #Data for calculations
        self.age = 0
        self.id = id_num
        self.directions = [[],
                           []]
        self.fitness = 0
        self.position_queue = []
        self.geneLength = geneLength

        #Data specifically for rendering the sprites of a organism
        self.x = x
        self.y = y
        self.dx = 0
        self.dy = 0
        self.image = pygame.image.load("resources/ERAM.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)
        self.currentRotation = 4

    #This method generates random genes/vectors for a completely new organism (typically only done at the start of a simulation)
    def generateNewDirections(self):
        for i in range(self.geneLength):
            dir = rand.randint(1,4)
            speed = rand.randint(1,5)
            self.directions[0].append(dir)
            self.directions[1].append(speed)
    
    #organismMovement updates the position variables such as x and y of the organism based on their gnees
    def organismMovement(self):
        for i in range(len(self.directions[0])):
            dx = 0
            dy = 0
            newRotation = 0
            if int(self.directions[0][i]) == 1:
                dx = 0
                dy = -10
                newRotation = 4
            elif int(self.directions[0][i]) == 2:
                dx = 10
                dy = 0
                newRotation = 1
            elif int(self.directions[0][i]) == 3:
                dx = 0
                dy = 10
                newRotation = 2
            elif int(self.directions[0][i]) == 4:
                dx = -10
                dy = 0
                newRotation = 3
            self.position_queue.append(((dx * self.directions[1][i]/10), (dy * self.directions[1][i]/10), newRotation))
        return self.position_queue

    #This method blits the position of the organism based on which gene they're currently on
    def update(self, current_frame : int, foods, xBound, yBound):
        if len(self.position_queue) > 0 and current_frame in [0, 10, 20]:
            self.dx, self.dy, newRotation = self.position_queue.pop(0)
            self.image = pygame.transform.rotate(self.image, (self.currentRotation-newRotation)*90)
            self.currentRotation = newRotation
            self.rect = self.image.get_rect(center=self.rect.center)
        if len(self.position_queue) <= 0:
            self.dx, self.dy = 0, 0
        self.x += self.dx
        self.y += self.dy
        if self.x > xBound:
            self.x = 0
        if self.x < 0:
            self.x = xBound
        if self.y > yBound:
            self.y = 0
        if self.y < 0:
            self.y = yBound
        self.rect.center = (self.x, self.y)
        collisionDict = pygame.sprite.groupcollide([self], foods, False, False)
        if collisionDict and len(self.position_queue) != 0:
            self.fitness += len(collisionDict[self])
        if len(self.position_queue) == 0:
            return True
        else:
            return False

    #This method rolls a random float from 0.00 to 1.00 and checks if a gene needs to be randomized (mutated)
    def mutate(self, mutateRate):
        mutationP = mutateRate
        for i in range(len(self.directions[0])):
            mutationRoll = rand.uniform(0.00, 1.00)
            if mutationRoll <= mutationP:
                dir = rand.randint(1,4)
                speed = rand.randint(1,5)
                self.directions[0][i] = dir
                self.directions[1][i] = speed

    #Dunderscore String Method was used during development for testing
    def __str__(self):
        return f'ID: {self.id} || {self.directions[0]} || {self.directions[1]} || Fitness: {self.fitness}'