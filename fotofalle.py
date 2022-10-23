#!/usr/bin/python3
# -*- coding: utf-8 -*-

#********************************************************************************
#
# This is the "foto trap" control script.
#
# Module        : main module, fotofalle.py
# Author        : Swen Hopfe (dj)
# Design        : 2022-09-04
# Last modified : 2022-10-01
#
# The python script works with camera, OLED and several external hardware
# and was tested on Raspberry Pi Zero W (1/2).
#
#********************************************************************************

import time
import datetime
import random
import sys
import os
import subprocess
import board
import smbus
from PIL import Image, ImageDraw, ImageFont
import adafruit_ssd1306
from picamera import PiCamera

#--------------------------------------------------------------------------------
# clear display

def display_clear():
    global draw
    global oled
    global image
    draw.rectangle((0, 0, oled.width, oled.height), outline=0, fill=0)
    oled.image(image)
    oled.show()
    return(True)

#--------------------------------------------------------------------------------
# display text on standard position

def display_postext(pos, dstr):
    global draw
    global oled
    global image
    global font5

    # Draw the text
    if(pos == 1):
        draw.text((6, 0), dstr, font=font5, fill=255)
    elif(pos == 2):
        draw.text((6, 16), dstr, font=font5, fill=255)
    elif(pos == 3):
        draw.text((6, 32), dstr, font=font5, fill=255)
    elif(pos == 4):
        draw.text((6, 48), dstr, font=font5, fill=255)
    # Display image
    oled.image(image)
    oled.show()

    return(True)

#--------------------------------------------------------------------------------
# Display splash screen

def display_splash():
    global draw
    global oled
    global image
    global font1,font4

    draw.rectangle((0, 0, oled.width-1, oled.height-1), outline=255, fill=0)
    draw.text((6, 12), " foto_trap", font=font1, fill=255)
    draw.text((27, 45), "R1.0 09.22", font=font4, fill=255)
    oled.image(image)
    oled.show()

    return(True)

#--------------------------------------------------------------------------------
# program entry
#--------------------------------------------------------------------------------

if __name__ == "__main__":

    # setting up I2C and OLED
    i2c = smbus.SMBus(1)
    bi2c = board.I2C()
    oled = adafruit_ssd1306.SSD1306_I2C(128, 64, bi2c, addr=0x3C)

    # font loading
    font1 = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 22)
    font2 = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 17)
    font3 = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 18)
    font4 = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 14)
    font5 = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 15)

    # clear display, create blank image for drawing
    oled.fill(0)
    oled.show()
    image = Image.new("1", (oled.width, oled.height))
    draw = ImageDraw.Draw(image)

#----------------------------------

    # greetings
    display_splash()

#----------------------------------

    # capture settings
    camera = PiCamera()
    time.sleep(1)
    camera.resolution = (2592, 1944)
    camera.rotation = 180
    time.sleep(1)

    # path names with date and random
    rnstr = str(random.randint(1,999999))
    rnstr_fill = rnstr.zfill(6)
    now = datetime.datetime.now()
    dstr = now.strftime("_%Y%m%d_%H%M%S_")
    fname = "/home/pi/scripts/images/img" + dstr + rnstr_fill + ".jpg"

    # capture
    camera.capture(fname)
    time.sleep(1)
    camera.close()

#----------------------------------

    display_clear()
    draw.rectangle((0, 0, 0, oled.height-1), outline=255, fill=0)
    draw.rectangle((oled.width-1, 0, oled.width-1, oled.height-1), outline=255, fill=0)
    display_postext(1,"Foto!")
    display_postext(2,rnstr_fill)
    display_postext(3,dstr)
    display_postext(4,"----------")
    time.sleep(4)

#----------------------------------

    # going down
    display_clear()
    os.system("sudo shutdown now -h")

#------------------------------ physical end ------------------------------------
#--------------------------------------------------------------------------------
