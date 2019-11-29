# -*- coding: utf-8 -*-
"""
Created on Fri Nov 29 15:36:57 2019

@author: Wayne Monteiro
"""

import requests

api_key = ""
url = "http://maps.googleapis.com/maps/api/staticmap?"
location  = "Johns Hopkins University"
center = location
zoom =15
#r = requests.get(url +"center="+center+"&zoom="+str(zoom)+"&size=1024x768&key="+api_key)
r = requests.get("https://maps.googleapis.com/maps/api/staticmap?key="+api_key+"&center="+location+"&zoom="+str(zoom)+"&format=png&maptype=roadmap&style=element:labels%7Cvisibility:off&style=feature:administrative.land_parcel%7Cvisibility:off&style=feature:administrative.neighborhood%7Cvisibility:off&size=1230x1230")
s = requests.get("https://maps.googleapis.com/maps/api/staticmap?key="+api_key+"&center="+location+"&zoom="+str(zoom)+"&format=png&maptype=roadmap&size=1230x1230")
print (url +"center="+center+"&zoom="+str(zoom)+"&size=1024x768&key="+api_key)
f = open("image_without_label.png","wb")
f.write(r.content)
f.close()
g = open("image_with_label.png","wb")
g.write(s.content)
g.close()