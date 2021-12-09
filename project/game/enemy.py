import arcade
import random
from game import constants


class Enemy(arcade.Sprite):
    
    def __init__(self, velocity):
        
        self.enemys = ["e1.png", "e2.png", "e3.png", "e4.png"]
        self.enemy = random.choice(self.enemys)
        super().__init__("project/sprites/" + self.enemy, constants.SCALING)
        self.change_x = velocity
        self.bottom = 40
        self.right = -400

    def update(self):
        if self.left > constants.SCREEN_WIDTH:
            self.remove_from_sprite_lists()
            
        return super().update()