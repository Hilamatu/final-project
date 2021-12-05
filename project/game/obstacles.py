import arcade
import random
from game import constants

class Obstacles(arcade.Sprite):

    def __init__(self, y, x, velocity):
        self._obstacles_names = ["cone.png", "bricks.png", "bike.png", "fence.png", "ball.png", "sofa.png", "bags.png", "box.png", "chiken.png", "pumpkin.png", "sofa.png", "trash.png", "wheel.png", "wood.png"]
        self._obstacle = random.choice(self._obstacles_names)
        super().__init__("project/sprites/" + self._obstacle, constants.SCALING)
        self.change_x = velocity
        self.bottom = y
        self.right = constants.SCREEN_WIDTH + x

    def update(self):
        if self.right < 0:
            self.remove_from_sprite_lists()
        return super().update()
