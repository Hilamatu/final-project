import arcade
import random

from arcade.draw_commands import draw_rectangle_filled
from game import constants
from game.moving_sprite import MovingSprite
from game.handle_collisions_action import HandleCollisionsAction
# from game.player import Player
from game.score import Score



class GameView(arcade.View):
    """The game view. Where everything will happen.
    Stereotype: interface, controller, information holder
    
    Methods:
    on_show_view: Code to execute while displaying the view
    add_obstacles: Function to create 4 types of obstacles and add it randomly to spriteList
    on_key_press: Function to detect when a key is pressed and perform the respective task
    on_key_release: Function to detect when a key is released and perform the respective task
    on_draw: Will draw everything on this view
    on_update: Code to excute everytime the view is updated"""

    def on_show_view(self):
        """ While in this view, evrything below will take place.
        args: 
        self.obstacles: creates the spriteList to store the obstacles
        self.all_sprites: Creates the spriteList to store all the sprites for the game
        sel.player: The player. In this case, the skater
        self.ground_list: Creates the spriteList to store the ground sprite separatedly to controll the jump
        self.physics_engine: Checks if the player is on ground and if .can_jump.
        """

        # Set the background color
        arcade.set_background_color(arcade.color.LIGHT_BLUE)
        # Clear the screen and start drawing
        arcade.start_render()

        # Will schedule the method calling to 4
        arcade.schedule(self.add_obstacles, 4)
        self.obstacles = arcade.SpriteList() # Sprite List to store the obstacles
        self.all_sprites = arcade.SpriteList() # Sprite list to store all sprites of the game

        # Creates the player sprite
        self.player = arcade.Sprite("../final-project/project/sprite/skater.png", center_x=100, center_y=200)
        # add the player sprite to all_sprite list
        self.all_sprites.append(self.player)

        self.ground_list = arcade.SpriteList() # Creates the sprite list to store the ground sprite

        # Creates a loop to create sprites for the ground on different X position.
        for x in range(0, constants.SCREEN_WIDTH, constants.SPRITE_SIZE):
            ground = arcade.Sprite("../final-project/project/sprite/ground.png", constants.SCALING)
            ground.center_y=110 # Y position will not change
            ground.left = x # Will change the X position according to the width stepping the size of the sprite

            self.ground_list.append(ground) # Append everything with the x position updated to ground_list

        # Will call the arcade.PhysicsEnginePlatformer passing the player, ground_list and gravity_constant as parameters
        self.physics_engine = arcade.PhysicsEnginePlatformer(self.player, self.ground_list, gravity_constant= constants.GRAVITY)

        Score().collisionDetection(self.player_score)
        
        



    def add_obstacles(self, delta_time: int):
        """ Will create and to the sprite list all the obstacles randomly. 
        Receives the parameter of delta_time to manage how much time has passed since last call.

        The obstacles will be created using MovingSprite which receives arcade.Sprite as parameter.
        The MovingSprite will delete every sprite that goes off the view
        """

        brick = MovingSprite("../final-project/project/sprite/brick.png", center_x=constants.SCREEN_WIDTH, center_y=200)
        brick.velocity = (-100, 0) # Since it is moving from left to right on the same height

        dog = MovingSprite("../final-project/project/sprite/dog.png", center_x=constants.SCREEN_WIDTH + 200, center_y=200)
        dog.velocity = (-100, 0) # Since it is moving from left to right on the same height

        obstacle_list = [brick, dog] # Creates a list to store all the obstacles created
        selected_obstacle = random.choice(obstacle_list) # Using the random.choice, will select randomly one of the sprites

        # Will add the randomly selected sprites to bothe spriteList
        self.obstacles.append(selected_obstacle)
        self.all_sprites.append(selected_obstacle)

    def on_key_press(self, symbol, modifiers):
        """Handle user keyboard input
        Q: Quit the game
        I/J/K/L: Move up, left, down, right 
        Arrows: Move up, left, down, right 
        
        Arguments: 
            symbol {int} -- which key was pressed
            modifires {int} -- Which modifiers were pressed
        """

        if symbol == arcade.key.Q:
            # Quit immediatelly
            arcade.close_window()
        
        if symbol == arcade.key.J or symbol == arcade.key.LEFT:
            self.player.change_x = -10
        
        if symbol == arcade.key.L or symbol == arcade.key.RIGHT:
            self.player.change_x = 10

        if symbol == arcade.key.SPACE:
            # Will using the parameters passed, will check if the player is on the ground.
            # If the player is on the ground, will return True to .can_jump
            if self.physics_engine.can_jump():
                # Will apply the JUMP_SPEED to determine the height of the jump the gravity to controll the falling
                self.player.change_y = constants.JUMP_SPEED
                
    def on_key_release(self, symbol, modifiers):

        """Will handle the key release and will stop moving the player"""

        if (
            symbol == arcade.key.J
            or symbol == arcade.key.L
            or symbol == arcade.key.LEFT
            or symbol == arcade.key.RIGHT

        ):
            self.player.change_x = 0
        

    def on_draw(self):
        """ Will clean the view and draw everything"""

        arcade.start_render()
        self.all_sprites.draw()
        self.ground_list.draw()
    

    def on_update(self, delta_time: float):

        """ Codes to be executed when update the screen"""

        # Will automatically move the sprites 
        for sprite in self.all_sprites:
            sprite.center_x = int (
                sprite.center_x + sprite.change_x * delta_time
            )
            sprite.center_y = int (
                sprite.center_y + sprite.change_y * delta_time
            )
        
        #cheking collisions
        HandleCollisionsAction().on_obstacles_collision(self.obstacles, self.player, delta_time)
        
        
        # Will update the physics_engine. It means updating the player position simulating the jump 
        # considering the values and parameters passed
        self.physics_engine.update()

        # Keep the player on the screen
        if self.player.right > constants.SCREEN_WIDTH:
            self.player.right = constants.SCREEN_WIDTH
        if self.player.left < 0:
            self.player.left = 0

        