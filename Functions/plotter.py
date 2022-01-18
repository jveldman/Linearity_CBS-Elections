# -*- coding: utf-8 -*-
"""
Created on Fri Jan 14 12:55:04 2022

@author: jjhve
"""

# create plot 
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
df = pd.read_csv('temp.csv')
df.dropna(inplace = True)

plt.plot(df['Koopwoningen_94'], df['perc_party'], linestyle = 'none', marker="o", markersize = 1)
m, b = np.polyfit(df['Koopwoningen_94'], df['perc_party'], 1)
plt.plot(df['Koopwoningen_94'], m*df['Koopwoningen_94'] + b, c='r')
plt.xlabel('Koopwoningen')
plt.ylabel('Votes party')
plt.show()