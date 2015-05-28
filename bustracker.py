from splinter import Browser
from pyvirtualdisplay import Display
from Adafruit_CharLCDPlate import Adafruit_CharLCDPlate
import time
import csv

# *** GLOBAL VARIABLES ***
btURLBASE = 'http://www.ctabustracker.com/bustime/eta/eta.jsp?id='
stops = ['5037','1646']
descriptions = [
  "Downtown",
  "University"
  ];
cstop = 0 # Current stop
times = ['time1', 'time2', 'time3', 'time4', 'time5']
routes = ['route1', 'route2', 'route3', 'route4', 'route5']
vehicles = ['vehicle1', 'vehicle2', 'vehicle3', 'vehicle4', 'vehicle5']
destinations = ['destination1', 'destination2', 'destination3', 'destination4', 'destination5']


# *** FUNCTIONS ***

# Create a timer to avoid a modal delay
millis = lambda: int(round(time.time() * 1000))

# Load page with particular stop
btURLBASE = 'http://ctabustracker.com/bustime/eta/eta.jsp?id='
def btLoadPage(stop, urlbase=btURLBASE):
  urlstring = "".join([urlbase,stop])
  browser.visit(urlstring)
  return 

# Assumes that a page has already been loaded and takes advanage of the
#  dynamic updating of the bus tracker page, saving a bit of time.
def btScrape(list):
  'list is one of times, routes, vehicles, destinations and values are returned'
  temp = []
  for i in list:
    temp.append(browser.find_by_id(i).text)
  return map(str,temp)

def btScrapePage():
  'no args; loops through all lists to get all available information'
  temp = []
  for i in (times, routes, vehicles, destinations):
    temp.append(btScrape(i))
  currtime = bttime()
  temp.append([currtime for i in xrange(5)])
  return temp

# Gets the current time. Used to grab this from bustracker but I think
#   the system time is easier to deal with.
def bttime():
  #return str(browser.find_by_id('etalines').text.split('\n')[-1].split('  ')[0])
  return str(time.time())

# Formats the information returned from btScrapePage for display on LCD
def btFormatData(data):
  return "#{}: {}\n#{}: {}".format(data[1][0],data[0][0],data[1][1],data[0][1])

# Logs the data for further analysis
def btStoreData(data, fname='bt.csv'):
  f = open(fname,'ab')
  fa = csv.writer(f)
  fa.writerows(map(list,zip(*data)))
  f.close()


# Start LCD panel
lcd = Adafruit_CharLCDPlate(busnum = 1)
lcd.clear()
lcd.message("LCD activated")

# Set up virtual display for browser
display = Display(visible=0, size=(800,600))
display.start()
lcd.clear()

# Load iceweasel browser
lcd.message("Starting\n browser")
browser = Browser()
lcd.clear()
lcd.message("Browser started")

lcd.clear()
lcd.message("Starting\n bustracker")

# Initialization stuff
ptime = millis() # The previous time to allow for a non-modal delay
# 60000 and it looks like I miss some of the approaching messages
looptime = 50000 # Amount of time between updates
running = True
lcd.clear()
lcd.message("Stop {}\n{}".format(stops[cstop],descriptions[cstop]))
btLoadPage(stops[cstop])

while running:
  if millis() - ptime > looptime:
    data = btScrapePage()
    message = btFormatData(data)
    lcd.clear()
    lcd.message(message)
    btStoreData(data)
    ptime = millis()
  if lcd.buttonPressed(lcd.RIGHT):
    cstop+=1;
    cstop = cstop % 2
    lcd.clear();
    lcd.message("Stop {}\n{}".format(stops[cstop],descriptions[cstop]))
    btLoadPage(stops[cstop])
    ptime = 0
  if lcd.buttonPressed(lcd.LEFT):
    cstop-=1;
    cstop = cstop % 2
    lcd.clear();
    lcd.message("Stop {}\n{}".format(stops[cstop],descriptions[cstop]))
    btLoadPage(cstop)
    ptime = 0
  if lcd.buttonPressed(lcd.DOWN):
    lcd.clear()
    lcd.message("Goodbye!")
    running = False


browser.quit()
display.stop()
lcd.clear()
lcd.backlight(lcd.OFF)

