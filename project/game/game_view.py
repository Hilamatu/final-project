import arcade
from actor import Actor


class GameView(arcade.View):
    def on_show(self):
        
        # Set the background color
        arcade.set_background_color(arcade.color.LIGHT_BLUE)
        # Clear the screen and start drawing
        arcade.start_render()
        
        Actor()

    