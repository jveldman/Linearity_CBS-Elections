# Function to clean up the municode column

def clean_municode(table):
    table.dropna(subset = ['municode'], inplace = False)
    clean_string = lambda x: table.municode.str.replace(x, '')
    table.municode = clean_string('GM')
    table.municode = clean_string(' ')
    table.municode = pd.to_numeric(table.municode)
    return(table) 