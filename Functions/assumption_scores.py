# -*- coding: utf-8 -*-
"""
Created on Tue Jan 25 18:56:36 2022

@author: jjhve
"""

import warnings
import set_checkerdata
import pandas as pd
import statsmodels.api as sm 
import numpy as np
import val_calc

def assumption_scores(statistic, party, alpha = 0.05): 
    # Turn off warnings 
    warnings.filterwarnings('ignore')
    # Get transformed columns 
    data = set_checkerdata(statistic, party)
    # If dataframe appears to be empty, return "0" values. 
    if len(data) < 5: 
        result = pd.DataFrame([party, statistic, 'Empty', 0,0,0,0,0,0,0],
            columns = ['Party', 'Statistic','Type', 'Coeff', 'pval_coeff', 'r2', 'Lilliefors', 'Linearity', 'Heteroscedasticity', 'Model_score'])
        return(result)
    # Define dict with different types of transformed columns as keys and columns as item. 
    votes_types = {'votes': data['perc_party'], 'votes_div':data['perc_partDIV'], 'votes_log':data['perc_partLOG'],
                   'votes_square':data['perc_partPW2'],'votes_sqrt': data['perc_partSRT']}
    # Create empty dictionary for scores
    scores = {}
    # Create empty dataframe for the scores of the transformed columns
    result = pd.DataFrame(columns = ['Party', 'Statistic','Type', 'Coeff', 'pval_coeff', 'r2', 'Lilliefors', 'Linearity', 'Heteroscedasticity', 'Model_score'])
    for key, value in votes_types.items():
        # Run linear regression
        model = sm.OLS(value, data[['const',statistic]]).fit()
        # Save predicted values and residuals incl. squared versions. 
        data['pred'] = model.predict()
        data['pred2'] = np.power(data['pred'],2)
        data['resids'] = model.resid
        data['resids2'] = np.power(data['resids'],2)
        # Replace infinite by nan
        data = data.replace([np.inf, -np.inf], np.nan)
        if data.isna().all()[-4:].all():
            # If all the values are nan note 0 for scores
            scores[key] = 0
            result.loc[len(result)] = [party, statistic, key, 0,0,0,0,0,0,0]
            next
        else:
            # If not, obtain earlier stated statistics defining the performance on that assumption
            lilfor =  sm.stats.diagnostic.lilliefors(data['resids'], dist = 'norm', pvalmethod = 'approx')
            linearity = sm.OLS(value,data[['const', statistic, 'pred2']]).fit()
            linear_val = [linearity.params[1], linearity.pvalues[2]]
            hetero = sm.OLS(data['resids2'], data[['const',statistic]]).fit()
            hetero_val = [hetero.params[1], hetero.pvalues[1]]
            # Use val_calc function to define the score based on p-values 
            val = val_calc(model, lilfor, linear_val, hetero_val, alpha)
            # Give score to this variation of the dependent variable
            scores[key] = val
            # Put the values that gave the score in dataframe. 
            result.loc[len(result)] = [party, statistic, key, model.params[1], model.pvalues[1], model.rsquared,  lilfor[1], linear_val[1], hetero_val[1], val]
    # Find best score
    max_name = max(scores, key = scores.get)
    # Take out the best performing values and return them
    max_val = result[result['Type'] == max_name]
    return(max_val)
