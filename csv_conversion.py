import glob
import pandas as pd
from alias import alias
from tabulate import tabulate

path = "./csv/*.csv"
append_name = True

full_df = pd.DataFrame()

for fname in glob.glob(path):
    current_df = pd.read_csv(fname)
    #current_df = current_df.drop(df.columns[[0, 2, 4, 5]], axis=1) 
    #print(df)
    contexted = []

    # context window of size 7
    n = 7
    for i in current_df.index:
        if i < n:
            continue
        row = []
    
        prev = i - 1 - n # we additionally substract 1, so row will contain current responce and 7 previous responces  
        if append_name == False:    
            for j in range(i, prev, -1):
                row.append(current_df["Content"][j])
            contexted.append(row)
        else:
            if current_df["Author"][i] in alias:
                row.append(str(current_df["Content"][i]) + " -"+ str(alias[current_df["Author"][i]]))
            if current_df["Author"][i] in alias:
                row.append("@" + str(alias[current_df["Author"][i]] + " " + str(current_df["Content"][i-1])))
            for j in range(i-2, prev, -1):
                row.append(current_df["Content"][j])
            contexted.append(row)


    columns = ['response', 'context'] 
    columns = columns + ['context/' + str(i) for i in range(n - 1)]
    formated_current_df = pd.DataFrame.from_records(contexted, columns=columns)

    full_df = pd.concat([full_df, formated_current_df], axis= 0)
    #pd.set_option('display.max_rows', 1)  # or 1000
    #pd.set_option('display.max_columns', None)  # or 1000
    #print(new.sample(6))

#print("Number of NAN rows to be removed", full_df.isna().sum())
#print(full_df[full_df.isna().any(axis=1)]) # and rows with Nan
print("Shape before filtering", full_df.shape)
#full_df = full_df.dropna()
full_df.dropna(subset=columns, inplace = True, how='all')
full_df = full_df.fillna(' ') # replace Nans with spaces
#pd.set_option('display.max_rows', 5)  # or 1000
#pd.set_option('display.max_columns', None)  # or 1000
#print(full_df.sample(6)) 
print(full_df.shape)
print(tabulate(full_df.sample(1).T, headers='keys', tablefmt='pretty'))
full_df.to_csv('processed-data.csv')

