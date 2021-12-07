
class HandleCollisionsAction:
    """A code template for handling collisions. The responsibility of this class of objects 
    is to update the game state when actor collides.
    
    Stereotype:
        Controller
    """

    def __init__(self):
        
        pass

    def on_obstacles_collision(self, obstacles, player, delta_time: float):
        
        if len(player.collides_with_list(obstacles)) > 0:
            
            return True
            
            
        

