#!usr/bin/python
import time
import Adafruit_CharLCD as LCD
import json
import requests
import RPi.GPIO as GPIO

# configure GPIO
switch_pin = 10
# GPIO.setmode(GPIO.BOARD) Adafruit library sets mode to BCM
GPIO.setup(10, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) #set up switch to toggle data refresh and backlight

# desired bus stop
stop_no = "51204"

# translink API info
api_key = "fQkcNy0xwMb4e3uWUwlD"
request_url_base = "http://api.translink.ca/rttiapi/v1/stops/" + stop_no  + "/estimates?apikey=" + api_key
headers = {"accept":"application/json"}

# GPIO pin configuration on Raspberry Pi Zero W
lcd_rs = 26
lcd_en = 19
lcd_d4 = 13
lcd_d5 = 6
lcd_d6 = 5
lcd_d7 = 11
lcd_backlight = 9 # backlight pin not used, replaced with toggle switch

# configure screen
lcd_columns = 16
lcd_rows = 2

# initialize screen
lcd = LCD.Adafruit_CharLCD(lcd_rs, lcd_en, lcd_d4, lcd_d5, lcd_d6, lcd_d7, lcd_columns, lcd_rows, lcd_backlight)

while True:
# get bus stop info
	r = requests.get(request_url_base, headers=headers)
	loaded_info = json.loads(r.text)

	route_no = loaded_info[0]["RouteNo"]
	schedules = loaded_info[0]["Schedules"]

	# takes first schedule in list
	upcoming_schedule = schedules[0]

	destination = upcoming_schedule["Destination"]

	leave_time = upcoming_schedule["ExpectedLeaveTime"]
	countdown = upcoming_schedule["ExpectedCountdown"]

	firstline = route_no + " to " + destination
	secondline = leave_time.split(" ")[0] + " in " + str(countdown) + " min"
	lcd.clear()
	lcd.message(firstline + "\n" + secondline)

	time.sleep(60)

#TODO: Add toggle switch to turn on backlight and turn on refreshing 
#TODO: Fix bugs with negative time 
#TODO: add physical buttons to refresh/show different info, add support for stops with multiple bus routes
#message = "first\nmessage"
#lcd.message(message)
#time.sleep(5)
#lcd.clear()
#message = "second\nmessage"
#time.sleep(5)
#lcd.clear()
#lcd.message("third\nmessage")
