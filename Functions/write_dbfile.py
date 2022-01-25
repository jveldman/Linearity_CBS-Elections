# -*- coding: utf-8 -*-
"""
Created on Tue Jan 25 18:46:09 2022

@author: jjhve
"""

import os
import pandas as pd
import sqlite3
# Set database location
location = str(os.getcwd().replace('\\', '/') +'/Data/PolProj.db')

def write_dbfile(table_name, dataframe, primary_key = 0,  forkey_ref = 0, connection = location):
    # Turn editing warning off 
    pd.options.mode.chained_assignment = None
    # Establish sqlite connection
    con = sqlite3.connect(connection)
    # Open cursor
    cur = con.cursor()
    # Obtain table list and delete table if it already exists
    try:
        cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tableframe = pd.DataFrame(cur.fetchall())
        if tableframe.iloc[:,0].str.contains(table_name).any():
            cur.execute(str('DROP TABLE ' + table_name +';'))
    except IndexError: 
        pass
    # Opening SQLite statement
    cmd_start = str('CREATE TABLE IF NOT EXISTS ' + table_name + ' ( ')
    # Open dataframe with descriptions of dataframe
    descdat = pd.DataFrame(
        {'colnames': dataframe.columns,
        'coltypes':dataframe.dtypes, 
        'special': float("NaN")}
        )
    # Set index back to numeric 
    descdat = descdat.reset_index(drop=True)
    # If primary key matches with colnames, add to descriptive frame
    try:
        to_primary = descdat.loc[descdat['colnames']== primary_key].index[0]
        descdat.special[to_primary] = 'PRIMARY KEY'
    # If not, give message
    except IndexError: 
        #print('No primary key match found')
        pass
    # If foreign key matches with colnames, add to descriptive frame
    if forkey_ref != 0:
        try:
            to_foreign = descdat.loc[descdat['colnames'] == forkey_ref[1]].index[0]
            descdat.special[to_foreign] = 'FOREIGN KEY'
        # if not, give message
        except IndexError: 
            #print('No foreign key match found')
            pass
    # Change description column types to strings
    descdat.coltypes = descdat.coltypes.astype(str)
    # Define replacing string function
    clean_string = lambda x,y: descdat.coltypes.str.replace(x, y)
    descdat.coltypes = clean_string('int64', 'INTEGER')
    descdat.coltypes = clean_string('float64', 'REAL')
    descdat.coltypes = clean_string('object', 'TEXT')
    for i,row in descdat.iterrows():
        # Loop over every row and create SQLite command string. 
        if row[2] == 'PRIMARY KEY': 
            cmd_start += str(str(row[0])+ ' '+ str(row[1]) + 'NOT NULL PRIMARY KEY' + ',')
        else: 
            cmd_start += str(str(row[0])+ ' '+ str(row[1]) + ',')
    # If foreign key mentioned, add foreign key indication to SQLite string
    if forkey_ref != 0: 
        cmd_start += str('FOREIGN KEY(' + forkey_ref[1] + ') REFERENCES ' +
                         forkey_ref[0] + '(' + forkey_ref[1]+ '));')
    else: 
        cmd_start = str(cmd_start[:-1]+');')
    # execute string
    cur.execute(cmd_start)    
    # Close cursor and return string for checking 
    cur.close()
    # Write dataframe to newly created table 
    dataframe.to_sql(table_name, con, if_exists = 'append', index = False)
    return()