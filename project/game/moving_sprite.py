import arcade

class MovingSprite(arcade.Sprite):
    """ Base class for all moving sprites"""


    def udpate(self):
        """Update the position of the sprite
        when it moves off screen to the left, remove it """

        # Move the sprite
        super().update()

        # remove it from screen
        if self < 0:
            self.remove_from_sprite_lists()
    
