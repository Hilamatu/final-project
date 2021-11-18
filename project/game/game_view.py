import arcade
from arcade.color import RED


class GameView(arcade.View):
    def on_show(self):
        
        # Set the background color
        arcade.set_background_color(arcade.color.WHITE)
        # Clear the screen and start drawing
        arcade.start_render()

        # Draw a blue circle
        arcade.draw_rectangle_filled(200, 200, 100, 300, RED)