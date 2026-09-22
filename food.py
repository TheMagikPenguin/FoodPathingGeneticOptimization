import pygame

class Food(pygame.sprite.Sprite):
    def __init__(self, x : int, y : int, foodType : int):
        #The x and y coordinate of a food object is the top left corner of the food
        #In reality the whole food class is just a bounding area with a png grafted on it
        super().__init__()
        self.foodTypes = ['Bread.png','Strawberry.png']
        self.image = pygame.image.load(f'resources/{self.foodTypes[foodType]}').convert_alpha()
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = self.x
        self.rect.y = self.y
    
    #Updates the location of the Food object. The food object position never changes but is useful for expanding the simulation if they need to move
    def update(self):
        self.rect.x, self.rect.y = self.x, self.y
