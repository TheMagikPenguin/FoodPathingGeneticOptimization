#Importing classes (OOB) and libraries (pygame and random)
from food import *
from organism import *
from generation import *
import random as rand
import pygame
from button import *

#CREATING GAME ENVIRONMENT
#------------------------------------------------
pygame.init()
#Initializing screen size, title, color, and window icon
screen_width = 1150
screen_height = 720
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Genetic Algorithm Simulation')
bgColor = (237, 232, 218)
screen.fill(bgColor)
simIcon = pygame.image.load("resources/Icon.png").convert_alpha()
pygame.display.set_icon(simIcon)


#RUNTIME LOGIC
#--------------------------------------------------------------
#Creating running boolean to know when pygame is quited
running = True
#Initialize clock object with important counter variables
clock = pygame.time.Clock()
FPS = 30
font = pygame.font.Font(None, 36)
paused = False
runDone = False
currentFrame = 0

#GUI ELEMENTS (MENUS AND BUTTONS)
#---------------------------------------------------------------
#Game Menu
gameMenuXY = (380,275)
gameMenuSize = (400, 130)
gameMenuColor = (74, 71, 64)
gameMenu = pygame.Surface(gameMenuSize)
gameMenu.fill(gameMenuColor)
#Start Menu
startMenuXY = (330,200)
startMenuSize = (450, 340)
startMenuColor = (74, 71, 64)
startMenu = pygame.Surface(startMenuSize)
startMenu.fill(startMenuColor)
startMenuVisible = True
#Next Generation Button Instantiation
newGenButton = Button(screen, font, 6, (420,300), (328,30), (0,0,0), (255,255,255), (181, 177, 168), (0,0,0), False, 'Create Improved Generation')
#Quit Button Instantiation
quitButton = Button(screen, font, 6, (480,350), (195,30), (0,0,0), (255,255,255), (230, 167, 158), (0,0,0), False, 'Quit Simulation')
#Gene Length Customization
geneComplexity = 40
geneDisplay = Button(screen, font, 6, (380,232), (325, 30), (0,0,0), (255,255,255), (181, 177, 168), (0,0,0), True, 'Gene Length/Complexity: 40')
upButtonGene = Button(screen, font, 6, (720,222.5), (18,25), (0,0,0), (255,255,255), (181, 177, 168), (0,0,0), True, 'V')
upButtonGene.text = pygame.transform.rotate(upButtonGene.text, 180)
downButtonGene = Button(screen, font, 6, (720,249.5), (18,25), (0,0,0), (255,255,255), (181, 177, 168), (0,0,0), True, 'V')
#Num of Organisms Customization
numOfOrganisms = 50
organismNumDisplay = Button(screen, font, 6, (397,287), (290, 30), (0,0,0), (255,255,255), (181, 177, 168), (0,0,0), True, 'Number of Organisms: 50')
upButtonOrganismsNumDisplay = Button(screen, font, 6, (720,277.5), (18,25), (0,0,0), (255,255,255), (181, 177, 168), (0,0,0), True, 'V')
upButtonOrganismsNumDisplay.text = pygame.transform.rotate(upButtonOrganismsNumDisplay.text, 180)
downButtonOrganismsNumDisplay = Button(screen, font, 6, (720,304.5), (18,25), (0,0,0), (255,255,255), (181, 177, 168), (0,0,0), True, 'V')
#Num of Food Customization
numOfFood = 7
foodNumDisplay = Button(screen, font, 6, (386,342), (312, 30), (0,0,0), (255,255,255), (181, 177, 168), (0,0,0), True, 'Number of Food Areas: 7')
upButtonFoodNumDisplay = Button(screen, font, 6, (720,332.5), (18,25), (0,0,0), (255,255,255), (181, 177, 168), (0,0,0), True, 'V')
upButtonFoodNumDisplay.text = pygame.transform.rotate(upButtonFoodNumDisplay.text, 180)
downButtonFoodNumDisplay = Button(screen, font, 6, (720,359.5), (18,25), (0,0,0), (255,255,255), (181, 177, 168), (0,0,0), True, 'V')
#Rate of Mutation Customization
mutationRate = 0.05
mutationDisplay = Button(screen, font, 6, (389,397), (306, 30), (0,0,0), (255,255,255), (181, 177, 168), (0,0,0), True, 'Chance of Mutation: 5%')
upButtonMutationDisplay = Button(screen, font, 6, (720,387.5), (18,25), (0,0,0), (255,255,255), (181, 177, 168), (0,0,0), True, 'V')
upButtonMutationDisplay.text = pygame.transform.rotate(upButtonMutationDisplay.text, 180)
downButtonMutationDisplay = Button(screen, font, 6, (720,414.5), (18,25), (0,0,0), (255,255,255), (181, 177, 168), (0,0,0), True, 'V')
#Begin Sim Button
begin = Button(screen, font, 6, (410, 460), (272,40), (0,0,0), (255,255,255), (182, 232, 169), (0,0,0), True, 'Begin Simulation')

#Object/Entity info
spawnPoint = (500, 550)
foods = []
textSurf = font.render(f"Food Collected by This Generation: 0", True, (0,0,0))
screen.blit(textSurf, (10, 10))

#METHOD FOR CHECKING IF MOUSE IS IN A RECTANGULAR AREA (USED FOR BUTTONS)
#---------------------------------------------------------------------------------------------
def MouseInRect(rect):
    mousePos = pygame.mouse.get_pos()
    if mousePos[0] >= rect[0][0] and mousePos[0] <= rect[0][1] and mousePos[1] >= rect[1][0] and mousePos[1] <= rect[1][1]:
        return True
    return False


#RUN LOOP
#---------------------------------------------------------------
while running:
    #Frame counting
    if currentFrame >= 30:
        currentFrame = 0
    
    #EVENT CHECKING
    #--------------------------------------------------------------
    for event in pygame.event.get():
        #Check for quit (hitting x to quit)
        if event.type == pygame.QUIT:
            running = False
        #You can click "p" to pause during the simulation
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p and not newGenButton.visible and not startMenuVisible:
                paused = not paused
        #This entire if makes sure that the color of a button is shaded when hovering over it by checking if it is in the rectangular area of the button.
        if event.type == pygame.MOUSEMOTION:
            if MouseInRect(newGenButton.interactArea) and newGenButton.visible:
                newGenButton.contents.fill(newGenButton.hoverColor)
            else:
                newGenButton.contents.fill(newGenButton.contentColor)
            if MouseInRect(quitButton.interactArea) and quitButton.visible:
                quitButton.contents.fill(quitButton.hoverColor)
            else:
                quitButton.contents.fill(quitButton.contentColor)
            if MouseInRect(upButtonGene.interactArea) and upButtonGene.visible:
                upButtonGene.contents.fill(upButtonGene.hoverColor)
            else:
                upButtonGene.contents.fill(upButtonGene.contentColor)
            if MouseInRect(downButtonGene.interactArea) and downButtonGene.visible:
                downButtonGene.contents.fill(downButtonGene.hoverColor)
            else:
                downButtonGene.contents.fill(downButtonGene.contentColor)
            if MouseInRect(upButtonOrganismsNumDisplay.interactArea) and upButtonOrganismsNumDisplay.visible:
                upButtonOrganismsNumDisplay.contents.fill(upButtonOrganismsNumDisplay.hoverColor)
            else:
                upButtonOrganismsNumDisplay.contents.fill(upButtonOrganismsNumDisplay.contentColor)
            if MouseInRect(downButtonOrganismsNumDisplay.interactArea) and downButtonOrganismsNumDisplay.visible:
                downButtonOrganismsNumDisplay.contents.fill(downButtonOrganismsNumDisplay.hoverColor)
            else:
                downButtonOrganismsNumDisplay.contents.fill(downButtonOrganismsNumDisplay.contentColor)
            if MouseInRect(upButtonFoodNumDisplay.interactArea) and upButtonFoodNumDisplay.visible:
                upButtonFoodNumDisplay.contents.fill(upButtonFoodNumDisplay.hoverColor)
            else:
                upButtonFoodNumDisplay.contents.fill(upButtonFoodNumDisplay.contentColor)
            if MouseInRect(downButtonFoodNumDisplay.interactArea) and downButtonFoodNumDisplay.visible:
                downButtonFoodNumDisplay.contents.fill(downButtonFoodNumDisplay.hoverColor)
            else:
                downButtonFoodNumDisplay.contents.fill(downButtonFoodNumDisplay.contentColor)
            if MouseInRect(upButtonMutationDisplay.interactArea) and upButtonMutationDisplay.visible:
                upButtonMutationDisplay.contents.fill(upButtonMutationDisplay.hoverColor)
            else:
                upButtonMutationDisplay.contents.fill(upButtonMutationDisplay.contentColor)
            if MouseInRect(downButtonMutationDisplay.interactArea) and downButtonMutationDisplay.visible:
                downButtonMutationDisplay.contents.fill(downButtonMutationDisplay.hoverColor)
            else:
                downButtonMutationDisplay.contents.fill(downButtonMutationDisplay.contentColor)
            if MouseInRect(begin.interactArea) and downButtonFoodNumDisplay.visible:
                begin.contents.fill(begin.hoverColor)
            else:
                begin.contents.fill(begin.contentColor)
        #Checks if buttons are hit
        if event.type == pygame.MOUSEBUTTONDOWN:
            #If new gen button is clicked then it will create a new and typically improved generation
            if MouseInRect(newGenButton.interactArea) and newGenButton.visible:
                currentGeneration = newGenButton.newGen(currentGeneration, geneComplexity)
                quitButton.visible = False
                organismSprites = pygame.sprite.Group(currentGeneration.organisms)
                for o in currentGeneration.organisms:
                    o.organismMovement()
                currentFrame = 0
                paused = False
            #Clicking this button increases gene complexity/length
            if MouseInRect(upButtonGene.interactArea) and upButtonGene.visible:
                if geneComplexity < 90:
                    geneComplexity += 10
                geneDisplay.string = f'Gene Length/Complexity: {geneComplexity}'
                if geneDisplay.fitByHeightYN:
                    geneDisplay.text = geneDisplay.textFitByHeight(geneDisplay.string, geneDisplay.font, geneDisplay.contentsSize[1], geneDisplay.textColor)
                else:
                    geneDisplay.text = geneDisplay.textFitByWidth(geneDisplay.string, geneDisplay.font, geneDisplay.contentsSize[1], geneDisplay.textColor)
            #Clicking this button decreases gene complexity/length
            if MouseInRect(downButtonGene.interactArea) and downButtonGene.visible:
                if geneComplexity > 10:
                    geneComplexity -= 10
                geneDisplay.string = f'Gene Length/Complexity: {geneComplexity}'
                if geneDisplay.fitByHeightYN:
                    geneDisplay.text = geneDisplay.textFitByHeight(geneDisplay.string, geneDisplay.font, geneDisplay.contentsSize[1], geneDisplay.textColor)
                else:
                    geneDisplay.text = geneDisplay.textFitByWidth(geneDisplay.string, geneDisplay.font, geneDisplay.contentsSize[1], geneDisplay.textColor)
            #Clicking this button increases number of organisms in a generation
            if MouseInRect(upButtonOrganismsNumDisplay.interactArea) and upButtonOrganismsNumDisplay.visible:
                if numOfOrganisms < 90:
                    numOfOrganisms += 5
                organismNumDisplay.string = f'Number of Organisms: {numOfOrganisms}'
                if organismNumDisplay.fitByHeightYN:
                    organismNumDisplay.text = organismNumDisplay.textFitByHeight(organismNumDisplay.string, organismNumDisplay.font, organismNumDisplay.contentsSize[1], organismNumDisplay.textColor)
                else:
                    organismNumDisplay.text = organismNumDisplay.textFitByWidth(organismNumDisplay.string, organismNumDisplay.font, organismNumDisplay.contentsSize[1], organismNumDisplay.textColor)
            #Clicking this button decreases number of organisms in a generation
            if MouseInRect(downButtonOrganismsNumDisplay.interactArea) and downButtonOrganismsNumDisplay.visible:
                if numOfOrganisms > 20:
                    numOfOrganisms -= 5
                organismNumDisplay.string = f'Number of Organisms: {numOfOrganisms}'
                if organismNumDisplay.fitByHeightYN:
                    organismNumDisplay.text = organismNumDisplay.textFitByHeight(organismNumDisplay.string, organismNumDisplay.font, organismNumDisplay.contentsSize[1], organismNumDisplay.textColor)
                else:
                    organismNumDisplay.text = organismNumDisplay.textFitByWidth(organismNumDisplay.string, organismNumDisplay.font, organismNumDisplay.contentsSize[1], organismNumDisplay.textColor)
            #Clicking this button increases the number of food areas in the map
            if MouseInRect(upButtonFoodNumDisplay.interactArea) and upButtonFoodNumDisplay.visible:
                if numOfFood < 20:
                    numOfFood += 1
                foodNumDisplay.string = f'Number of Food Areas: {numOfFood}'
                if foodNumDisplay.fitByHeightYN:
                    foodNumDisplay.text = foodNumDisplay.textFitByHeight(foodNumDisplay.string, foodNumDisplay.font, foodNumDisplay.contentsSize[1], foodNumDisplay.textColor)
                else:
                    foodNumDisplay.text = foodNumDisplay.textFitByWidth(foodNumDisplay.string, foodNumDisplay.font, foodNumDisplay.contentsSize[1], foodNumDisplay.textColor)
            #Clicking this button decreases the number of food areas in the map
            if MouseInRect(downButtonFoodNumDisplay.interactArea) and downButtonFoodNumDisplay.visible:
                if numOfFood > 3:
                    numOfFood -= 1
                foodNumDisplay.string = f'Number of Food Areas: {numOfFood}'
                if foodNumDisplay.fitByHeightYN:
                    foodNumDisplay.text = foodNumDisplay.textFitByHeight(foodNumDisplay.string, foodNumDisplay.font, foodNumDisplay.contentsSize[1], foodNumDisplay.textColor)
                else:
                    foodNumDisplay.text = foodNumDisplay.textFitByWidth(foodNumDisplay.string, foodNumDisplay.font, foodNumDisplay.contentsSize[1], foodNumDisplay.textColor)
            #Clicking this button increases the percent chance that a gene will mutate
            if MouseInRect(upButtonMutationDisplay.interactArea) and upButtonMutationDisplay.visible:
                if mutationRate < 0.4:
                    mutationRate += 0.01
                mutationDisplay.string = f'Chance of Mutation: {int(mutationRate*100)}%'
                if mutationDisplay.fitByHeightYN:
                    mutationDisplay.text = mutationDisplay.textFitByHeight(mutationDisplay.string, mutationDisplay.font, mutationDisplay.contentsSize[1], mutationDisplay.textColor)
                else:
                    mutationDisplay.text = mutationDisplay.textFitByWidth(mutationDisplay.string, mutationDisplay.font, mutationDisplay.contentsSize[1], mutationDisplay.textColor)
            #Clicking this button decreases the percent chance that a gene will mutate
            if MouseInRect(downButtonMutationDisplay.interactArea) and downButtonMutationDisplay.visible:
                if mutationRate > 0.0:
                    mutationRate -= 0.01
                mutationDisplay.string = f'Chance of Mutation: {int(mutationRate*100)}%'
                if mutationDisplay.fitByHeightYN:
                    mutationDisplay.text = mutationDisplay.textFitByHeight(mutationDisplay.string, mutationDisplay.font, mutationDisplay.contentsSize[1], mutationDisplay.textColor)
                else:
                    mutationDisplay.text = mutationDisplay.textFitByWidth(mutationDisplay.string, mutationDisplay.font, mutationDisplay.contentsSize[1], mutationDisplay.textColor)
            #Clicking this button removes you from the start menu and starts the simulation
            if MouseInRect(begin.interactArea) and begin.visible:
                currentGeneration = Generation(spawnPoint, numOfOrganisms, mutationRate)
                currentGeneration.randGeneration(geneComplexity)
                for o in currentGeneration.organisms:
                    o.organismMovement()
                for i in range(numOfFood):
                    f = Food(rand.randint(50,screen_width-50), rand.randint(50,screen_height-50), rand.randint(0,1))
                    while f.x >= (spawnPoint[0]-350) and f.x <= (spawnPoint[0]+350) and f.y >= (spawnPoint[1]-200) and f.y <= (spawnPoint[1]+200):
                        f = Food(rand.randint(50,screen_width-50), rand.randint(50,screen_height-50), rand.randint(0,1))
                    foods.append(f)
                foodSprites = pygame.sprite.Group(foods)
                organismSprites = pygame.sprite.Group(currentGeneration.organisms)
                startMenuVisible = False
                geneDisplay.visible = False
                upButtonGene.visible = False
                downButtonGene.visible = False
                organismNumDisplay.visible = False
                upButtonOrganismsNumDisplay.visible = False
                downButtonOrganismsNumDisplay.visible = False
                foodNumDisplay.visible = False
                upButtonFoodNumDisplay.visible = False
                downButtonFoodNumDisplay.visible = False
                mutationDisplay.visible = False
                upButtonMutationDisplay.visible = False
                downButtonMutationDisplay.visible = False
                begin.visible = False
            #In between generations clicking this button will close the simulation
            if MouseInRect(quitButton.interactArea) and quitButton.visible:
                running = False
    #ALL EVENTS THAT WILL OCCUR WHILE ORGANISMS ARE MOVING
    #-----------------------------------------------------------------------------
    if not (paused or newGenButton.visible or startMenuVisible):
        #Renders the fitness counter text and the background
        screen.fill(bgColor)
        textSurf = font.render(f"Food Collected by This Generation: {currentGeneration.fitnessSummation()}", True, (0,0,0))
        screen.blit(textSurf, (10, 10))
        #Updates the position of the organisms and foods and redraws them along with iterating the frame counter
        for o in organismSprites:
            tf = o.update(currentFrame, foods, screen_width, screen_height)
            newGenButton.visible, quitButton.visible = tf, tf
        foodSprites.update()
        foodSprites.draw(screen)
        organismSprites.draw(screen)
        screen.blit(textSurf, (10, 10))
        currentFrame += 1
        clock.tick(FPS)
    #Updating all GUIs
    if newGenButton.visible:
        screen.blit(gameMenu, gameMenuXY)
    if startMenuVisible:
        screen.blit(startMenu, startMenuXY)
    newGenButton.update(screen)
    quitButton.update(screen)
    geneDisplay.update(screen)
    upButtonGene.update(screen)
    downButtonGene.update(screen)
    organismNumDisplay.update(screen)
    upButtonOrganismsNumDisplay.update(screen)
    downButtonOrganismsNumDisplay.update(screen)
    foodNumDisplay.update(screen)
    upButtonFoodNumDisplay.update(screen)
    downButtonFoodNumDisplay.update(screen)
    mutationDisplay.update(screen)
    upButtonMutationDisplay.update(screen)
    downButtonMutationDisplay.update(screen)
    begin.update(screen)
    pygame.display.flip()