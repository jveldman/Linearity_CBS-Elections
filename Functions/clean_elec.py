# -*- coding: utf-8 -*-
"""
Created on Tue Jan 25 18:51:49 2022

@author: jjhve
"""

import os 
import pandas as pd
from write_dbfile import write_dbfile

location = str(os.getcwd().replace('\\', '/') +'/Data/PolProj.db')

# define data map 
def clean_elec():
    # Define directory 
    directory = str(os.getcwd())
    # Import column names + replacements
    colnamers = pd.read_csv(str(directory + '\\Data\\colnames.csv'))
    # Create list to filter out small parties (local parties in municipality elections, etc)
    filter_list = list(colnamers.iloc[:,0])
    # Locate data directory 
    directory += str('\\Data\\Elections')
    for file in os.listdir(directory): 
        # Loop through folders
        directory_temp = str(directory + '\\' + str(file))
        for item in os.listdir(directory_temp):
            # Iterate over csv's in folder
            data = pd.read_csv(str(directory_temp + '\\' + item), sep = ';').rename(columns = {'RegioCode' : 'municode'})
            # Filter out small parties
            data = data[data.columns.intersection(filter_list)]
            # Convert new and old column names to dictionary
            filter_dict = dict(zip(colnamers.colname_old, colnamers.colname_new))
            # Rename columns
            data.rename(columns = filter_dict, inplace = True)
            # Define cleaning function
            remove_signs = lambda x:  data.columns.str.replace(x, '')
            # Define strings to remove
            removables = ['.', '(', ')', '!', '&', '-', ":", '/', '+']  
            # iterate over string list and remove them 
            for character in removables:
                    data.columns = remove_signs(character) 
            # Define string cleaning function
            clean_string = lambda x: data.municode.str.replace(x, '')
            # Filter out everything else except municipalities
            data = data[data['municode'].str.contains('G')]
            data.municode = clean_string('G')
            data.municode = clean_string(' ')
            # Convert municode to numeric
            data.municode = pd.to_numeric(data.municode)
            filename = item.replace('.csv', '')
            # Clean and store data in database
            write_dbfile(filename,data, 0, ['general_data', 'municode'],location)
    return()
clean_elec()
