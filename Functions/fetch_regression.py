# -*- coding: utf-8 -*-
"""
Created on Wed Jan 12 11:06:12 2022

@author: jjhve
"""

import pandas as pd
import sqlite3 

def stats_allyears():
    return()

def elec_clean(string): 
    replacables = ['GR', 'PS', 'TK', 'EP', '_gem', ' ']
    for repl in replacables: 
        string = string.replace(repl, '')
    return(string)

def request_elecstat(statistic, party, division):
    con = sqlite3.connect('D:/data/PolProj.db')
    table_frame = pd.read_sql("SELECT name FROM sqlite_master WHERE type='table';", con)
    elections = table_frame[table_frame.name.str.contains('_gem')]
    output = pd.DataFrame()
    for i, row in enumerate(elections.iterrows()):
        elec_tablename = row[1][0]
        year = elec_clean(elec_tablename)
        cur = con.cursor()
        #cur.execute('.headers on')
        query = str(
            'SELECT cbs_data.Perioden, cbs_data.TotaleBevolking_1,'+
            statistic + 
            ', cbs_data.municode,'
            ) 
        if division != False: 
            query += str(
                'cbs_data.'+
                division + ', t1.'+
                party + 
                ', t1.GeldigeStemmen'+
                ' FROM cbs_data INNER JOIN ' + 
                elec_tablename +
                ' AS t1 ON t1.municode = cbs_data.municode WHERE Perioden = '+
                year + 
                ' GROUP BY cbs_data.municode;'
                )
        else: 
            query += str('t1.'+
            party + 
            ', t1.GeldigeStemmen'+
            ' FROM cbs_data INNER JOIN ' + 
            elec_tablename +
            ' AS t1 ON t1.municode = cbs_data.municode WHERE Perioden = '+
            year + 
            ' GROUP BY cbs_data.municode;'
            )
        try: 
            data = cur.execute(query)
            data = pd.read_sql(query, con = con)
            #data = pd.read_sql(query, con)
            output = output.append(data)
        except sqlite3.DatabaseError as err: 
            print(str(party + ' did not participate in the '+elec_tablename + ' elections.'))
            pass
    return(output)

import pandas as pd
from statsmodels.formula.api import ols
from matplotlib import pyplot as plt
import numpy as np
import math

def fetch_regression(statistic, party, division = False):
    data= request_elecstat(statistic, party, division)
    data = data.apply(pd.to_numeric) 
    if division != False:
        data['perc_stat'] = data[statistic]/data[division]
        data['perc_party'] = data[party]/data['GeldigeStemmen']
        plt.plot(data['perc_stat'], data['perc_party'], 'o')
        #m,b = np.polyfit(data['perc_stat'], data['perc_party'], 1)        
        #plt.plot(data['perc_stat'], m*data['perc_stat'] + b)
        #plt.scatter(data['perc_stat'], data['perc_party'])
        plt.title(str('Votes for '+ party + ' compared to '+ statistic + "."))
        plt.xlabel(statistic)
        plt.ylabel(str('Votes for '+party))
        plt.savefig('D:/temp.png')
        model = ols('perc_party ~ perc_stat', data = data)
        results = model.fit()
        print(results.summary())
    else: 
        data['perc_party'] = data[party]/data['GeldigeStemmen']
        plt.plot(data[statistic], data['perc_party'], 'o')
        #m,b = np.polyfit(data[statistic], data[party], 1)        
        #plt.plot(data[statistic], m*data[statistic] + b)
        #plt.scatter(data['perc_stat'], data['perc_party'])
        plt.title(str('Votes for '+ party + ' compared to '+ statistic + "."))
        plt.xlabel(statistic)
        plt.ylabel(str('Votes for '+party))
        plt.savefig('D:/temp.png')
        model = ols(str(party + ' ~ ' + statistic), data = data)
        results = model.fit()
        print(results.summary())
    return(data)

data = fetch_regression('Koopwoningen_94', 'VVD')
data.to_csv('temp.csv')







