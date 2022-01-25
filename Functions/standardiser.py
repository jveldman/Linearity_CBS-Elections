# -*- coding: utf-8 -*-
"""
Created on Tue Jan 25 18:53:33 2022

@author: jjhve
"""

import json

def standardiser(x_var):
    FileObject = open('Data/itertable.json')
    readfile = FileObject.read()
    # Open json file with lists and dictionaries
    itertable = json.loads(readfile)
    # Create list for standardised values
    standardised = []
    todo = []
    for item in itertable: 
        # if item in list, append standardised kist
        if type(item) == list: 
            standardised.append(item)
        else: 
        # if not, then add to dictionary list 'todo'
            todo.append(item)
    # unpack standardised list
    standardised = [key for sublist in standardised for key in sublist]
    # If x_var is in the standardised list, set divider to False
    if x_var in standardised: 
        divider = False
        return(divider)
    # if not, set the divider as the key of the dictionary it's found in
    else: 
        for item in todo: 
            if any(any(x_var in s for s in subList) for subList in item.values()): 
                divider = list(item.keys())[0]
            else: 
                next
        try:
            return(divider)
        # If the x_var cannot be found, raiser error
        except UnboundLocalError as err: 
            print(str('Error: ' + x_var + ' not found in variables.'))
            raise(err)