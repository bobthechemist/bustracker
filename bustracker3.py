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
      if entry.find(i).text != '&nbsp':
        temp2.append(entry.find(i).text)
      else:
        temp2.append("")
    temp1.append(temp2)
  return temp1

# Format data to fit the 16x2 display
def formatData(data):
  # Poor way to deal with insufficient data
  temp = "No information"
  if len(data)>=2:
    temp = "#{}: {}{}\n#{}: {}{}".format(data[0][4],data[0][0],data[0][1],data[1][4],data[1][0],data[1][1])  
  if len(data)==1:
    temp = "#{}: {}{}".format(data[0][4],data[0][0],data[0][1]) 
  return temp

# Reading pause - so that messages can be seen
def readingPause():
  time.sleep(2)

# *** Weather functions ***
def getWeatherMessages():
  'Grabs weather information from NOAH and returns a some information about the forecast'
  weather_url = 'http://graphical.weather.gov/xml/SOAP_server/ndfdXMLclient.php?whichClient=NDFDgen&lat=38.99&lon=-77.01&product=time-series&begin=2004-01-01T00%3A00%3A00&end=2019-08-01T00%3A00%3A00&Unit=e&maxt=maxt&mint=mint&temp=temp&wx=wx&tmpabv14d=tmpabv14d&tmpblw14d=tmpblw14d&prcpabv14d=prcpabv14d&prcpblw14d=prcpblw14d&precipa_r=precipa_r&sky_r=sky_r&temp_r=temp_r&Submit=Submit'
  npage = requests.get(weather_url).content
  ntree = ElementTree.fromstring(npage)
  weatherMessages = ["Today's Weather"]
  # First, get the max/min temps for the day
  tmax = 'N/A'
  tmin = 'N/A'
  for i in ntree.find('data').find('parameters').findall('temperature'):
  	if i.attrib['type']=='maximum':
  		tmax = i[1].text
  	if i.attrib['type']=='minimum':
  		tmin = i[1].text
  weatherMessages.append("Hi:" + tmax + " Lo:" + tmin)
  # Find the first weather forecast - return the element
  for i in ntree.find('data').find('parameters').find('weather').iter('weather-conditions'):
  	itemp = i.getchildren()
  	if len(itemp)>0:
  		forecast = itemp
  		break
  # Now make the forecast results user friendly.
  for i in forecast:
  	adj = ''
  	if i.attrib['intensity'] != 'none':
  		adj = i.attrib['intensity'] + " "
  	weatherMessages.append(i.attrib['coverage']+' of '+adj+i.attrib['weather-type'])  
  # Return the list of weather messages
  return weatherMessages
  
def printWeather(fordisplay):
  for i in fordisplay:
    lcd.clear()
    if len(i)>16:
      if len(i)>32:
        lcd.message(i[0:15]+"\n"+i[16:31])
        time.sleep(3)
        lcd.clear()
        lcd.message(i[32:-1])
      else:
        lcd.message(i[0:15]+"\n"+i[16:-1])
    else:
      lcd.message(i)
    time.sleep(3)

# *** Start to work ***
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
lcd.message("Stop {}\n{}".format(stops[cstop],descriptions[cstop]))
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
  if lcd.buttonPressed(lcd.UP):
    printWeather(getWeatherMessages())
    lcd.clear();
    lcd.message("Stop {}\n{}".format(stops[cstop],descriptions[cstop]))
  if lcd.buttonPressed(lcd.DOWN):
    lcd.clear()
    lcd.message("Goodbye!")
    readingPause()
    running = False

lcd.clear()
