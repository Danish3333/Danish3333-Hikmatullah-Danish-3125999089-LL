# Legacy Rainfall Monitor v1.0 (circa 2018)
# WARNING: This is legacy code with known issues for Assignment 2

import urllib2
import json
from datetime import datetime

API_KEY = '789c45f216f2e926657548a0fe7e4431'

def getweather(city):
    url = 'http://api.openweathermap.org/data/2.5/weather?q=' + city + '&appid=' + API_KEY
    response = urllib2.urlopen(url)
    data = json.loads(response.read())
    return data

def process(data):
    # Extract rainfall
    rain = 0
    if 'rain' in data:
        if '1h' in data['rain']:
            rain = data['rain']['1h']
        elif '3h' in data['rain']:
            rain = data['rain']['3h'] / 3
    
    temp = data['main']['temp']
    humidity = data['main']['humidity']
    
    # Alert logic
    alert = 'green'
    if rain > 10:
        alert = 'yellow'
    if rain > 20:
        alert = 'red'
    
    # Log to file
    f = open('alert.log', 'a')
    f.write(str(datetime.now()) + ' ' + city + ' ' + str(rain) + '\n')
    f.close()
    
    return rain, temp, humidity, alert

# Main
cities = ['Beijing', 'Shanghai', 'Guangzhou']
for c in cities:
    d = getweather(c)
    r = process(d)
    print c, r

# Known Issues:
# - Uses urllib2 (Python 2 only, removed in Python 3)
# - No error handling (crashes if API fails)
# - Magic numbers in alert thresholds (10 and 20)
# - Hardcoded cities list
# - Log file not closed if exception occurs
# - No type hints
# - No docstrings
# - Alert threshold reversed (should be rain < 10 = green, 10-20 = yellow, >= 20 = red)
# - Uses city variable outside scope in process()
# - String concatenation for URL (no URL encoding)
# - No timeout on network request
# - No unit tests
# - Returns tuple with inconsistent types
# - No input validation