import glob
import pandas as pd
from alias import alias
from tabulate import tabulate
import re
import numpy as np
path = "./csv/*.csv"
username = "ducky#6230"

full_df = pd.DataFrame() 




for fname in sorted(glob.glob(path)):
	print(fname)
	raw_df = pd.read_csv(fname)
	# this part combines successive messages through author id
	#for i in raw_df.index:
	raw_df = raw_df.fillna(' ') 
	current_df = pd.DataFrame()
	change_value = (raw_df["AuthorID"].shift() != raw_df["AuthorID"]).to_list() # False indicates identical as one before
	#print(change_value)
	#print(raw_df)
	current_message = ""
	for current_index in range (0, len(change_value)-1):
		if change_value[current_index+1] == False:
			current_message = current_message + str(raw_df["Content"][current_index]) + "\n"
			#print(raw_df.at[current_index, "Content"])
			#print(str(raw_df["Content"][current_index]))
		else:
			current_message = current_message  + str(raw_df["Content"][current_index])
			current_row = pd.DataFrame([raw_df["Author"][current_index], re.sub(r'\s+$', '', current_message, flags=re.M)]).T
			#print(current_row)
			current_df = pd.concat([current_df, current_row], axis= 0, ignore_index=True) # concat also concats row numbers
			current_message = ""
	current_df.columns =["Author", "Content"]
	#print(current_df["Author"][0].to_string(index=False))
	print(current_df.iloc[0])

	#import sys
	#sys.exit()


	contexted = []

	# context window of size 7
	n = 7
	for i in current_df.index:
		if i < n:
			continue
		row = []
	
		prev = i - 1 - n # we additionally substract 1, so row will contain current responce and 7 previous responces  

		# Comment out and uncomment as needed

		
		# append both author of response and adds fake @author in context
		'''
		if current_df["Author"][i] in alias:
			row.append(str(current_df["Content"][i]) + " -"+ str(alias[current_df["Author"][i]]))
		if current_df["Author"][i] in alias:
			row.append("@" + str(alias[current_df["Author"][i]] + " " + str(current_df["Content"][i-1])))
		for j in range(i-2, prev, -1):
			row.append(current_df["Content"][j])
		contexted.append(row)   
		'''    

		# Doesn't append anything
		'''
		for j in range(i, prev, -1):
			row.append(current_df["Content"][j])
		contexted.append(row)
		'''

		# Filters out for one single username and appends only author of response
		'''
		if current_df["Author"][i] == username:
			if current_df["Author"][i] in alias:
				row.append(str(current_df["Content"][i]) + " -"+ str(alias[current_df["Author"][i]]))
			for j in range(i-1, prev, -1):
				row.append(current_df["Content"][j])
			contexted.append(row)
			'''

		# Filters out for one single username only
		if current_df["Author"][i] == username:
			for j in range(i, prev, -1):
				row.append(current_df["Content"][j])
			contexted.append(row)

	columns = ['response', 'context'] 
	columns = columns + ['context/' + str(i) for i in range(n - 1)]
	formated_current_df = pd.DataFrame.from_records(contexted, columns=columns)

	full_df = pd.concat([full_df, formated_current_df], axis= 0)
	#pd.set_option('display.max_rows', 1)  # or 1000
	#pd.set_option('display.max_columns', None)  # or 1000
	print(formated_current_df)


print(full_df.shape)
print(tabulate(full_df.sample(1).T, headers='keys', tablefmt='pretty'))
full_df.to_csv('processed-data.csv', index=False) #save without row number

