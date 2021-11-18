import arcade
import arcade.gui
import constants
from game_view import GameView


class StartView(arcade.View):
    """Displays the main window with the "Start Game" and "How to Play" button."""
    def __init__(self):
        """Since view does not support width and height, it just calls the parent init"""
        super().__init__()

    def on_show(self):
        
        self._start_button = Start
        self._how_to_play_button = howToPlay

        # UIManager to handle the UI. 
        self.manager = arcade.gui.UIManager()
        self.manager.enable()

        # Set background color
        arcade.set_background_color(arcade.color.BLUE_GRAY)

        # Create a vertical BoxGroup to align buttons
        self.v_box = arcade.gui.UIBoxLayout()

        # Create the start button and add it to v_box to align
        start_button = self._start_button(text="Start Game", width=200)
        self.v_box.add(start_button.with_space_around(bottom=20))
        

        # Create the how_to_play_button and add it to v_box to align
        how_to_play_button = self._how_to_play_button(text="How to play", width=200)
        self.v_box.add(how_to_play_button.with_space_around(bottom=20))

        # Create a widget to hold the v_box widget, that will center the buttons
        self.manager.add(
            arcade.gui.UIAnchorWidget(
                anchor_x="center_x",
                anchor_y="center_y",
                child=self.v_box))
        
    def on_draw(self):
        arcade.start_render()
        self.manager.draw()


class InstructionView(arcade.View):
    """View to show the game instruction"""

    def on_show(self):
        """This method will run once the view changes"""

        self._return_button = Return

        self.manager = arcade.gui.UIManager()
        self.manager.enable()

        arcade.set_background_color(arcade.color.BLUE_GRAY)

       

        # Create a vertical BoxGroup to align buttons
        self.v_box = arcade.gui.UIBoxLayout()

        # Create a text label
        ui_text_label = arcade.gui.UITextArea(text="Welcome to SKATER",
                                              width=450,
                                              height=40,
                                              font_size=24,
                                              font_name="Kenney Blocks")
        self.v_box.add(ui_text_label.with_space_around(bottom=20))

        text = "Hurry up, you need to get to school in time! But be careful, there are many obstacle in the way!\n"\
        "\n"\
        "Instruction:\n"\
        "You need to jump over the obstacles and arrive to the school.\n"\
        "You have 3 lives and if you collide with an obstacle, you will lose 1 life.\n"\
        "\n"\
        "Commands list: \n"\
        "- Arrows: Move to the right or left\n"\
        "- Space: Jump " 
        ui_text_label = arcade.gui.UITextArea(text=text,
                                              width=500,
                                              height=300,
                                              font_size=14,
                                              font_name="Arial")
        self.v_box.add(ui_text_label.with_space_around(bottom=0))

        return_view = self._return_button(text="Return", width=200)
        self.v_box.add(return_view.with_space_around(bottom=20))

        self.manager.add(
            arcade.gui.UIAnchorWidget(
                anchor_x="center_x",
                anchor_y="center_y",
                child=self.v_box)
        )


    def on_draw(self):
        """ Draw this view """
        arcade.start_render()
        self.manager.draw()
        arcade.draw_text("How to play", constants.SCREEN_WIDTH / 2, constants.SCREEN_HEIGHT - 70,
                        arcade.color.WHITE, font_size=50, anchor_x="center")



class Return(arcade.gui.UIFlatButton):
    """A class to handle the Return button clik"""
    def on_click(self, event: arcade.gui.UIOnClickEvent):
        start_view = StartView()
        window.show_view(start_view)

class howToPlay(arcade.gui.UIFlatButton):
    """A class to handle the how_to_play button click"""
    def on_click(self, event: arcade.gui.UIOnClickEvent):
        
        instruction = InstructionView()
        window.show_view(instruction)

class Start(arcade.gui.UIFlatButton):
    def on_click(self, event: arcade.gui.UIOnClickEvent):
        start = GameView()
        window.show_view(start)

if __name__ == "__main__":
    window = arcade.Window(constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT, title=constants.SCREEN_TITLE)
    start_view = StartView()
    window.show_view(start_view)

    arcade.run()