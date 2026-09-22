#Importing classes (OOB) and libraries (pygame and random)
from food import *
from organism import *
from generation import *
import random as rand
import pygame

class Button():
    #The instantiation for my button class with all the qualities of a button
    def __init__(self, screen : pygame.Surface, font : pygame.font.Font, borderThickness : int,\
                 XY : tuple, buttonSize : tuple, borderColor : tuple, contentColor : tuple, 
                 hoverColor : tuple, textColor: tuple, visibility : bool = False,\
                 string : str = '', fitByHeightYN = True):
        #Everything relating to the button sizing variables and creating the border
        self.visible = visibility
        self.font = font
        #Note: Border thickness should be even unless you want an uneven button
        self.borderThickness = borderThickness
        self.XY = XY
        self.string = string
        self.size = buttonSize
        #Note: The bui variable stands for Bordered User Interface as unusual as it sounds
        self.bui = (self.XY, self.size)
        self.button = pygame.Surface(self.size)
        self.borderColor = borderColor
        self.button.fill(self.borderColor)

        #Creating the contents of the button inside the border
        self.contentsSize = (self.size[0] - self.borderThickness, self.size[1] - self.borderThickness)
        self.contents = pygame.Surface(self.contentsSize)
        self.contentColor = contentColor
        self.contents.fill(self.contentColor)
        self.contentsXY = (self.XY[0] + self.borderThickness/2, self.XY[1] + self.borderThickness/2)

        #Creates the text on the button
        self.textColor = textColor
        self.fitByHeightYN = fitByHeightYN
        if self.fitByHeightYN:
            self.text = self.textFitByHeight(self.string, self.font, self.contentsSize[1], self.textColor)
        else:
            self.text = self.textFitByWidth(self.string, self.font, self.contentsSize[1], self.textColor)

        self.hoverColor = hoverColor
        self.interactArea = [(self.XY[0], self.XY[0] + self.size[0]), (self.XY[1], self.XY[1] + self.size[1])]

    #TEXT SIZING METHODS
    #--------------------------------------------------------------------------------------
    #The following two methods create a ratio between the height and the width of the button and create a surface using the font and scaling it
    #in relation to said ratio
    def textFitByHeight(self, text, fontType, height, color = (0,0,0), antiAlias = True):
        size = fontType.size(text)
        ratio = size[0]/ size[1]
        render = fontType.render(text, antiAlias, color)
        render = pygame.transform.scale(render, (ratio * height, height))
        return render
    
    def textFitByWidth(self, text, fontType, width, color = (0,0,0), antiAlias = True):
        size = fontType.size(text)
        ratio = size[1]/ size[0]
        render = fontType.render(text, antiAlias, color)
        render = pygame.transform.scale(render, (width, ratio * width))
        return render
    
    #THIS RUNS WHEN CLICKING THE NEW GEN BUTTON
    #-------------------------------------------------------------------------------------------
    def newGen(self, previousGeneration : Generation, geneLength):
        #It either creates a new generation if last generation got 0 fitness or improves the generations
        if previousGeneration.fitnessSummation() == 0:
            newGeneration = Generation((previousGeneration.initialX, previousGeneration.initialY), geneLength)
            newGeneration.randGeneration()
        else:
            newGeneration = previousGeneration.twoPointCrossover(geneLength)
        newGeneration.mutateGeneration(previousGeneration.mutateRate)
        self.visible = False
        return newGeneration

    #Blits the border, content, and text of a button to the screen. This method exists so I can write less
    def update(self, screen : pygame.Surface):
        if self.visible:
            screen.blit(self.button, self.XY)
            screen.blit(self.contents, self.contentsXY)
            screen.blit(self.text, self.contentsXY)
            return True
        return False