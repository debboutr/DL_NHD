j# -*- coding: utf-8 -*-
"""
This script is being developed...Currently it gathers all of the URLs to every
.7z file in horizon-systems NHDPlusV2_data page based on the zones that are 
included in the inputs list. 

Need to develop a GUI to allow the selection of zones, as well as, select the 
desired .7z files within each zone, reducing the amount of data to be downloaded

Further development could also include flexibility in how the files are unziped,
currently a shell script is created that can then be run once all .7z files are
downloaded.
"""
import sys, os
import zipfile
from bs4 import BeautifulSoup
import requests

inputs = ['01','02','03N','03S','03W','04','05','06','07','08','09','10U','10L',
          '11','12','13','14','15','16','17','18']

def pickURL(obj):
    for link in obj.find_all('a'):
        b = link.get('href')
        if 'NHDPlusCatchment' in b and 'http' in b:
            return b

def pickAll(obj):  
    d = []          
    for link in obj.find_all('a'):
        name = link.get('href')
        if name and 'http' in name and '.7z' in name:
            d.append(name)
    return d
    
root = 'http://www.horizon-systems.com/NHDPlus/'
html = 'http://www.horizon-systems.com/NHDPlus/NHDPlusV2_data.php'
html = 'https://nhdplus.com/NHDPlus/NHDPlusV2_data.php'
r  = requests.get(html)
data = r.text
soup = BeautifulSoup(data)
dl= []
store = 'L:/Public/rdebbout/NHDv21_zips'
###############################################################################
# this block gets just catchment zips for each region in inputs
for link in soup.find_all('a'):
    for s in inputs:
        if s in link.get('href'):
            h = requests.get(root + link.get('href'))
            dat = h.text
            stew = BeautifulSoup(dat)
            dl.append(pickURL(stew))
###############################################################################
# this block gets all zips for each region in inputs
for link in soup.find_all('a'):
    for s in inputs:
        if s in link.get('href'):
            #print link.get('href')
            h = requests.get(root + link.get('href'))
            dat = h.text
            stew = BeautifulSoup(dat)
            g = pickAll(stew)
            for x in g:
                dl.append(x)
###############################################################################
# this block does the downloading of the zips saved in the dl object above
for x in range(len(dl)):
    if not os.path.exists("%s/%s" % (store, dl[x].split('/')[-1])):
        r = requests.get(dl[x])
        with open("%s/%s" % (store, dl[x].split('/')[-1]), "wb") as code:
            code.write(r.content)
###############################################################################
# this block writes a file to .spyder2 to run at the command line for unzipping
# ./
with open("%s/unzip.sh" % store, "w") as text_file:
    text_file.write("#! /bin/bash\n")
    text_file.write("\n")
    for x in dl:
        if not 'pdf' in x and not 'referer' in x:
            text_file.write("7z x %s\n" % x.split('/')[-1])
