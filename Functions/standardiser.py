# -*- coding: utf-8 -*-
"""
Created on Fri Jan 14 12:17:09 2022

@author: jjhve
"""

# load itertable: 
import json
import pandas as pd

#from request_elecstat import request_elecstat

def standardiser(x_var):
    FileObject = open('C:/users/jjhve/Documents/TilburgUniversity/PolProj/itertable.json')
    readfile = FileObject.read()
    itertable = json.loads(readfile)
    standardised = []
    todo = []
    for item in itertable: 
        if type(item) == list: 
            standardised.append(item)
        else: 
            todo.append(item)
    standardised = [key for sublist in standardised for key in sublist]
    if x_var in standardised: 
        divider = False
        return(divider)
    else: 
        for item in todo: 
            if any(any(x_var in s for s in subList) for subList in item.values()): 
                divider = list(item.keys())[0]
            else: 
                next
        return(divider)

#q = standardiser('VoortgezetOnderwijs_103')





        