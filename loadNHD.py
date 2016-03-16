# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import sys, os
import zipfile
from bs4 import BeautifulSoup
import requests

inputs = ['01','02','03N','03S','03W','04','05','06','07','08','09','10U','10L','11','12','13','14','15','16','17','18']

def pickURL(obj):
    for link in obj.find_all('a'):
        b = link.get('href')
        if 'NHDPlusCatchment' in b and 'http' in b:
            return b

def pickAll(obj):  
    d = []          
    for link in stew.find_all('a'):
        name = link.get('href')
        if name and 'http' in name and not 'horizon-systems' in name:
            d.append(name)
    return d
    
root = 'http://www.horizon-systems.com/NHDPlus/'
html = 'http://www.horizon-systems.com/NHDPlus/NHDPlusV2_data.php'
r  = requests.get(html)
data = r.text
soup = BeautifulSoup(data)
dl= []
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
            h = requests.get(root + link.get('href'))
            dat = h.text
            stew = BeautifulSoup(dat)
            g = pickAll(stew)
            for x in g:
                dl.append(x)
###############################################################################
# this block does the downloadin of the zips saved in the dl object above
for x in range(len(dl)):
    if not os.path.exists("/media/rick/Seagate Backup Plus Drive/NHDv21/%s"%dl[x].split('/')[-1]):
        r = requests.get(dl[x])
        with open("/media/rick/Seagate Backup Plus Drive/NHDv21/%s"%dl[x].split('/')[-1], "wb") as code:
            code.write(r.content)
###############################################################################
# this block writes a file to .spyder2 to run at the command line for unzipping
# ./
with open("/media/rick/Seagate Backup Plus Drive/NHDv21/unzip.sh", "w") as text_file:
    text_file.write("#! /bin/bash\n")
    text_file.write("\n")
    for x in dl:
        if not 'pdf' in x and not 'referer' in x:
            text_file.write("7z x %s\n" % x.split('/')[-1])