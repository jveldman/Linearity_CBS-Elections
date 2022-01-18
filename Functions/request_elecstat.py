# -*- coding: utf-8 -*-
"""
Created on Fri Jan 14 14:06:26 2022

@author: jjhve
"""

import sqlite3
import pandas as pd
from standardiser import standardiser
import matplotlib.pyplot as plt
def elec_clean(string): 
    replacables = ['GR', 'PS', 'TK', 'EP', '_gem', ' ']
    for repl in replacables: 
        string = string.replace(repl, '')
    return(string)

def request_elecstat(statistic, party, divider, con = 'D:/data/PolProj.db'):
    con = sqlite3.connect(con)
    table_frame = pd.read_sql("SELECT name FROM sqlite_master WHERE type='table';", con)
    elections = table_frame[table_frame.name.str.contains('_gem')]
    output = pd.DataFrame()
    for i, row in enumerate(elections.iterrows()):
        elec_tablename = row[1][0]
        year = elec_clean(elec_tablename)
        cur = con.cursor()
        query = str(
        'SELECT cbs_data.Perioden,'+
        'cbs_data.' + statistic +
        ', cbs_data.municode'
            )
        if divider != False: 
            query += str(
                ', cbs_data.' + 
                divider)
        query += str(
            ', t1.'+party + 
            ', t1.GeldigeStemmen FROM cbs_data INNER JOIN '+
            elec_tablename + 
            ' AS t1 ON t1.municode = cbs_data.municode WHERE Perioden = '+
            year + ' GROUP BY cbs_data.municode;')
        try: 
            data = cur.execute(query)
            data = pd.read_sql(query, con = con)
            #data = pd.read_sql(query, con)
            output = output.append(data)
        except sqlite3.DatabaseError as err: 
            print(str(party + ' did not participate in the '+elec_tablename + ' elections.'))
            pass
    return(output)

def fetch_regression(statistic, party): 
    divider = standardiser(statistic)
    data = request_elecstat(statistic, party,divider)
    data = data.apply(pd.to_numeric)
    data['perc_party'] = data[party]/data['GeldigeStemmen']
    scatter = lambda x : plt.plot(x, data['perc_party'], linestyle = 'none', marker="o", markersize = 1)
    if divider == False: 
        scatter(data[statistic])
    if type(divider) == str: 
        print(str('divider' + 'does this work? '))
        data['stan_stat'] = data[statistic] / data[divider]
        scatter(data['stan_stat'])
    plt.title(str('Votes for '+ party + ' compared to '+ statistic + "."))
    plt.xlabel(statistic)
    plt.ylabel(str('% Votes for '+party))
    plt.show()
    return(data)

#temp = fetch_regression('Nieuwvormingen_64', 'Groenlinks')

def get_alloptions(): 
    import json
    from itertools import chain
    FileObject = open('C:/users/jjhve/Documents/TilburgUniversity/PolProj/itertable.json')
    readfile = FileObject.read()
    itertable = json.loads(readfile)
    temp = []
    for item in itertable: 
        if type(item) == dict: 
            step = list(chain(*list(item.items())))
            temp.append(step[1])
        else: 
            temp.append(item)
    temp = list(chain(*temp))
    return(temp)

def regress_all(party):
    q = get_alloptions()
    for item in q: 
        fetch_regression(item, party)
        
regress_all('SGP')    
