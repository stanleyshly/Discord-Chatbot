import glob
import pandas as pd
path = "./csv/*.csv"
f = open("alias.py", "w+")
alias = {}
for fname in glob.glob(path):
    df = pd.read_csv(fname)
    for current_row_index in range(0, df.shape[0]):
        #f.write()
        author = df["Author"][current_row_index]
        if author not in alias:
            alias[author] = ""
            print(author)
    print(fname)

print(alias)
f.write( 'alias = {' + repr(list(alias.keys())[0]) + ' : ' + repr(list(alias.keys())[0]) + ", \n" ) 
for current_index in range(1,len(alias)-1):
    f.write('\t \t' + repr(list(alias.keys())[current_index]) + ' : ' + repr(list(alias.keys())[current_index]) + ", \n" ) 
f.write('\t \t' + repr(list(alias.keys())[len(alias)-1]) + ' : ' + repr(list(alias.keys())[len(alias)-1]) + "}" ) 
