import arcade
import random
from game import constants


class Medicine(arcade.Sprite):
    """Class to create the medicine for the game
    
    Stereotype: Service provider"""

    def __init__(self, velocity):
        # Creates and positions the medicine at the screen
        velocities = [220, 290, 360]
        random_velocity = random.choice(velocities)       
        super().__init__("project/sprites/medicine.png", constants.SCALING)
        self.change_x = velocity
        self.bottom = random_velocity
        self.right = constants.SCREEN_WIDTH

    def update(self):
        """Remove the scenario image when it goes off the screen""" 
        if self.right < 0:
            self.remove_from_sprite_lists()
        return super().update()
    