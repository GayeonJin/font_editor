#!/usr/bin/python

import sys
import time
import pygame

COLOR_BLACK = (0, 0, 0)
COLOR_WHITE = (255, 255, 255)
COLOR_RED = (255, 0, 0)
COLOR_BLUE = (0, 0, 255)
COLOR_PURPLE = (100,100,200)

resource_path = ''

class game_ctrl :
    def __init__(self) :
        self.surface = None 
        self.width = 640
        self.height = 320

    def set_surface(self, surface) :
        self.surface = surface
        self.width = surface.get_width()
        self.height = surface.get_height()

    def save_scr_capture(self, prefix) :
        pygame.image.save(self.gamepad,(prefix + time.strftime('%Y%m%d%H%M%S')+ '.jpg'))

gctrl = game_ctrl()

if __name__ == '__main__' :
    print('font resoure')