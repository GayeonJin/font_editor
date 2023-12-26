#!/usr/bin/python

import os
import sys
import csv

import pygame
import random
from time import sleep

from gresource import *

from font import *
from font_bitmap import *
from cursor import *

TITLE_STR = "Bitmap Font Editor"

MOVE_CODE_PREV = 1
MOVE_CODE_NEXT = 2

INFO_HEIGHT = 40
INFO_OFFSET = 10
INFO_FONT = 14

def draw_info() :
    font = pygame.font.SysFont('Verdana', INFO_FONT)
    info = font.render('F1 : load font,  F2 : save font', True, COLOR_BLACK)
    info1 = font.render('1 : prev, 2 : next, space : toggle', True, COLOR_BLACK)

    pygame.draw.rect(gctrl.surface, COLOR_PURPLE, (0, gctrl.height - INFO_HEIGHT, gctrl.width, INFO_HEIGHT))
    gctrl.surface.blit(info, (INFO_OFFSET * 2, gctrl.height - 2 * INFO_FONT - INFO_OFFSET))
    gctrl.surface.blit(info1, (INFO_OFFSET * 2, gctrl.height - INFO_FONT - INFO_OFFSET))

def draw_message(str) :
    font = pygame.font.Font('freesansbold.ttf', 40)
    text_suf = font.render(str, True, COLOR_BLACK)
    text_rect = text_suf.get_rect()
    text_rect.center = ((gctrl.width / 2), (gctrl.height / 2))

    gctrl.surface.blit(text_suf, text_rect)
    pygame.display.update()
    sleep(2)

def terminate() :
    pygame.quit()
    sys.exit()

def edit_font() :
    global clock
    global font_bitmap, obj_font

    cursor = cursor_object(font_bitmap)
    cursor.x = 0
    cursor.y = 0

    direction = 0
    
    pre_x = 0
    pre_y = 0
    mouse_drag = False

    change_code = 0
    pixel_toggel = 0
    edit_exit = False
    while not edit_exit :
        for event in pygame.event.get() :
            if event.type == pygame.QUIT :
                edit_exit = True

            if event.type == pygame.KEYUP :
                if event.key == pygame.K_UP:
                    direction = cursor.CURSOR_MOVE_UP
                elif event.key == pygame.K_DOWN :
                    direction = cursor.CURSOR_MOVE_DOWN
                elif event.key == pygame.K_LEFT :
                    direction = cursor.CURSOR_MOVE_LEFT
                elif event.key == pygame.K_RIGHT :
                    direction = cursor.CURSOR_MOVE_RIGHT
                elif event.key == pygame.K_SPACE :
                    pixel_toggel = 1
                elif event.key == pygame.K_1 :
                    change_code = MOVE_CODE_PREV
                elif event.key == pygame.K_2 :
                    change_code = MOVE_CODE_NEXT
                elif event.key == pygame.K_F1 :               
                    obj_font.load_file()
                    font_bitmap.map = obj_font.load_bmp(font_bitmap.code)
                elif event.key == pygame.K_F2 :
                    obj_font.update_bmp(font_bitmap.code, font_bitmap.map) 
                    obj_font.save_file()
                elif event.key == pygame.K_x :
                    return
            elif event.type == pygame.MOUSEBUTTONDOWN :
                l_button, wheel, r_button = pygame.mouse.get_pressed()
                mouse_pos = pygame.mouse.get_pos()
                x, y = font_bitmap.get_pos(mouse_pos)
                if x != None or y != None :
                    mouse_drag = True
                    cursor.set_pos(x, y)
                    if l_button :
                        font_bitmap.set(cursor.x, cursor.y)
                    elif r_button :
                        font_bitmap.clear(cursor.x, cursor.y)
                    pre_x = x
                    pre_y = y                    
            elif event.type == pygame.MOUSEMOTION :
                if mouse_drag == True :
                    mouse_pos = pygame.mouse.get_pos()
                    x, y = font_bitmap.get_pos(mouse_pos)
                    if x != None or y != None :
                        if pre_x != x or pre_y != y :
                            cursor.set_pos(x, y)
                            if l_button :
                                font_bitmap.set(cursor.x, cursor.y) 
                            elif r_button :
                                font_bitmap.clear(cursor.x, cursor.y)                           
                            pre_x = x
                            pre_y = y
            elif event.type == pygame.MOUSEBUTTONUP :
                mouse_drag = False
                mouse_pos = pygame.mouse.get_pos()
                x, y = font_bitmap.get_pos(mouse_pos)
                if x != None or y != None :
                    if pre_x != x or pre_y != y :
                        cursor.set_pos(x, y)
                        if l_button :
                            font_bitmap.set(cursor.x, cursor.y)
                        elif r_button :
                            font_bitmap.clear(cursor.x, cursor.y)                          
                        pre_x = x
                        pre_y = y

        # Load the font
        if change_code == MOVE_CODE_NEXT :
            obj_font.update_bmp(font_bitmap.code, font_bitmap.map)
            font_bitmap.move_next(obj_font.get_length())
            font_bitmap.map = obj_font.load_bmp(font_bitmap.code)
        elif change_code == MOVE_CODE_PREV :
            obj_font.update_bmp(font_bitmap.code, font_bitmap.map) 
            font_bitmap.move_prev()
            font_bitmap.map = obj_font.load_bmp(font_bitmap.code)

        change_code = 0

        # Move cursor
        if direction != 0 :
            cursor.move(direction)
            direction = 0

        # Change pixel
        if pixel_toggel != 0 :
            font_bitmap.toggle(cursor.x, cursor.y)
            pixel_toggel = 0
            
        # Clear gamepad
        gctrl.surface.fill(COLOR_WHITE)

        # Draw font_bitmap
        font_bitmap.draw()
 
        small_font_bitmap.update_bitmap(font_bitmap.get_cur_code(), font_bitmap.get_bitmap())
        small_font_bitmap.draw(True)

        # Draw cursor
        cursor.draw_rect(COLOR_BLACK, 1)

        # Draw Info
        draw_info()

        pygame.display.update()
        clock.tick(60)

def start_font_edit() :
    # Clear gamepad
    gctrl.surface.fill(COLOR_WHITE)

    font = pygame.font.Font('freesansbold.ttf', 20)
    text_suf = font.render(TITLE_STR, True, COLOR_BLACK)
    text_rect = text_suf.get_rect()
    text_rect.center = ((gctrl.width / 2), (gctrl.height / 2))
    gctrl.surface.blit(text_suf, text_rect)

    help_str = ['e : edit bitmap font',
                'x : exit']

    font1 = pygame.font.SysFont(None, 25)
    for i, help in enumerate(help_str) :
        text_suf1 = font1.render(help, True, COLOR_BLUE)
        text_rect1 = text_suf1.get_rect()
        text_rect1.top = text_rect.bottom + 50 + i * 25
        text_rect1.centerx = gctrl.width / 2
        gctrl.surface.blit(text_suf1, text_rect1)

    while True :
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_ESCAPE:
                    terminate()
                elif event.key == pygame.K_e :
                    return 'edit'
                elif event.key == pygame.K_x :
                    terminate()

        pygame.display.update()
        clock.tick(60)    
       
def init_font_edit() :
    global clock
    global font_bitmap, small_font_bitmap, obj_font

    # font 
    obj_font = font_object(FONT_WIDTH, FONT_HEIGHT)

    pygame.init()
    clock = pygame.time.Clock()

    # font bitmap
    font_bitmap = font_bitmap_object(MAX_ROWS, MAX_COLS)
    (pad_width, pad_height) = font_bitmap.get_padsize()

    small_font_bitmap = font_bitmap_object(MAX_ROWS, MAX_COLS)
    rect = pygame.Rect(pad_width - 40, 10, 16, 16)
    small_font_bitmap.set_rect(rect)

    pad_height += INFO_HEIGHT

    gctrl.set_surface(pygame.display.set_mode((pad_width, pad_height)))
    pygame.display.set_caption(TITLE_STR)

if __name__ == '__main__' :
    init_font_edit()
    while True :
        mode = start_font_edit()
        if mode == 'edit' :
            edit_font()

