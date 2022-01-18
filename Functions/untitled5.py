# -*- coding: utf-8 -*-
"""
Created on Fri Jan 14 16:13:05 2022

@author: jjhve
"""

import pandas as pd 
import sqlite3
con = sqlite3.connect('D:/data/PolProj.db')
string = 'SELECT * FROM general_data'
a = pd.read_sql(string, con = con )