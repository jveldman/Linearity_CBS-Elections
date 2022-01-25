# -*- coding: utf-8 -*-
"""
Created on Tue Jan 25 18:58:02 2022

@author: jjhve
"""
import os 
import get_alloptions
import pandas as pd 
import tqdm 
import assumption_scores

def regress_all(alpha = 0.05):
    try: 
        os.remove('statvals.csv')
    except FileNotFoundError: 
        pass
    import itertools
    q = get_alloptions()
    # Get a list of all the parties using the colnames file
    parties = list(pd.read_csv('Data/colnames.csv').iloc[10:,1])
    # remove duplicates
    parties = list(dict.fromkeys(parties))
    # Get all combos
    combos = list(itertools.product(q, parties))
    values = pd.DataFrame(columns = ['Party', 'Statistic','Type', 'Coeff', 'pval_coeff', 'r2', 'Lilliefors', 'Linearity', 'Heteroscedasticity', 'Model_score'])
    for item in tqdm(combos):
        try:
            get_values = assumption_scores(item[0], item[1], alpha)
        except ValueError: 
            get_values = pd.Series([item[1], item[0],0,0,0,0,0,0,0,0],
                               index = ['Party', 'Statistic','Type', 'Coeff', 'pval_coeff', 'r2', 'Lilliefors', 'Linearity', 'Heteroscedasticity', 'Model_score'])
        values = values.append(get_values, ignore_index = True)
        values.iloc[:,3:8] = values.iloc[:,3:8].round(4)
        values.to_csv('statvals.csv', index = False)
    return(values)
regress_all()