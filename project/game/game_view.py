import arcade
import random

from arcade.sprite_list.sprite_list import SpriteList
from game import constants
from game.moving_sprite import MovingSprite

class GameView(arcade.View):
    def on_show_view(self):
        
        # Set the background color
        arcade.set_background_color(arcade.color.LIGHT_BLUE)
        # Clear the screen and start drawing
        arcade.start_render()

        arcade.schedule(self.add_obstacles, 4)
        self.obstacles = arcade.SpriteList()

    def add_obstacles(self, delta_time: int):
        
        obstacle = MovingSprite("../final-project/project/sprite/jet.png", center_x=constants.SCREEN_WIDTH, center_y=200)
        rectangle = MovingSprite("../final-project/project/sprite/missile.png", center_x=constants.SCREEN_WIDTH + 200, center_y=200)

        obstacle.velocity = (-100, 0)
        rectangle.velocity = (-100, 0)

        self.obstacles.append(rectangle)
        self.obstacles.append(obstacle)

        

    def on_draw(self):
        arcade.start_render()
        self.obstacles.draw()

    
    def on_update(self, delta_time: float):
        for sprite in self.obstacles:
            sprite.center_x = int (
                sprite.center_x + sprite.change_x * delta_time
            )
            sprite.center_y = int (
                sprite.center_y + sprite.change_y * delta_time
            )

