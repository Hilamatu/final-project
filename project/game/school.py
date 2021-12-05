import arcade
from game import constants

class School(arcade.Sprite):

    def __init__(self, y, velocity):        
        super().__init__("project/sprites/school.png", constants.SCALING)
        self.change_x = velocity
        self.bottom = y
        self.left = constants.SCREEN_WIDTH * 3

    def update(self):
        if self.right < constants.SCREEN_WIDTH + 10:
            self.change_x = 0
        return super().update()
