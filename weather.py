import requests
from xml.etree import ElementTree
from Adafruit_CharLCDPlate import Adafruit_CharLCDPlate
import time
                        


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
  
# Start LCD Panel
lcd = Adafruit_CharLCDPlate(busnum = 1)
lcd.clear()
lcd.message('LCD activated')
time.sleep(3)

printWeather(getWeatherMessages())
  

lcd.clear()
