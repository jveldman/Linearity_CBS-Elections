# -*- coding: utf-8 -*-
"""
Created on Tue Jan 25 18:55:55 2022

@author: jjhve
"""

import get_regresdat
import numpy as np

def set_checkerdata(statistic, party):
    # Get data
    data = get_regresdat(statistic, party)
    # Reshape data to make it suitable for regression
    data[statistic] = data[statistic].values.reshape(-1,1)
    data['perc_party'] = data['perc_party'].values.reshape(-1,1)
    # Column with natiural logarithm of dependent variable
    data['perc_partLOG'] = np.log(data['perc_party'])
    # Column with one divided by the dependent variable
    data['perc_partDIV'] =  1/data['perc_party']
    # Column with dependent variable to the power two
    data['perc_partPW2'] = np.power(data['perc_party'],2)
    # Column with the square root of dependent variable
    data['perc_partSRT'] = np.sqrt(data['perc_party'])
    # Add constant for regression analysis
    data['const'] = 1
    return(data)