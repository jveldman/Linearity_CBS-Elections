# -*- coding: utf-8 -*-
"""
Created on Tue Jan 25 18:57:33 2022

@author: jjhve
"""

import json
def get_alloptions(): 
    from itertools import chain
    # Find file
    FileObject = open('C:/users/jjhve/Documents/TilburgUniversity/PolProj/itertable.json')
    readfile = FileObject.read()
    itertable = json.loads(readfile)
    temp = []
    for item in itertable: 
        if type(item) == dict: 
            step = list(chain(*list(item.items())))
            temp.append(step[1])
        else: 
            temp.append(item)
    temp = list(chain(*temp))
    return(temp)