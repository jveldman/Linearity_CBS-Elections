# -*- coding: utf-8 -*-
"""
Created on Tue Jan 25 18:55:25 2022

@author: jjhve
"""

import standardiser
import request_elecstat
import pandas as pd

def get_regresdat(statistic, party):
    # Define the divider for the statistic
    divider = standardiser(statistic)
    # Obtain the data
    data = request_elecstat(statistic, party, divider)
    # Convert to numeric
    data = data.apply(pd.to_numeric)
    # Divide amount of votes for a party by the total amount of valid votes
    data['perc_party'] = data[party]/data['GeldigeStemmen']
    # Return original data if divider is absent
    if divider == False: 
        return(data.dropna())
    # Create relative statistic by defined divider variable
    if type(divider) == str: 
        data[statistic] = data[statistic]/data[divider]
        return(data.dropna())