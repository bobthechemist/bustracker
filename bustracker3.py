import requests
from xml.etree import ElementTree
from Adafruit_CharLCDPlate import Adafruit_CharLCDPlate
import time
import csv

# *** GLOBAL VARIABLES ***
BASE = 'http://www.ctabustracker.com/bustime/eta/getStopPredictionsETA.jsp?route=all&stop='
stops = ['5037', '1646']
descriptions = [
  'Downtown',
  'University'
  ]
cstop = 0 # Current stop

# *** FUNCTIONS ***

# Create a timer to avoid a modal delay
millis = lambda: int(round(time.time() * 1000))

# Return XML tree with stop information
def loadStop(stop):
  return ElementTree.fromstring(requests.get(BASE+stop).content)

# Convert XML tree into list of lists
def getData(tree):
  temp1 = []
  for entry in tree.findall('pre'):
    temp2 = []
    for i in ['pt', 'pu', 'fd','v','rn']:
      temp2.append(entry.find(i).text)
    temp1.append(temp2)
  return temp1

# Format data to fit the 16x2 display
def formatData(data):
  return"#{}: {}{}\n#{}: {}{}".format(data[0][4],data[0][0],data[0][1],data[1][4],data[1][0],data[1][1])

# Reading pause - so that messages can be seen
def readingPause():
  time.sleep(2)


# Start LCD panel
lcd = Adafruit_CharLCDPlate(busnum = 1)
lcd.clear()
lcd.message('LCD activated')
readingPause()

# Initialization stuff
ptime = millis()
looptime = 60000 #
running = True
lcd.clear()
lcd.message("Stop{}\n{}".format(stops[cstop],descriptions[cstop]))
readingPause()

data = getData(loadStop(stops[cstop]))
lcd.clear()
lcd.message(formatData(data))

while running:
  if millis() - ptime > looptime:
    lcd.clear()
    lcd.message(formatData(getData(loadStop(stops[cstop]))))
    ptime = millis()
  if lcd.buttonPressed(lcd.RIGHT):
    cstop+=1
    cstop = cstop % 2
    lcd.clear();
    lcd.message("Stop {}\n{}".format(stops[cstop],descriptions[cstop]))
    readingPause()
    ptime = 0
  if lcd.buttonPressed(lcd.LEFT):
    cstop -=1
    cstop = cstop % 2
    lcd.clear()
    lcd.message("Stop {}\n{}".format(stops[cstop],descriptions[cstop]))
    readingPause()
    ptime = 0
  if lcd.buttonPressed(lcd.DOWN):
    lcd.clear()
    lcd.message("Goodbye!")
    readingPause()
    running = False

lcd.clear()
