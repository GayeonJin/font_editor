#!/usr/bin/python

import sys
import csv

import pygame
import random

from font import *
from gresource import *
from gobject import *

MAX_ROWS = 16
MAX_COLS = 16

MAP_XOFFSET = 10
MAP_YOFFSET = 30

MAP_WIDTH = 20 * MAX_COLS
MAP_HEIGHT = 20 * MAX_ROWS

DEFAULT_CODE = 0x30

class font_bitmap_object :
    def __init__(self, rows, cols) :
        self.map = []

        self.rows = rows
        self.cols = cols
        
        for x in range(self.cols) :
            self.map.append([])
            for y in range(self.rows) :
                self.map[x].append(0)

        self.x_offset = MAP_XOFFSET
        self.y_offset = MAP_YOFFSET

        self.obj_width = int(MAP_WIDTH / self.cols)
        self.obj_height = int(MAP_HEIGHT / self.rows)

        self.code = DEFAULT_CODE

    def get_size(self) :
        return self.rows, self.cols

    def set_rect(self, rect) :
        self.x_offset = rect.x
        self.y_offset = rect.y
        self.obj_width = rect.width / self.cols
        self.obj_height = rect.height /self.rows
       
    def get_padsize(self) :
        pad_width = 2 * self.x_offset + self.cols * self.obj_width 
        pad_height = 2 * self.y_offset + self.rows * self.obj_height
        return (pad_width, pad_height) 

    def update_bitmap(self, code, bitmap) :
        self.code = code
        self.map = bitmap

    def get_cur_code(self) :
        return self.code

    def get_bitmap(self) :
        return self.map

    def get_map_rect(self, x, y) :
        map_rect = pygame.Rect(self.x_offset, self.y_offset, self.obj_width , self.obj_height)

        # map[0][0] is left and bottom
        map_rect.x += x * self.obj_width 
        map_rect.y += y * self.obj_height
        return map_rect        

    def get_pos(self, screen_xy) :
        # map[0][0] is left and top
        for y in range(self.rows) :
            for x in range(self.cols) :
                map_rect = self.get_map_rect(x, y)
                if screen_xy[0] > map_rect.left and screen_xy[0] < map_rect.right :
                    if screen_xy[1] > map_rect.top and screen_xy[1] < map_rect.bottom :      
                        return (x, y)
                    
        return (None, None)

    def toggle(self, x, y) :
        if self.map[x][y] == 1 :
            self.map[x][y] = 0
        else :
            self.map[x][y] = 1

    def set(self, x, y) :
        self.map[x][y] = 1

    def clear(self, x, y) :
        self.map[x][y] = 0 

    def move_next(self, font_length) :
        if self.code < font_length - 1 :
            self.code += 1

    def move_prev(self) :
        if self.code > 0 :
            self.code -= 1

    def draw_info(self, x, y) :
        disp_str = ['font code : ']

        font1 = pygame.font.SysFont(None, 20)
        for i, str in enumerate(disp_str) :
            str += ' %c, (0x%x)'%(self.code, self.code)

            text_suf1 = font1.render(str, True, COLOR_BLUE)
            text_rect1 = text_suf1.get_rect()
            text_rect1.left = x
            text_rect1.top = y
            gctrl.gamepad.blit(text_suf1, text_rect1)        

    def draw(self, real_size = False) :
        # code
        if real_size == False :
            self.draw_info(self.x_offset, 10)

        map_rect = pygame.Rect(self.x_offset, self.y_offset, self.obj_width, self.obj_height)

        # map[0][0] is left and top
        for y in range(self.rows) :
            for x in range(self.cols) :
                if real_size == False :
                    pygame.draw.rect(gctrl.gamepad, COLOR_RED, map_rect, 1, 1)
                if self.map[x][y] == 1 :
                    pygame.draw.rect(gctrl.gamepad, COLOR_BLACK, map_rect)

                map_rect.x += self.obj_width
            map_rect.y += self.obj_height
            map_rect.x = self.x_offset

if __name__ == '__main__' :
    print('font map object')
