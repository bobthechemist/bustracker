import requests
from xml.etree import ElementTree
import time

# XML information from http://w1.weather.gov/xml/current_obs/
url = 'http://w1.weather.gov/xml/current_obs/KMDW.xml'
page = requests.get(url).content
tree = ElementTree.fromstring(page)
curr_weather = tree.find('weather').text
curr_temp = tree.find('temp_f').text
# Get remaining data tags with something like
# for i in tree.iter():
#   print i.tag, ":", i.text

# Consider using below for forecast information
# http://graphical.weather.gov/xml/SOAP_server/ndfdXML.htm
# I think this URL gives me the relevant weather information
weather_url = 'http://graphical.weather.gov/xml/SOAP_server/ndfdXMLclient.php?whichClient=NDFDgen&lat=38.99&lon=-77.01&product=time-series&begin=2004-01-01T00%3A00%3A00&end=2019-08-01T00%3A00%3A00&Unit=e&maxt=maxt&mint=mint&temp=temp&wx=wx&tmpabv14d=tmpabv14d&tmpblw14d=tmpblw14d&prcpabv14d=prcpabv14d&prcpblw14d=prcpblw14d&precipa_r=precipa_r&sky_r=sky_r&temp_r=temp_r&Submit=Submit'
npage = requests.get(weather_url).content
ntree = ElementTree.fromstring(npage)
# this will get all the time layout elements
tlelements = ntree.find('data').findall('time-layout')
# Here are the time layout keys
timekeys = []
for i in tlelements:
	timekeys.append(i.find('layout-key').text)
# Extracts the high and low temperatures
tmax = 'N/A'
tmin = 'N/A'
for i in ntree.find('data').find('parameters').findall('temperature'):
	if i.attrib['type']=='maximum':
		tmax = i[1].text
	if i.attrib['type']=='minimum':
		tmin = i[1].text
temp_message = "Hi:" + tmax + " Lo:" + tmin
# Find the first weather forecast - return the element
for i in ntree.find('data').find('parameters').find('weather').iter('weather-conditions'):
	itemp = i.getchildren()
	if len(itemp)>0:
		forecast = itemp
		break
# Create the forecase out of the element
forecast_message = []
for i in forecast:
	adj = ''
	if i.attrib['intensity'] != 'none':
		adj = i.attrib['intensity'] + " "
	forecast_message.append(i.attrib['coverage']+' of '+adj+i.attrib['weather-type'])
  
     
      
def getWeatherMessages():
  'Grabs weather information from NOAH and returns a some information about the forecast'
  weather_url = 'http://graphical.weather.gov/xml/SOAP_server/ndfdXMLclient.php?whichClient=NDFDgen&lat=38.99&lon=-77.01&product=time-series&begin=2004-01-01T00%3A00%3A00&end=2019-08-01T00%3A00%3A00&Unit=e&maxt=maxt&mint=mint&temp=temp&wx=wx&tmpabv14d=tmpabv14d&tmpblw14d=tmpblw14d&prcpabv14d=prcpabv14d&prcpblw14d=prcpblw14d&precipa_r=precipa_r&sky_r=sky_r&temp_r=temp_r&Submit=Submit'
  npage = requests.get(weather_url).content
  ntree = ElementTree.fromstring(npage)
  weatherMessages = []
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
  
    
  

