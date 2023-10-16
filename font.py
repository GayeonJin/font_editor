#!/usr/bin/python

import sys
import csv

import random

FONT_WIDTH = 16
FONT_HEIGHT = 16

BYTE_PER_PIXEL = 8

FONT_TYPE_ASCII = 0
FONT_TYPE_UNICODE = 0

FONT_NUM_ASCII = 256
FONT_NUM_UNICODE = 65536

class font_object :
    def __init__(self, font_width = FONT_WIDTH, font_height = FONT_HEIGHT, type = FONT_TYPE_ASCII) :
        self.fonts = []

        self.font_type = type
        self.rows = font_width
        self.cols = font_height
        
        self.width_size = int(font_width / BYTE_PER_PIXEL)
        self.font_size = int(self.width_size * font_height) 

        if self.font_type == FONT_TYPE_ASCII :
            self.font_num = FONT_NUM_ASCII
        elif self.font_type == FONT_TYPE_UNICODE :
            self.font_num = FONT_NUM_UNICODE

        for i in range(self.font_num) :
            self.fonts.append([])
            for j in range(self.font_size) :
                self.fonts[i].append(0)

        self.bmp = []
        for x in range(self.cols) :
            self.bmp.append([])
            for y in range(self.rows) :
                self.bmp[x].append(0)

        self.bitmask = [0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40, 0x80]
        self.shiftmask = [0, 1, 2, 3, 4, 5, 6, 7]
        
    def get_font_size(self) :
        return self.rows, self.cols      

    def get_length(self) :
        return self.font_num

    def get_data(self, code) :
        return self.fonts[code]

    def load_bmp(self, code) :
        bmp_data = self.fonts[code]

        #print('load 0x%x'%code)
        #print(bmp_data)

        for i, data in enumerate(bmp_data) :
            x = int(i % self.width_size) * BYTE_PER_PIXEL
            y = int(i / self.width_size)

            for mask in self.bitmask :
                if data & mask != 0 :
                    self.bmp[x][y] = 1
                else :
                    self.bmp[x][y] = 0

                x += 1

        return self.bmp 
    
    def update_bmp(self, code, bmp) :
        self.bmp = bmp

        index = 0
        datas = []
        for y in range(self.cols) :
            for x in range(self.rows) :
                if x % BYTE_PER_PIXEL == 0 :
                    index = int((x / BYTE_PER_PIXEL)  + (y * self.width_size))
                    datas.append(0)
                datas[index] |= (self.bmp[x][y] << self.shiftmask[x % BYTE_PER_PIXEL])

        # print('update 0x%x'%code)
        # print(datas)

        self.fonts[code] = datas 

    def load_file(self, filename = 'default_font.csv') :
        print("load font : " + filename)

        file = open(filename, 'r')
        rows = csv.reader(file)

        print(rows)

        for i, font_data in enumerate(rows) :
            for j, value in enumerate(font_data) :
                self.fonts[i][j] = int(value)

    def save_file(self, filename = 'default_font.csv') :
        print("save font : " + filename)

        with open(filename, 'w') as file:
            #for header in header:
            #    file.write(str(header)+', ')
            #file.write('n')
            for i in range(self.font_num):
                font_data = self.fonts[i]
                for j in range(self.font_size - 1):                    
                    file.write(str(font_data[j])+', ')
                file.write(str(font_data[j+1]))
                file.write('\n')

if __name__ == '__main__' :
    print('font object')
