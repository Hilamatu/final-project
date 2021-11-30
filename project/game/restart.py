import arcade
import random
import time
import arcade.gui
from game.handle_collisions_action import HandleCollisionsAction
from game import constants
from game.moving_sprite import MovingSprite
import pygame
import sys
    
# initializing the constructor
pygame.init()
  
# screen resolution
res = (720,720)
  
# opens up a window
screen = pygame.display.set_mode(res)
  
# white color
color = (255,255,255)
  
# light shade of the button
color_light = (170,170,170)
  
# dark shade of the button
color_dark = (100,100,100)
  
# stores the width of the
# screen into a variable
width = screen.get_width()
  
# stores the height of the
# screen into a variable
height = screen.get_height()
  
# defining a font
smallfont = pygame.font.SysFont('Corbel',35)
  
# rendering a text written in
# this font
text = smallfont.render('RESTART' , True , color)
  
while True:
      
    for ev in pygame.event.get():
          
        if ev.type == pygame.RESTART:
            pygame.restart()
              
        #checks if a mouse is clicked
        if ev.type == pygame.MOUSEBUTTONDOWN:
              
            #if the mouse is clicked on the
            # button the game is restarted
            if width/2 <= mouse[0] <= width/2+140 and height/2 <= mouse[1] <= height/2+40:
                pygame.restart()
                  
    # restarts the game
    pygame.init()
      
    # stores the (x,y) coordinates into
    # the variable as a tuple
    mouse = pygame.mouse.get_pos()
      
    # if mouse is hovered on a button it
    # changes to lighter shade 
    if width/2 <= mouse[0] <= width/2+140 and height/2 <= mouse[1] <= height/2+40:
        pygame.draw.rect(screen,color_light,[width/2,height/2,140,40])
          
    else:
        arcade.close_window()
      
    # superimposing the text onto our button
    screen.blit(text , (width/2+50,height/2))
      
    # updates the frames of the game
    pygame.display.update()
