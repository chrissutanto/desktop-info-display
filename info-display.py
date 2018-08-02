#!usr/bin/python
import time
import Adafruit_CharLCD as LCD
import json
import requests
import RPi.GPIO as GPIO

# configure GPIO
switch_pin = 21
# GPIO.setmode(GPIO.BOARD) Adafruit library sets mode to BCM
GPIO.setup(switch_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP) #set up switch to toggle data refresh and backlight

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

# function to request data, returns string of info to print
def getData():
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
	secondline = leave_time.split(" ")[0] + " in " + str(countdown) + "min"
	return firstline + "\n" + secondline

# function to update screen with data
def printData(to_print):
	lcd.clear()
	lcd.message(to_print)

# main loop
try:
	while True:
		printData(getData())
		if(GPIO.input(switch_pin) == False): # if toggle switch is in "on" pos, despite "False"
			for _ in range(120): # check if switch is turned off every 0.5 seconds for 1 minute UNTESTED
				if(GPIO.input(switch_pin) == False):
					time.sleep(0.5)
		else:
			lcd.clear()
			lcd.message("not refreshing")
			#TODO: add backlight pin and turn off backlight here
			GPIO.wait_for_edge(switch_pin, GPIO.FALLING)
			#TODO: toggle backlight on
except KeyboardInterrupt:
	GPIO.cleanup()
