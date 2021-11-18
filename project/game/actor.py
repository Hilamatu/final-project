from time import time
import arcade
import constants
import random
from moving_sprites import MovingSprite
import time

class Actor():
    """A class to create all the sprites for the game
    
    Stereotype: Information holder, Interface"""

    def __init__(self):

        """ Set up the empty sprites lists """

        # Create the list to handle position and collision
        self.obstacles_list = arcade.SpriteList()

        # Draw everything
        self.all_sprites = arcade.SpriteList()

        self.width = constants.SCREEN_WIDTH

        self.height = constants.SCREEN_HEIGHT

        # Spawn a new obstacle every 0.25 seconds
        arcade.schedule(self.add_obstacles, 0.50)

    
    def add_obstacles(self, delta_time: float):
        """ Adds a new obstacle to screen.
        
        Arguments: 
            delta_time {float} -- How much time has passed since the last call """

        # First create the new obstacle sprite (Rather than creating a new Sprite, 
        # you create a new FlyingSprite to take advantage of the new .update())
        obstacle = arcade.Sprite(arcade.draw_rectangle_filled(center_x=random.randint(self.width, self.width + 10), center_y=self.height/3, width=100, height=60, color=arcade.color.RED))

        # Sets  its speed to a random speed heading left 
        obstacle.velocity = (-800, 100)

        # Add it to the enemies list
        self.obstacles_list.append(obstacle)
        self.all_sprites.append(obstacle)


    def on_draw(self):
        """ Draw  all game objects
        
        All drawing starts with the call to arcade.start_render(). 
        Just like updating, you can draw all your sprites at once by simply calling self.all_sprites.draw()"""

        arcade.start_render()
        self.all_sprites.draw()

        
