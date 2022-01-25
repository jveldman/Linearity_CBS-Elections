# -*- coding: utf-8 -*-
"""
Created on Tue Jan 25 18:59:00 2022

@author: jjhve
"""
import numpy as np 
import matplotlib.pyplot as plt
import seaborn as sns


def requirement_plot(data, value,alpha = 0.05,):
    # Define when a value is sufficient and when not
    if value == 'pval_coeff':
        data['Significance'] = np.where(data[value] < 0.05, 'Sufficient', 'Insufficient')
    elif value in ['r2', 'Lilliefors', 'Linearity',	'Heteroscedasticity']:
        data['Significance'] = np.where(data[value] > 0.05, 'Sufficient', 'Insufficient')
    if value == 'Coeff': 
        sns.boxplot(x = data[value], showfliers = False).set(title = str('Division of '+value))
        plt.show()
        plt.close()
        return
    # Create plot environment
    fig, ax = plt.subplots(1,2)
    sns.countplot(x = data['Significance'], data = data, ax = ax[0], order = ['Sufficient', 'Insufficient']).set(title = str('Q significant / sufficient ' + value))
    sns.kdeplot(x = data[value], ax = ax[1]).set(title = str('Division of '+value))
    fig.tight_layout(pad = 2.0)
    plt.show()
    plt.close()	