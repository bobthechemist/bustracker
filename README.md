# bustracker
Scraping CTA bus arrive times with an RPi and displaying on an Adafruit LCD Plate

# Motivation
I hate leaving my apartment and turning the corner only to see that the bus is just arriving at the bus stop and I'm still a few minutes walk away from it.  I also seem to be unable to get into the habit  of checking the [CTA Bustracker](http://www.ctabustracker.com) website.  Clearly, what I need is to use one of my spare Raspbery Pi's as a marquee.

# Installation and use
I'll assume you have python installed on your RPi and have the [Adafruit LCD Plate](https://learn.adafruit.com/adafruit-16x2-character-lcd-plus-keypad-for-raspberry-pi) (or something similar) set up and ready to go.  You'll need a few additional modules, the [Python Virtual Display](https://pypi.python.org/pypi/PyVirtualDisplay) wrapper and [Splinter](https://splinter.readthedocs.org/en/latest/) for web scraping.  I'm using iceweasel for the browser `sudo apt-get install iceweasel` and this allows you to use the firefox driver in Splinter.

You'll probably want to run the program once to see what it's doing, although I seriously doubt you care when the #6 CTA bus arrives in Hyde Park. (If you do, drop me a line so we can get to work on a local Raspberry Jam.)  If you really want to use this for Chicago, it's easiest to first use the CTA Bustracker website (linked above) to find the four-digit bus stop ID that you want.

Since the LCD Plate has some pushbuttons, I've added a very simple interface.  The left/right buttons will switch between the bus stops and the down button will end the program gracefully.

The bus information (all buses, not just the 2 displayed on the LCD) is stored in a CSV file, which I will use at some point in the future.

Since I run my marquee headless, I ssh into the RPi and start the program with

```
nohup sudo python bustracker.py &
```

`nohup` allows the program to keep running even after I log out.
