import arcade
import random
from game import constants



class Scenario(arcade.Sprite):
    """Class to create the scenarion over the background image created on first_scenario"""
    def __init__(self, y, velocity, turn, condition):
        
        # Will get the position and check if the image can be drawn 
        if condition:
            self.scenes = ["s2.png", "s3.png", "s4.png", "s5.png", "s6.png", "s7.png"]
            super().__init__("project/sprites/" + self.scenes[turn], constants.SCALING)
            self.change_x = velocity
            self.bottom = y
            self.left = constants.SCREEN_WIDTH
        else:
            pass        

    def update(self): 
        """Remove the scenario image when it goes off the screen"""    
        if self.right < 0:
            self.remove_from_sprite_lists()
        return super().update()
