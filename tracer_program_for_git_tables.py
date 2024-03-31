import pandas as pd
import os
import json
from pandas import ExcelWriter

def get_file_list(folder):
	#declaring empty strings to store information
	sql_paths = ""
	config_json_paths = ""
	#initating loop for directories sub directories and files
	for path, subdirs, files in os.walk(folder):
	    for name in files:
	    	if name.endswith(".sql"):
	    		#adding to string if it is an sql file
	    		sql_paths = sql_paths + "," + str(os.path.join(path, name))
	    	if name.endswith(".json"):
	    		#getting all json files
	    		json_filepath = os.path.join(path, name)
	    		# removing file names in the jobs folder since we wont need to update the same
	    		if "/jobs/" in json_filepath:
	    			config_json_paths = config_json_paths
	    		else:
	    			#getting all other json files
	    			config_json_paths = config_json_paths + ","+json_filepath

	#turning strings into list for ease of processing
	config_json_path_list = config_json_paths.split(",")[1:]
	sql_path_list = sql_paths.split(",")[1:]
	return config_json_path_list,sql_path_list

def get_sql_script(sql,df_rep):
	sql_new = sql
	print(sql_new)
	output_string = ""
	for i in range(0,len(df_rep)):
		old_table = (df_rep['source_table'].iloc[i]).lower()
		#print(old_table)
		a = sql.find(old_table)
		print(a)
		if a > 0:
			output_string = output_string + old_table + ","

	return output_string






# please provide as close of a directory as possible
directory = "C:/Users/Varna/GIT_REPOSITORY/SQL_CODES/"
current_directory = os.getcwd() 
backup_code_folder = current_directory + "/backup_folder/"

if os.path.exists(backup_code_folder):
	backup_code_folder = backup_code_folder
else:
	os.mkdir(backup_code_folder)


migration_table_input = current_directory + "/table_migration_list.xlsx"

table_list = pd.read_excel(migration_table_input)

print(table_list)

config_file_list, sql_file_list = get_file_list(directory)
#print(config_file_list)
#print(sql_file_list)

output_df = pd.DataFrame(columns=['file','table_name'])

for i in sql_file_list:
	# opening file for read
	file_name = i.replace("\\","/")
	print(file_name)
	sql_file = open(file_name,'r')
	sql_text = sql_file.read()
	# creating backup in case
	print(sql_text)
	updated_sql = get_sql_script(sql_text,table_list)
	output_list = [i,updated_sql]
	output_df.loc[len(output_df)] = output_list
	
output_df = output_df[output_df['table_name'] != ""]
print(output_df)
output_file = f"{current_directory}/git_changes_output.xlsx"
writer =ExcelWriter(output_file)
output_df.to_excel(writer,"list",index=False)
writer.close()