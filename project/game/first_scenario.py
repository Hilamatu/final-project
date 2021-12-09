import arcade
from game import constants

class First_scenario(arcade.Sprite):
    """Class to create the scenario for the game.
    Stereotype: Structure, service provider"""

    def __init__(self, y, velocity):

        super().__init__("project/sprites/firstscene.png", constants.SCALING)
        self.change_x = velocity
        self.bottom = y
        self.left = 0
        

    def update(self): 
        """Remove the scenario image when it goes off the screen"""   
        if self.right < 0:
            self.remove_from_sprite_lists()

        return super().update()

