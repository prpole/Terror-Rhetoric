from bs4 import BeautifulSoup
from types import *
import os

def checkfile(filename):
    content = open("TextOnly/"+filename,"r+")
    print content.read()
    
for fname in os.listdir('TextOnly'):
    if fname != ".DS_Store":
        file = open('TextOnly/'+fname, 'r')
        text = file.read()
        date = []
        year = fname[6:8]
        month = fname[0:2]
        day = fname[3:5]
        date.append(year)
        date.append(month)
        date.append(day)
        newfname = ''.join(date)
        newfile = open('TextOnlyDated/'+newfname+'.txt','w')
        newfile.write(text)
        newfile.close()
        file.close()
        
    
