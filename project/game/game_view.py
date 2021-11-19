import arcade
from actor import Actor
import random
import constants


class GameView(arcade.View):
    def on_show_view(self):
        
        # Set the background color
        arcade.set_background_color(arcade.color.LIGHT_BLUE)
        # Clear the screen and start drawing
        arcade.start_render()

        self.center_x = constants.SCREEN_WIDTH
        self.center_y = constants.SCREEN_HEIGHT/3

    def on_draw(self):
        arcade.start_render()
        arcade.draw_rectangle_filled(center_x=self.center_x, center_y=self.center_y, width=100, height=60, color=arcade.color.RED)

    
    def on_update(self, delta_time: float):
        self.center_x += -200 * delta_time
        self.center_y += 0 * delta_time

    