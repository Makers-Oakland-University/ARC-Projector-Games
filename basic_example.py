#!/usr/bin/env python3

import pygame
import random
import numpy as np
import sys
from location_parser import LocationParser
            
#lidar positioner that handles the parsing of the file into a tuple array. 
#see location_parser.py for parameter description.
lidar_positioner = LocationParser()

#start pygame
pygame.init()
SCREEN_WIDTH, SCREEN_HEIGHT = 1920 , 1080 #render resolution, this will be scaled to the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN | pygame.SCALED)

running = True #indicates the game is currently running
clock = pygame.time.Clock() #used to moduleate the frame rate and keep successive actions constant

while running:

    #check whether the user quit the game 
    # if so set running to False so we can close on the next iteration
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Fill the background with black
    screen.fill((0,0,0, 1))

    #get positions from the LocationParser
    positions = lidar_positioner.getPositions()
    for xy in positions: 
        pygame.draw.circle(screen, (0,0,255), xy, 10) 

    #write pixels to the display
    pygame.display.flip()
    
    #wait until next game tick
    clock.tick(120)

#exit
pygame.quit()
sys.exit()
