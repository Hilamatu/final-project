import arcade
from game import constants

class Skater(arcade.Sprite):
    """Class to create the skater.

    Stereotype: Service Provider"""

    def __init__(self):
        """Create the skater sprite and set the initial position"""

        super().__init__("project/sprites/skater.png", constants.SCALING)
        self.center_x = 80
        self.bottom = 52

    def update(self):
        
        """Will keep the skater on the screen"""
        self.center_x += self.change_x
        self.center_y += self.change_y
                
        if self.left < 0:
            self.left = 0
        elif self.right > constants.SCREEN_WIDTH:
            self.right = constants.SCREEN_WIDTH
        elif self.top > constants.SCREEN_HEIGHT:
            self.top = constants.SCREEN_HEIGHT