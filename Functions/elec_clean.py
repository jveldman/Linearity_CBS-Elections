# -*- coding: utf-8 -*-
"""
Created on Tue Jan 25 18:53:22 2022

@author: jjhve
"""

def elec_clean(string): 
    replacables = ['GR', 'PS', 'TK', 'EP', '_gem', ' ']
    for repl in replacables: 
        string = string.replace(repl, '')
    return(string)