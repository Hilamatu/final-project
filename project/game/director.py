
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



WIDTH = constants.SCREEN_WIDTH
HEIGHT = constants.SCREEN_HEIGHT

score = 0

def main():
    window = arcade.Window(WIDTH, HEIGHT, "Skater")
    menu_view = MenuView()
    window.show_view(menu_view)
    arcade.run()


class MenuView(arcade.View):
    def on_show(self):
        arcade.set_background_color(arcade.color.SKY_BLUE)

    def on_draw(self):
        arcade.start_render()
        start_background = arcade.Sprite("project/sprites/start.jpg", constants.SCALING)
        start_background.center_x = constants.SCREEN_WIDTH / 2
        start_background.center_y = constants.SCREEN_HEIGHT / 2
        start_background.draw()

    def on_key_press(self, symbol, modifiers):
        if symbol == arcade.key.H:
            instructions_view = InstructionView()
            self.window.show_view(instructions_view)
        elif symbol == arcade.key.ENTER:
            director = Director()
            self.window.show_view(director)
        elif symbol == arcade.key.Q:
            arcade.close_window()




class InstructionView(arcade.View):
    def on_show(self):
        self.width = WIDTH/2
        self.new_line = 45

    def on_draw(self):
        arcade.start_render()
        instructions_background = arcade.Sprite("project/sprites/instructions.jpg", constants.SCALING)
        instructions_background.center_x = constants.SCREEN_WIDTH / 2
        instructions_background.center_y = constants.SCREEN_HEIGHT / 2
        instructions_background.draw()

    def on_key_press(self, symbol, modifiers):
        if symbol == arcade.key.R:
            menu_view = MenuView()
            self.window.show_view(menu_view)




class Director(arcade.View):
    def __init__(self):
        super().__init__()
        self.skater_list = arcade.SpriteList()
        self.obstacles_list = arcade.SpriteList()
        self.scenario_list = arcade.SpriteList()
        self.ground_list = arcade.SpriteList()
        self.first_scenario_list = arcade.SpriteList()
        self.school_list = arcade.SpriteList()
        self.medicine_list = arcade.SpriteList()
        self.enemy_list = arcade.SpriteList()

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
        

        #sounds
        self.sound_crash = arcade.load_sound(constants.SOUND_OUCH)
        self.sound_live = arcade.load_sound(constants.SOUND_LIVE)
        self.sound_jump = arcade.load_sound(constants.SOUND_JUMP)
        self.sound_enemy = arcade.load_sound(constants.SOUND_ENEMY)
        self.sound_bell = arcade.load_sound(constants.SOUND_BELL)
        self.sound_background = arcade.load_sound(constants.SOUND_BACKGROUND, streaming=True)

    def on_show(self):
        arcade.set_background_color(arcade.color.LIGHT_BLUE)    
        self.skater = Skater()
        arcade.schedule(self.add_obstacle, 1.1)
        arcade.schedule(self.add_scenario, 8)
        arcade.schedule(self.add_medicine, random.randint(8, 15))
        

        self.music = arcade.play_sound(self.sound_background, volume=constants.VOLUME_BACKGROUND, looping=True)
        
        
        self.add_background()
        self.add_static_scene()
        self.add_first_scene()
        
        self.skater_list.append(self.skater)
    
        #Set the skater falling by gravity limit. 
        for x in range(0, constants.SCREEN_WIDTH, constants.SPRITE_SIZE):
            ground = arcade.Sprite("project/sprites/ground.png", constants.SCALING)
            ground.top = 50
            ground.left = x
            self.ground_list.append(ground)
            self.physics_engine = arcade.PhysicsEnginePlatformer(self.skater, self.ground_list, gravity_constant= self._gravity) 

        
         
            

    def on_draw(self):
        arcade.start_render()              
        self.static_background.draw()
        self.static_scene.draw()
        self.first_scenario_list.draw()
        self.scenario_list.draw()
        self.school_list.draw()
        self.skater_list.draw()
        self.obstacles_list.draw()
        self.medicine_list.draw()
        self.enemy_list.draw()
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
        global score
        self.skater_list.update()
        self.obstacles_list.update()
        self.first_scenario_list.update()
        self.scenario_list.update()
        self.physics_engine.update()
        self.school_list.update()    
        self.medicine_list.update()    
        self.enemy_list.update()  
        self.score_text = f"SCORE: {score}"
        self.lives_text = f"LIVES: {self.lives}"
      
        
        if arcade.check_for_collision_with_list(self.skater, self.obstacles_list):            
            self.lives -= 1
            self.skater.velocity[1] = 0                           
            self.skater.center_y = 700 # We have to imporve this
            score -= 30
            arcade.play_sound(self.sound_crash, volume=constants.VOLUME_EFFECTS)
            if self.lives == 0:
                arcade.stop_sound(self.music)
                arcade.play_sound(self.sound_crash, volume=constants.VOLUME_EFFECTS)
                time.sleep(1)
                game_over_view = GameOverView()
                self.window.show_view(game_over_view)



        if arcade.check_for_collision_with_list(self.skater, self.enemy_list):          
            self.lives -= 1
            self.skater.velocity[1] = 0                           
            self.skater.center_y = 700 # We have to imporve this
            score -= 30
            arcade.play_sound(self.sound_crash, volume=constants.VOLUME_EFFECTS)


                
        for obstacle in self.obstacles_list:
            if obstacle.left < 0:
                score += 1
        

        if arcade.check_for_collision_with_list(self.skater, self.medicine_list):
            if self.lives < 5:
                self.lives += 1
            arcade.play_sound(self.sound_live, volume=constants.VOLUME_EFFECTS)
            self.medicine_list.pop()


        if len(self.school_list) > 0 and self.school.change_x == 0:
            arcade.stop_sound(self.music)
            self.sound_bell.play()
            time.sleep(2)
            win = WinView()
            self.window.show_view(win)

        if self.enemy_period == self.round:
            self.add_enemy()
            self.sound_enemy.play()
            self.enemy_period *= 2

        

    def on_key_press(self, symbol, modifiers):
        """Handle user keyboard input
        ESCAPE: Quit the game
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
            if self.physics_engine.can_jump():
                self.skater.change_y = constants.JUMP_SPEED
                arcade.play_sound(self.sound_jump, volume=constants.VOLUME_EFFECTS)



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
            self.obstacle = Obstacles(40, -10)
            self.obstacles_list.append(self.obstacle)
            self.round += 1
        elif len(self.school_list) < 1:
            self.add_school()
        else:
            pass


    def add_medicine(self, delta_time: float):
        """ Adds a new medicine to screen.
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
    def on_show(self):
        self.width = WIDTH/2
        self.new_line = 45


    def on_draw(self):
            global score
            arcade.start_render()
            game_over_background = arcade.Sprite("project/sprites/game_over.jpg", constants.SCALING)
            game_over_background.center_x = constants.SCREEN_WIDTH / 2
            game_over_background.center_y = constants.SCREEN_HEIGHT / 2
            game_over_background.draw()
            
            total_score = f"Total Score: {score}"
            arcade.draw_text(text = total_score,
                        color = (255, 255, 255),
                        start_x = constants.SCREEN_WIDTH / 2 + 80,
                        start_y = constants.SCREEN_HEIGHT / 8 * 5,
                        font_size = 36,
                        font_name = "calibri",
                        bold = True)    


    def on_key_press(self, symbol, modifiers):
        if symbol == arcade.key.P:
            global score
            score = 0
            game_view = Director()
            self.window.show_view(game_view)
        elif symbol == arcade.key.Q:
            arcade.close_window()




class WinView(arcade.View):    
    def on_show(self):
        self.width = WIDTH/2
        self.new_line = 45

    def on_draw(self):
        global score
        arcade.start_render()
        win_background = arcade.Sprite("project/sprites/win.jpg", constants.SCALING)
        win_background.center_x = constants.SCREEN_WIDTH / 2
        win_background.center_y = constants.SCREEN_HEIGHT / 2
        win_background.draw()
        
        total_score = f"Total Score: {score}"
        arcade.draw_text(text = total_score,
                    color = (255, 255, 255),
                    start_x = constants.SCREEN_WIDTH / 2 + 80,
                    start_y = constants.SCREEN_HEIGHT / 8 * 5,
                    font_size = 36,
                    font_name = "calibri",
                    bold = True)    

    def on_key_press(self, symbol, modifiers):
        if symbol == arcade.key.P:
            global score
            score = 0
            game_view = Director()
            self.window.show_view(game_view)
        elif symbol == arcade.key.Q:
            arcade.close_window()