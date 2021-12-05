import arcade
import random
from game import constants



class Scenario(arcade.Sprite):

    def __init__(self, y, velocity, turn, condition):
        
        if condition:
            self.scenes = ["s2.png", "s3.png", "s4.png", "s5.png", "s6.png", "s7.png"]
            super().__init__("project/sprites/" + self.scenes[turn], constants.SCALING)
            self.change_x = velocity
            self.bottom = y
            self.left = constants.SCREEN_WIDTH
        else:
            pass        

    def update(self):    
        if self.right < 0:
            self.remove_from_sprite_lists()
        return super().update()
