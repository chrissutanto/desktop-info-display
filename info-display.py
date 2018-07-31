#!usr/bin/python
import time
import Adafruit_CharLCD as LCD
import json
import requests

# translink API info
api_key = "fQkcNy0xwMb4e3uWUwlD"
api_url_base = "http://api.translink.ca/rttapi/v1"

# desired bus stop
stop_no = 51204

# GPIO pin configuration on Raspberry Pi Zero W
lcd_rs = 26
lcd_en = 19
lcd_d4 = 13
lcd_d5 = 6
lcd_d6 = 5
lcd_d7 = 11
lcd_backlight = 4 # backlight pin not used, replaced with toggle switch

# configure screen
lcd_columns = 16
lcd_rows = 2

# initialize screen
lcd = LCD.Adafruit_CharLCD(lcd_rs, lcd_en, lcd_d4, lcd_d5, lcd_d6, lcd_d7, lcd_columns, lcd_rows, lcd_backlight)



message = "first\nmessage"

lcd.message(message)

time.sleep(5)

lcd.clear()

message = "second\nmessage"

time.sleep(5)

lcd.clear()

lcd.message("third\nmessage")
