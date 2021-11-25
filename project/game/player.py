import arcade

class Player:
    def __init__(self):
        self.player = arcade.Sprite("../final-project/project/sprite/skater.png", center_x=100, center_y=200)

    def on_key_press(self, symbol, modifiers):
        """Handle user keyboard input
        Q: Quit the game
        P: Pause the game
        I/J/K/L: Move up, left, down, right 
        Arrows: Move up, left, down, right 
        
        Arguments: 
            symbol {int} -- which key was pressed
            modifires {int} -- Which modifiers were pressed
        """

        if symbol == arcade.key.Q:
            # Quit immediatelly
            arcade.close_window()
        
        if symbol == arcade.key.P:
            self.paused = not self.paused
        
        if symbol == arcade.key.J or symbol == arcade.key.LEFT:
            self.player.change_x = -200
        
        if symbol == arcade.key.L or symbol == arcade.key.RIGHT:
            self.player.change_x = 200
