import pandas as pd
import sqlite3

def write_dbfile(table_name, dataframe, primary_key = 0,  forkey_ref = 0, connection = 'D:/data/PolProj.db', elections = False):
    # Turn editing warning off 
    pd.options.mode.chained_assignment = None 
    if elections == True:
        colnamers= pd.read_csv('C:/users/jjhve/Documents/TilburgUniversity/PolProj/colnames.csv', index_col = False)
        filter_list = list(colnamers.iloc[:,0])
    # Filter on major parties and statistics
        dataframe = dataframe[dataframe.columns.intersection(filter_list)]
        filter_dict = dict(zip(colnamers.colname_old, colnamers.colname_new))
        dataframe.rename(columns = filter_dict, inplace = True)
    remove_signs = lambda x:  dataframe.columns.str.replace(x, '')
    removables = ['.', '(', ')', '!', '&', '-', ":", '/', '+']
    for item in removables:
        dataframe.columns = remove_signs(item) 
    # Establish sqlite connection
    con = sqlite3.connect(connection)
    # Open cursor
    cur = con.cursor()
    # Obtain table list
    cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tableframe = pd.DataFrame(cur.fetchall())
    # Table already exists, delete table
    if tableframe.iloc[:,0].str.contains('general_data').any():
        cur.execute(str('DROP TABLE ' + table_name +';'))
        print('table dropped')
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
        print('No primary key match found')
        pass
    # If foreign key matches with colnames, add to descriptive frame
    if forkey_ref != 0:
        try:
            to_foreign = descdat.loc[descdat['colnames'] == forkey_ref[1]].index[0]
            descdat.special[to_foreign] = 'FOREIGN KEY'
        # if not, give message
        except IndexError: 
            print('No foreign key match found')
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
        cmd_start += str('FOREIGN KEY (' + forkey_ref[1] + ') REFERENCES ' +
                         forkey_ref[0] + ' (' + forkey_ref[1]+ '));')
    else: 
        cmd_start = str(cmd_start[:-1]+');')
    # execute string
    #cur.execute(cmd_start)    
    # Close cursor and return string for checking 
    #cur.close()
    # Write dataframe to newly created table 
    #dataframe.to_sql(table_name, con, if_exists = 'append', index = False)
    return(cmd_start)

import cbsodata as cbs 
import pandas as pd
import sqlite3

# Obtain data
muni_all = pd.DataFrame(cbs.get_data('70739ned'))

# Rename columns, set 'municode' as central variable. 
muni_all = muni_all.rename(columns = {'GebiedsOfGemeentecode_3':'municode', 
                                      'EinddatumSorteerveld_7':'enddate'})

# Function for standardising municipality code variable 'municode'
def clean_municode(table):
    remove_string = lambda x: table[~table.RegioS.str.contains(x)]
    # Def strings to remove 
    removables = ['(PV)','(CR)','(LD)','Nederland']
    for item in removables: 
        table = remove_string(item)
    table.dropna(subset = ['municode'], inplace = True)
    clean_string = lambda x: table.municode.str.replace(x, '')
    table.municode = clean_string('GM')
    table.municode = clean_string(' ')
    table.municode = pd.to_numeric(table.municode)
    return(table)

main_data = clean_municode(muni_all)

# Table specific cleaning
clean_string = lambda x: main_data.enddate.str.replace(x, '')
main_data.enddate = clean_string(' ')
main_data.enddate = pd.to_numeric(main_data.enddate)
main_data = main_data[(main_data.enddate >= 20000101) | (main_data.enddate.isnull())]
main_data = main_data.drop_duplicates(subset = ['municode'])

## Write data to database
write_dbfile('general_data',main_data,  'municode', 0,'D:/data/PolProj.db', False)
