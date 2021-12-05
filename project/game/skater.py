import arcade
from game import constants

class Skater(arcade.Sprite):

    def __init__(self):        
        super().__init__("skater/sprites/skater.png", constants.SCALING)
        self.center_x = 80
        self.bottom = 52

    def update(self):
        self.center_x += self.change_x
        self.center_y += self.change_y
                
        if self.left < 0:
            self.left = 0
        elif self.right > constants.SCREEN_WIDTH:
            self.right = constants.SCREEN_WIDTH