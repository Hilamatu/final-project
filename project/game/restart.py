from game import constants
from game import handle_collisions_action.py
from game.action import Action
#from game.game_view import GameView
import arcade
import arcade.gui

def restart():
    user_input = input("Would you like to play again? Type 'Yes' or 'No'\n\n")

    if user_input.lower() == "no": # Converts input to lowercase for comparison
        return False
    elif user_input.lower() == "yes":
        return True

    
 startGame()
