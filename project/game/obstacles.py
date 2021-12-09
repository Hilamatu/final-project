import arcade
import random
from game import constants

class Obstacles(arcade.Sprite):
    """Class to create the obstacles of the game.
    Stereotype: Interface, service provider"""

    def __init__(self, y, velocity):
        # Will create a list with all the obstacles
        self._obstacles_names = ["cone.png", "bricks.png", "bike.png", "fence.png", "ball.png", "sofa.png", "bags.png", "box.png", "chiken.png", "pumpkin.png", "sofa.png", "trash.png", "wheel.png", "wood.png"]
        self._obstacle = random.choice(self._obstacles_names) # Randomly select one obstacle
        self.values = [0, 100, 150] # Position of the obstacle
        self._plus_distance = random.choice(self.values) # Distance between them
        super().__init__("project/sprites/" + self._obstacle, constants.SCALING) # Super class to get the sprite 
        self.change_x = velocity # Velocity
        self.bottom = y
        self.left = constants.SCREEN_WIDTH + self._plus_distance

    def update(self):
        """Remove the obstacle when it goes off the screen""" 
        if self.right < 0 or self.top < 0 or self.bottom > 720:
            self.remove_from_sprite_lists()
        return super().update()
