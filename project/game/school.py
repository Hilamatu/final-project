import arcade
from game import constants

class School(arcade.Sprite):
    """Class to create the school
    Sterorype: Service provider"""

    def __init__(self, y, velocity):
        # Will draw and position the school sprite image        
        super().__init__("project/sprites/school.png", constants.SCALING)
        self.change_x = velocity
        self.bottom = y
        self.left = constants.SCREEN_WIDTH * 3

    def update(self):
        """Remove the scenario image when it goes off the screen""" 
        if self.right < constants.SCREEN_WIDTH + 10:
            self.change_x = 0
        return super().update()
