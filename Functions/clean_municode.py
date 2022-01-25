# -*- coding: utf-8 -*-
"""
Created on Tue Jan 25 18:51:16 2022

@author: jjhve
"""
import pandas as pd

# Function for standardising municipality code variable 'municode'
def clean_municode(table):
    remove_string = lambda x: table[~table.RegioS.str.contains(x)]
    # Def strings to remove 
    removables = ['(PV)','(CR)','(LD)','Nederland']
    for item in removables: 
        table = remove_string(item)
    table.dropna(subset = ['municode'], inplace = False)
    clean_string = lambda x: table.municode.str.replace(x, '')
    table.municode = clean_string('GM')
    table.municode = clean_string(' ')
    table.municode = pd.to_numeric(table.municode)
    return(table)

