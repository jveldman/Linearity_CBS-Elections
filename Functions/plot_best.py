# -*- coding: utf-8 -*-
"""
Created on Tue Jan 25 19:00:00 2022

@author: jjhve
"""

import set_checkerdata
import matplotlib.pyplot as plt
import seaborn as sns

def plot_best(statistic, party, type):
    if type == 'votes_sqrt':
        type_val = 'perc_partSRT'
    elif type == 'votes_log':
        type_val = 'perc_partLOG'
    data = set_checkerdata(statistic, party)
    sns.regplot(x = statistic, y = type_val, data = data, scatter_kws={'s':2}).set_title(str('% votes for '+ party  + ' vs. ' + statistic))
    plt.show()
    plt.close()

