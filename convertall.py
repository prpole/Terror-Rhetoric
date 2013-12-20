#!/usr/bin/env python

from bs4 import BeautifulSoup
from types import *
import os

def checkfile(filename):
    content = open("TextOnly/"+filename,"r+")
    print content.read()

def pulltext(filename):    
    text = []
    soup = BeautifulSoup(open("www.presidentialrhetoric.com/speeches/"+filename,"r"))
    textversion = open("TextOnly/"+filename+".txt","w")
    for p in soup.find_all('p'):
        if p.attrs == {'align': 'left', 'class': ['style2']}:
            string = p.string
            if type(string) is not NoneType:
                try:
                    string.encode('ascii')
                    text.append(string)
                except UnicodeEncodeError:
                    pass
            else:
                pass
    for p in soup.find_all('span'):
        if p.attrs == {'class': ['style2']}:
            string = p.string
            if type(string) is not NoneType:
                try:
                    string.encode('ascii')
                    text.append(string)
                except UnicodeEncodeError:
                    pass
    if text == []:
        for p in soup.find_all('p'):
            string = p.string
            if type(string)is not NoneType:
                try:
                    string.encode('ascii')
                    text.append(string)
                except UnicodeEncodeError:
                    pass
    """for l in text:
        if type(l) is NoneType:
            del text[text.index(l)]
            return text"""
    textversion.write(''.join(text))
    textversion.close()

def wordlist(fname):
    file = open('TextOnly/'+str(fname),"r+")
    if fname != '.DS_Store':
        fcontent = open('TextOnly/'+str(fname),"r+")
        text = fcontent.read()
        fstr = text.split()
        for l in fstr:
            if str(l) == '(laughter.)' or str(l) == '(laughter)' or str(l) == '(Laughter.)' or str(l) == '(Laughter)' or str(l) == '(applause.)' or str(l) == '(applause)' or str(l) == '(Applause.)' or str(l) == '(Applause)':
                fstr.remove(l)
    return fstr

for fname in os.listdir('www.presidentialrhetoric.com/speeches'):
    if fname == ".DS_Store":
        pass
    else:
        try:
            pulltext(fname)
        except Exception:
            print 'error' + fname
