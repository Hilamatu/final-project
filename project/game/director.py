import arcade
import random

from game import constants
from game.first_scenario import First_scenario
from game.scenario import Scenario
from game.skater import Skater
from game.medicine import Medicine
from game.obstacles import Obstacles
from game.school import School



class Director(arcade.Window):
    def __init__(self):
        super().__init__(constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT, constants.TITLE)
        arcade.set_background_color(arcade.color.LIGHT_BLUE)
        self.skater_list = arcade.SpriteList()
        self.obstacles_list = arcade.SpriteList()
        self.scenario_list = arcade.SpriteList()
        self.ground_list = arcade.SpriteList()
        self.first_scenario_list = arcade.SpriteList()
        self.school_list = arcade.SpriteList()
        self.medicine_list = arcade.SpriteList()

        self.first_scenario = None
        self.scenario = None        
        self.skater = None
        self.obstacle = None
        self.score = 0
        self.score_text = None        
        self.lives = 5
        self.lives_text = None
        self.scene_turn = 0
        self.static_background = None
        self.static_scene = None
        self.round = 0
        self.school = None
        self.stop = True

        #sounds
        self.sound_crash = arcade.load_sound(constants.SOUND_OUCH)
        self.sound_jump = arcade.load_sound(constants.SOUND_JUMP)
       
        

    def setup(self):
        self.skater = Skater()
        arcade.schedule(self.add_obstacle, 1)
        arcade.schedule(self.add_scenario, 8)
        
        self.add_background()
        self.add_static_scene()
        self.add_first_scene()
        
        self.skater_list.append(self.skater)
      
        #Set the skater falling by gravity limit. 
        for x in range(0, constants.SCREEN_WIDTH, constants.SPRITE_SIZE):
            ground = arcade.Sprite("skater/sprites/ground.png", constants.SCALING)
            ground.top = 50
            ground.left = x
            self.ground_list.append(ground)
        self.physics_engine = arcade.PhysicsEnginePlatformer(self.skater, self.ground_list, gravity_constant= constants.GRAVITY) 


      
    def on_draw(self):        
        arcade.start_render()
        self.static_background.draw()
        self.static_scene.draw()
        self.first_scenario_list.draw()
        self.scenario_list.draw()
        self.school_list.draw()
        self.skater_list.draw()
        self.obstacles_list.draw()
        arcade.draw_text(text = str(self.score_text),
                        color = (105, 105, 105),
                        start_x = constants.SCREEN_WIDTH - 200,
                        start_y = constants.SCREEN_HEIGHT - 50,
                        font_size = 24, font_name = "calibri",
                        bold = True)
        arcade.draw_text(text = str(self.lives_text),
                        color = (105, 105, 105),
                        start_x = 50,
                        start_y = constants.SCREEN_HEIGHT - 50,
                        font_size = 24, font_name = "calibri",
                        bold = True)
        
            
        

    def on_update(self, delta_time):
        self.skater_list.update()
        self.obstacles_list.update()
        self.first_scenario_list.update()
        self.scenario_list.update()
        self.physics_engine.update()
        self.school_list.update()        

        self.score_text = f"SCORE: {self.score}"
        self.lives_text = f"LIVES: {self.lives}"
      
        if arcade.check_for_collision_with_list(self.skater, self.obstacles_list):
            self.lives -= 1
            self.skater.center_y = 800 # We have to imporve this
            self.score -= 30
            self.sound_crash.play()

        for obstacle in self.obstacles_list:
            if obstacle.left < 0:
                self.score += 1
                
            
        


  
    def on_key_press(self, symbol, modifiers):
        """Handle user keyboard input
        ESCAPE: Quit the game
        Arrows: Move left and right 
        
        Arguments: 
            symbol {int} -- which key was pressed
            modifires {int} -- Which modifiers were pressed
        """
        if symbol == arcade.key.ESCAPE:
            arcade.close_window()
        
        elif symbol == arcade.key.LEFT:
            self.skater.change_x = -5

        elif symbol == arcade.key.RIGHT:
            self.skater.change_x = 5
        
        elif symbol == arcade.key.SPACE:
            if self.physics_engine.can_jump():
                self.skater.change_y = constants.JUMP_SPEED
                self.sound_jump.play()



    def on_key_release(self, symbol, modifiers):

        """Called whenever a key is pressed. """

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
            x = random.randint(40, 300)
            self.obstacle = Obstacles(40, x, -10)
            self.obstacles_list.append(self.obstacle)
            self.round += 1
        elif len(self.school_list) < 1:
            self.add_school()
        else:
            pass
            
            



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
        self.static_background = arcade.Sprite("skater/sprites/background.png", constants.SCALING)
        self.static_background.bottom = 0
        self.static_background.left = 0


    def add_static_scene(self):
        """ Adds the first background when game starts
        """
        self.static_scene = arcade.Sprite("skater/sprites/static_street.png", constants.SCALING)
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