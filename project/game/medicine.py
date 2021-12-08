import arcade
import random
from game import constants


class Medicine(arcade.Sprite):

    def __init__(self, velocity):
        velocities = [220, 290, 360]
        random_velocity = random.choice(velocities)       
        super().__init__("project/sprites/medicine.png", constants.SCALING)
        self.change_x = velocity
        self.bottom = random_velocity
        self.right = constants.SCREEN_WIDTH

    def update(self):
        
        if self.right < 0:
            self.remove_from_sprite_lists()
        return super().update()
    