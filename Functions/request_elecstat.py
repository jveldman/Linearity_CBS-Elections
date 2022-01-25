# -*- coding: utf-8 -*-
"""
Created on Tue Jan 25 18:53:57 2022

@author: jjhve
"""
import pandas as pd
import sqlite3
import elec_clean
import os

location = str(os.getcwd().replace('\\', '/') +'/Data/PolProj.db')

def request_elecstat(statistic, party, divider, con = location):
    # Establish connection
    con = sqlite3.connect(con)
    # get list of all tables 
    table_frame = pd.read_sql("SELECT name FROM sqlite_master WHERE type='table';", con)
    # Filter out the election data (no CBS and general data)
    elections = table_frame[table_frame.name.str.contains('_gem')]
    # Create skeleton of dataframe
    output = pd.DataFrame()
    for i, row in enumerate(elections.iterrows()):
        # Select table name and clean year
        elec_tablename = row[1][0]
        year = elec_clean(elec_tablename)
        cur = con.cursor()
        # Open SQL query
        query = str(
        'SELECT cbs_data.Perioden,'+
        'cbs_data.' + statistic +
        ', cbs_data.municode'
            )
        # If there is a divider, include this in query
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
        # Try to execute the query
        try: 
            data = cur.execute(query)
            data = pd.read_sql(query,con)
            output = output.append(data)
            # If the query does not succeed, then the party was not in the columns and therefore print warning message. 
        except sqlite3.DatabaseError: 
            print(str('WARNING: ' + party + ' did not participate in the '+ elec_tablename + ' elections.'))
            pass
    return(output)