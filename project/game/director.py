
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
        arcade.draw_text("Welcome to SKATER", WIDTH / 2, HEIGHT / 2,
        arcade.color.BLACK, font_size=50, anchor_x="center", font_name="Kenney Blocks")
        arcade.draw_text("Hit ENTER to start the game or H for help and Q to quit the game", WIDTH / 2, HEIGHT / 2 - 75,
        arcade.color.GRAY, font_size=20, anchor_x="center")

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
        arcade.set_background_color(arcade.color.SKY_BLUE)
        self.width = WIDTH/2
        self.new_line = 45


    def on_draw(self):
        arcade.start_render()
        text = "Hurry up, you need to get to school in time!\n"\
        "But be careful, there are many obstacle in the way!\n"\
        "\n"\
        "Instruction:\n"\
        "You need to jump over the obstacles and arrive to the school.\n"\
        "You have 5 lives and if you collide with an obstacle, you will lose 1 life and 30 points.\n"\
        "\n"\
        "Commands list: \n"\
        "- Arrows: Move to the right or left\n"\
        "- Space: Jump "
        start_y = 660
        arcade.draw_text(text, 640, start_y,
                         arcade.color.BLACK, font_size=30, anchor_x="center",multiline=True, width=900)

        arcade.draw_text("Hit R to return to main menu", WIDTH / 2, 80,
                         arcade.color.GRAY, font_size=35, anchor_x="center")


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


        self.first_scenario = None
        self.scenario = None        
        self.skater = None
        self.obstacle = None
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
        self.sound_riding = arcade.load_sound(constants.SOUND_RIDING)

    def on_show(self):
        arcade.set_background_color(arcade.color.LIGHT_BLUE)

    # def setup(self):
        self.skater = Skater()
        arcade.schedule(self.add_obstacle, 1)
        arcade.schedule(self.add_scenario, 8)
        
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
        global score
        self.skater_list.update()
        self.obstacles_list.update()
        self.first_scenario_list.update()
        self.scenario_list.update()
        self.physics_engine.update()
        self.school_list.update()
              

        self.score_text = f"SCORE: {score}"
        self.lives_text = f"LIVES: {self.lives}"
      
        hit_list = arcade.check_for_collision_with_list(self.skater, self.obstacles_list)
        if hit_list:
            self.lives -= 1
                           
            self.skater.center_y = 700 # We have to imporve this
            score -= 30
            arcade.play_sound(self.sound_crash)
        
            if self.lives == 0:
                arcade.play_sound(self.sound_crash)
                time.sleep(1)
                game_over_view = GameOverView()
                self.window.show_view(game_over_view)

        for obstacle in self.obstacles_list:
            if obstacle.left < 0:
                score += 1

        if len(self.school_list) >= 1 and self.school.change_x == 0:
            win = WinView()
            self.window.show_view(win)

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
            self.skater.change_x = -8
            if self.skater.bottom <= 53:
                arcade.play_sound(self.sound_riding)

        elif symbol == arcade.key.RIGHT:
            self.skater.change_x = 8
            if self.skater.bottom <= 53:
                arcade.play_sound(self.sound_riding)
    
        elif symbol == arcade.key.SPACE:
            if self.physics_engine.can_jump():
                self.skater.change_y = constants.JUMP_SPEED
                arcade.play_sound(self.sound_jump)



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
        arcade.set_background_color(arcade.color.SKY_BLUE)
        self.width = WIDTH/2
        self.new_line = 45


    def on_draw(self):
        global score
        arcade.start_render()
        text = "Game Over"

        arcade.draw_text(text, WIDTH / 2, HEIGHT / 2,
                         arcade.color.BLACK, font_size=70, anchor_x="center", font_name="Kenney Blocks")
        
        total_score = f"Total Score: {score}"

        arcade.draw_text(total_score, WIDTH / 2, HEIGHT / 2 - 90,
                         arcade.color.BLACK, font_size=50, anchor_x="center")
        

        arcade.draw_text("Hit P to play again or Q to end the game",  WIDTH / 2, HEIGHT / 2 - 170,
                         arcade.color.GRAY, font_size=35, anchor_x="center")


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
        arcade.set_background_color(arcade.color.SKY_BLUE)
        self.width = WIDTH/2
        self.new_line = 45

    def on_draw(self):

        arcade.start_render()
        text = "You've arrived the school!!"

        arcade.draw_text(text, WIDTH / 2, HEIGHT / 2,
                            arcade.color.BLACK, font_size=40, anchor_x="center", font_name="Kenney Blocks")
    

        arcade.draw_text("Hit P to play again or Q to end the game",  WIDTH / 2, HEIGHT / 2 - 170,
                        arcade.color.GRAY, font_size=25, anchor_x="center")

    def on_key_press(self, symbol, modifiers):
        if symbol == arcade.key.P:
            global score
            score = 0
            game_view = Director()
            self.window.show_view(game_view)
        elif symbol == arcade.key.Q:
            arcade.close_window()