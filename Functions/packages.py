# -*- coding: utf-8 -*-
"""
Created on Tue Jan 25 18:46:34 2022

@author: jjhve
"""

# Import packages
import os 
import warnings
import pandas as pd
import sqlite3
import json
import statsmodels.api as sm 
import numpy as np
# Set database location
location = str(os.getcwd().replace('\\', '/') +'/Data/PolProj.db')