import arcade
from game.game_view import GameView

player_score = 0

class Score:
    # the score increases by one when the player jump over a obstacle
    def __init__(self):

        
        
        pass
    # 
    #   position = (-0.6, 0.4)

    # )
    def collisionDetection(player, player_score, brick, dog):
        if player.collide(brick):
            player_score = 0
        elif player.collide(dog):
            player_score = 0
        else:
            player_score += 1
            print(f"Score: {int(player_score)}", True, "black")



    
    
    
