# -*- coding: utf-8 -*-
"""
Created on Tue Jan 25 18:56:24 2022

@author: jjhve
"""

def val_calc(model, lilfor, linear_val, homosked_val, alpha): 
    val = 0
    # Check for r_squared
    if model.rsquared > 0.05: 
        val += 1
    # Check for significance variable
    if model.pvalues[1] < alpha: 
        val += 1
    # Check for Lilliefors
    if lilfor[1] > alpha:
        val += 1
    # Check for linearity
    if linear_val[1] > alpha: 
        val += 1
    # Check for homoskedasticity
    if homosked_val[1] > alpha: 
        val += 1
    return(val)