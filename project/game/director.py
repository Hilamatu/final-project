# Import everything to be used
import arcade
import random
import time


from game import constants
from game.first_scenario import First_scenario
from game.scenario import Scenario
from game.skater import Skater
from game.medicine import Medicine
from game.obstacles import Obstacles
from game.school import School
from game.enemy import Enemy


# Global variables
WIDTH = constants.SCREEN_WIDTH
HEIGHT = constants.SCREEN_HEIGHT

# Global score variable to be accesed and altered by all director and loseview
score = 0


def main():
    """Main function to run the arcade, start the window and display the initial view which is the MenuView"""

    window = arcade.Window(WIDTH, HEIGHT, "Skater")
    menu_view = MenuView()
    window.show_view(menu_view)
    arcade.run()


class MenuView(arcade.View):
    """A class to handle the menu view. It iherits the arcade.View.
    Sterteotype: Interface, information holder."""


    def on_show(self):
        """Method that will be called once this view is displayed.
        Will create the arcade view (Arcade's method)"""
        arcade.set_background_color(arcade.color.SKY_BLUE)

    def on_draw(self):
        """Method to draw everthing on screen (arcade's method)"""

        arcade.start_render() # Clear the screen and draw everything

        # Call and draw the background images
        start_background = arcade.Sprite("project/sprites/start.jpg", constants.SCALING)
        start_background.center_x = constants.SCREEN_WIDTH / 2
        start_background.center_y = constants.SCREEN_HEIGHT / 2
        start_background.draw()

    def on_key_press(self, symbol, modifiers):
        """Method to handle the key press of the keyboard. It takes symbol and modifiers as parameters"""

        # Checks what key was pressed and pass it to the symbol
        if symbol == arcade.key.H:
            instructions_view = InstructionView()
            self.window.show_view(instructions_view)
        elif symbol == arcade.key.ENTER:
            director = Director()
            self.window.show_view(director)
        elif symbol == arcade.key.Q:
            arcade.close_window()




class InstructionView(arcade.View):
    """Class for the instruction view. This class will be called once the 
    player press the H key on menu view.
    It will display the game instruction and will return to the menu view once the player press R
    
    Stereotype: Interface, information holder"""


    def on_show(self):
        """Method called once this view is displayed"""
        self.width = WIDTH/2
        self.new_line = 45

    def on_draw(self):
        """Method to draw everthing on screen (arcade's method)"""

        arcade.start_render()
        instructions_background = arcade.Sprite("project/sprites/instructions.jpg", constants.SCALING)
        instructions_background.center_x = constants.SCREEN_WIDTH / 2
        instructions_background.center_y = constants.SCREEN_HEIGHT / 2
        instructions_background.draw()

    def on_key_press(self, symbol, modifiers):
        """Method to handle the key press of the keyboard. It takes symbol and modifiers as parameters"""

        if symbol == arcade.key.R:
            menu_view = MenuView()
            self.window.show_view(menu_view)




class Director(arcade.View):
    """Class for the director view. This is the game view with the game logic. Will import other classes, create all
    the sprites and background for the game, updates the view and controls the entire game.
    
    Stereotype: Controller, information holder
    
    """
    def __init__(self):
        # Since it is using view instead of window, it will call the super class __init__ which contains the window 
        super().__init__()

        # Creates all the sprites to be used in this game and assign it to a variable
        self.skater_list = arcade.SpriteList()
        self.obstacles_list = arcade.SpriteList()
        self.scenario_list = arcade.SpriteList()
        self.ground_list = arcade.SpriteList()
        self.first_scenario_list = arcade.SpriteList()
        self.school_list = arcade.SpriteList()
        self.medicine_list = arcade.SpriteList()
        self.enemy_list = arcade.SpriteList()

        # Creates all the variables to be used in this game passing None, or constants values as their values.
        self.first_scenario = None
        self.scenario = None        
        self.skater = None
        self.obstacle = None
        self.score_text = None        
        self.lives = constants.LIVES
        self.lives_text = None
        self.scene_turn = 0
        self.static_background = None
        self.static_scene = None
        self.round = 0
        self.school = None
        self.stop = True
        self.medicine = None
        self._gravity = constants.GRAVITY    
        self.enemy = None
        self.enemy_period = constants.ENEMY_PERIOD
        self.remaining_obstacles = constants.ROUNDS
        self.remaining_text = None
        self.out_of_screen = False
        

        # Variables to handle the sounds
        self.sound_crash = arcade.load_sound(constants.SOUND_OUCH)
        self.sound_live = arcade.load_sound(constants.SOUND_LIVE)
        self.sound_jump = arcade.load_sound(constants.SOUND_JUMP)
        self.sound_enemy = arcade.load_sound(constants.SOUND_ENEMY)
        self.sound_bell = arcade.load_sound(constants.SOUND_BELL)
        self.sound_background = arcade.load_sound(constants.SOUND_BACKGROUND, streaming=True)

    def on_show(self):
        """Method called once this view is displayed"""

        # Creates the screen
        arcade.set_background_color(arcade.color.LIGHT_BLUE) 
        # Import the skater   
        self.skater = Skater()
        # Schedule the functions as needed
        arcade.schedule(self.add_obstacle, 1.1)
        arcade.schedule(self.add_scenario, 8)
        arcade.schedule(self.add_medicine, random.randint(8, 15))
        
        # Variable to store the background music to be played and stopped during the game.
        self.music = arcade.play_sound(self.sound_background, volume=constants.VOLUME_BACKGROUND, looping=True)
        
        # Calls the methods to add the scenario of the game
        self.add_background()
        self.add_static_scene()
        self.add_first_scene()
        
        # Appends the imported skater to the list
        self.skater_list.append(self.skater)
    
        # Creates the ground and the logic that will allow the skater to jump
        for x in range(0, constants.SCREEN_WIDTH, constants.SPRITE_SIZE):
            ground = arcade.Sprite("project/sprites/ground.png", constants.SCALING)
            ground.top = 50
            ground.left = x
            self.ground_list.append(ground)
            # Set the skater falling by gravity limit when jumping
            self.physics_engine = arcade.PhysicsEnginePlatformer(self.skater, self.ground_list, gravity_constant= self._gravity) 

         
            

    def on_draw(self):
        """Method to draw everthing on screen (arcade's method)"""

        arcade.start_render() # Clears the screen and starts drawing

        # Draw everything to be used in this game            
        self.static_background.draw()
        self.static_scene.draw()
        self.first_scenario_list.draw()
        self.scenario_list.draw()
        self.school_list.draw()
        self.skater_list.draw()
        self.obstacles_list.draw()
        self.medicine_list.draw()
        self.enemy_list.draw()

        # Makes the score to be update and displayed during the game 
        arcade.draw_text(text = str(self.score_text),
                        color = (105, 105, 105),
                        start_x = constants.SCREEN_WIDTH - 200,
                        start_y = constants.SCREEN_HEIGHT - 50,
                        font_size = 24, font_name = "calibri",
                        bold = True)
        # Makes the lives to be update and displayed during the game
        arcade.draw_text(text = str(self.lives_text),
                        color = (105, 105, 105),
                        start_x = 50,
                        start_y = constants.SCREEN_HEIGHT - 50,
                        font_size = 24, font_name = "calibri",
                        bold = True)
        # Makes the remaining obstacles to be update and displayed during the game
        arcade.draw_text(text = str(self.remaining_text),
                        color = (105, 105, 105),
                        start_x = WIDTH/3,
                        start_y = constants.SCREEN_HEIGHT - 50,
                        font_size = 24, font_name = "calibri",
                        bold = True)
        

    def on_update(self, delta_time):
        """Method that will be called everytime the screen is udpated. 
        This is the method that will make everything work in the game. Will make the 
        scenario, obstacles and the skater move."""

        # Will call the global variable score to be updated as needed
        global score

        # Will update all the sprite lists to make the sprites move
        self.skater_list.update()
        self.obstacles_list.update()
        self.first_scenario_list.update()
        self.scenario_list.update()
        self.physics_engine.update()
        self.school_list.update()    
        self.medicine_list.update()    
        self.enemy_list.update()

        # Creates the text to be displayed for score, lives and, remaining obstacles  
        self.score_text = f"SCORE: {score}"
        self.lives_text = f"LIVES: {self.lives}"
        self.remaining_text = f"REMAINING OBSTACLES: {self.remaining_obstacles}"
      
        
        # Checks if there was a collision with obstacles by calling the arcade check_for_collision_with_list
        # Which will return a list if a collision occured.
        if arcade.check_for_collision_with_list(self.skater, self.obstacles_list):  
            """If there is something inside the list, it will return True and the code below will be executed"""

            # Will take 1 life          
            self.lives -= 1

            # Will set the velocity that the skater will fall when appearing at position 700
            self.skater.velocity[1] = 10   
            # Will place the skater at position 700                        
            self.skater.center_y = 700

            # Reduce the score
            score -= 30
            # Plays the crash sound
            arcade.play_sound(self.sound_crash, volume=constants.VOLUME_EFFECTS)

            # Will check if there is remaining life
            if self.lives == 0:
                # If there is non remaining life:
                # Stop the background sound
                arcade.stop_sound(self.music)
                arcade.play_sound(self.sound_crash, volume=constants.VOLUME_EFFECTS)
                # Sleep the function for 1 second
                time.sleep(1)
                # Display the Game over view
                game_over_view = GameOverView()
                self.window.show_view(game_over_view)

        # Checks if there was a collision withe the moving obstacles by calling the arcade check_for_collision_with_list
        # Which will return a list if a collision occured.
        if arcade.check_for_collision_with_list(self.skater, self.enemy_list):          
            self.lives -= 1
            self.skater.velocity[1] = 10                   
            self.skater.center_y = 700 # We have to imporve this
            score -= 30
            arcade.play_sound(self.sound_crash, volume=constants.VOLUME_EFFECTS)
            if self.lives == 0:
                # If there is non remaining life:
                # Stop the background sound
                arcade.stop_sound(self.music)
                arcade.play_sound(self.sound_crash, volume=constants.VOLUME_EFFECTS)
                # Sleep the function for 1 second
                time.sleep(1)
                # Display the Game over view
                game_over_view = GameOverView()
                self.window.show_view(game_over_view)

        # Will loop through the obstacles list to get the obstacle position      
        for obstacle in self.obstacles_list:
            # Will check is the obstacle is going off the screen
            if obstacle.left < 0:
                # Will give the score according to the obstacles size. That's why the score point is only 1
                # It will continue adding 1 until the obstacle is completly out of the screen and delete from the list
                score += 1

        
        # Checks if there was a collision with the medicine by calling the arcade check_for_collision_with_list
        # Which will return a list if a collision occured.
        if arcade.check_for_collision_with_list(self.skater, self.medicine_list):
            # Will give lives only if the total lives is less than 5
            if self.lives < 5:
                self.lives += 1
            # Will play the sound effect 
            arcade.play_sound(self.sound_live, volume=constants.VOLUME_EFFECTS)
            # Will delete the medicine from the list
            self.medicine_list.pop()

        # Will check if the school was drawn by checking the length of the list and if the 
        # background images stopped to move
        if len(self.school_list) > 0 and self.school.change_x == 0:
            # Will stop the background music
            arcade.stop_sound(self.music)
            # Will play the school bell
            self.sound_bell.play()
            # Pause for 2 seconds
            time.sleep(2)
            # Change the view to the winview
            win = WinView()
            self.window.show_view(win)
        
        # Will add the moving obstacle
        if self.enemy_period == self.round:
            self.add_enemy()
            self.sound_enemy.play()
            self.enemy_period *= 2

        

    def on_key_press(self, symbol, modifiers):
        """Handle user keyboard input
        Q: Quit the game
        SPACE: Jump (If hit 2 times you can double jump)
        Arrows: Move left and right 
        
        Arguments: 
            symbol {int} -- which key was pressed
            modifires {int} -- Which modifiers were pressed
        """
        if symbol == arcade.key.Q:
            arcade.close_window()
               
        elif symbol == arcade.key.LEFT:
            self.skater.change_x = - constants.SPEED
       
        elif symbol == arcade.key.RIGHT:
            self.skater.change_x = constants.SPEED
    
        elif symbol == arcade.key.SPACE:
            # Checks if the skater is on the ground and then allow the jump
            if self.physics_engine.can_jump():
                # Enable 2 jump
                self.physics_engine.enable_multi_jump(2)
                # Will counter how many jumps were made
                self.physics_engine.increment_jump_counter()
                self.skater.change_y = constants.JUMP_SPEED
                arcade.play_sound(self.sound_jump, volume=constants.VOLUME_EFFECTS)



    def on_key_release(self, symbol, modifiers):

        """Called whenever a key is released. """

        if (
            symbol == arcade.key.J
            or symbol == arcade.key.L
            or symbol == arcade.key.LEFT
            or symbol == arcade.key.RIGHT

        ):
            self.skater.change_x = 0
    
    
    def add_obstacle(self, delta_time: float):
        """ Adds a new obstacle to screen.
        
        Arguments: 
            delta_time {float} -- The time has passed since last call """
        if self.round < constants.ROUNDS:
            self.obstacle = Obstacles(40, -10)
            self.obstacles_list.append(self.obstacle)
            self.round += 1
            self.remaining_obstacles -= 1
        elif len(self.school_list) < 1:
            self.add_school()
        else:
            pass


    def add_medicine(self, delta_time: float):
        """ Adds a new medicine to screen.
        Arguments: 
            delta_time {float} -- The time has passed since last call
        """
        if self.round < constants.ROUNDS:
            self.medicine = Medicine(-10)
            self.medicine_list.append(self.medicine)
        else:
            pass
        
       
    
    def add_enemy(self):
        """ Adds an enemy to screen.
        Arguments: 
            delta_time {float} -- The time has passed since last call """
        
        self.enemy = Enemy(15)
        self.enemy_list.append(self.enemy)
        
            
            
    def add_scenario(self, delta_time: float):
        """ Adds a new background to screen.
        
        Arguments: 
            delta_time {float} -- The time has passed since last call """
        if self.round < constants.ROUNDS:    
            if self.scene_turn < 5:
                self.scenario = Scenario(0, -10, self.scene_turn, self.stop)
                self.scenario_list.append(self.scenario)
                self.scene_turn += 1
            elif self.scene_turn == 5:
                self.scenario = Scenario(0, -10, self.scene_turn, self.stop)
                self.scenario_list.append(self.scenario)
                self.scene_turn = 0
        else:
            self.stop = False
            self.scenario = Scenario(0, 0, self.scene_turn, self.stop)
            

    def add_background(self):
        """ Adds the first background when game starts
        """
        self.static_background = arcade.Sprite("project/sprites/background.png", constants.SCALING)
        self.static_background.bottom = 0
        self.static_background.left = 0


    def add_static_scene(self):
        """ Adds the first background when game starts
        """
        self.static_scene = arcade.Sprite("project/sprites/static_street.png", constants.SCALING)
        self.static_scene.bottom = 0
        self.static_scene.left = 0

        
    def add_first_scene(self):
        """ Adds the first background when game starts
        """
        self.first_scenario = First_scenario(0, -10)
        self.first_scenario_list.append(self.first_scenario)
        

    def add_school(self):
        """ Adds the last background (the School) when it reaches the setted number of rounds
        """
        self.school = School(0, -10)
        self.school_list.append(self.school)

        


class GameOverView(arcade.View):
    """Class for game over view. 
    
    Stereotype: interface, information holder"""

    def on_show(self):
        """Method called once this view is displayed"""
        self.width = WIDTH/2
        self.new_line = 45


    def on_draw(self):
        """Method to draw everthing on screen (arcade's method)"""
        # Will call the global variable score to get the final score to display
        global score
        arcade.start_render()
        # Will display the background image for game over
        game_over_background = arcade.Sprite("project/sprites/game_over.jpg", constants.SCALING)
        game_over_background.center_x = constants.SCREEN_WIDTH / 2
        game_over_background.center_y = constants.SCREEN_HEIGHT / 2
        game_over_background.draw()
        
        # Will display the total score
        total_score = f"Total Score: {score}"
        arcade.draw_text(text = total_score,
                    color = (255, 255, 255),
                    start_x = constants.SCREEN_WIDTH / 2 + 80,
                    start_y = constants.SCREEN_HEIGHT / 8 * 5,
                    font_size = 36,
                    font_name = "calibri",
                    bold = True)    


    def on_key_press(self, symbol, modifiers):
        """Handle user keyboard input
        P: Restart the game by calling the director view
        Q: Quit the game 
        
        Arguments: 
            symbol {int} -- which key was pressed
            modifires {int} -- Which modifiers were pressed
        """

        if symbol == arcade.key.P:
            global score
            score = 0
            game_view = Director()
            self.window.show_view(game_view)
        elif symbol == arcade.key.Q:
            arcade.close_window()




class WinView(arcade.View):
    """"Class for the Win view. 
    Stereotype: Interface, information holder"""

    def on_show(self):
        """Method called once this view is displayed"""
        self.width = WIDTH/2
        self.new_line = 45

    def on_draw(self):
        """Method to draw everthing on screen (arcade's method)"""

        # Will call the global variable score to get the final score to display
        global score
        arcade.start_render()
        win_background = arcade.Sprite("project/sprites/win.jpg", constants.SCALING)
        win_background.center_x = constants.SCREEN_WIDTH / 2
        win_background.center_y = constants.SCREEN_HEIGHT / 2
        win_background.draw()
        
        # Display the total score
        total_score = f"Total Score: {score}"
        arcade.draw_text(text = total_score,
                    color = (255, 255, 255),
                    start_x = constants.SCREEN_WIDTH / 2 + 80,
                    start_y = constants.SCREEN_HEIGHT / 8 * 5,
                    font_size = 36,
                    font_name = "calibri",
                    bold = True)    

    def on_key_press(self, symbol, modifiers):
        """Handle user keyboard input
        P: Restart the game by calling the director view
        Q: Quit the game 
        
        Arguments: 
            symbol {int} -- which key was pressed
            modifires {int} -- Which modifiers were pressed
        """
        
        if symbol == arcade.key.P:
            global score
            score = 0
            game_view = Director()
            self.window.show_view(game_view)
        elif symbol == arcade.key.Q:
            arcade.close_window()