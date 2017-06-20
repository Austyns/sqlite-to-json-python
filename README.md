# Setup
To setup, colone this repo and run  the import_all.py file after supplying the right path to the sqlite file 

# sqlite-to-json-python
Convert sqlite databases to JSON files

import sqlite3
 
def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

# connect to the SQlite databases
connection = sqlite3.connect("path/to/sqlite/db")
connection.row_factory = dict_factory
 
cursor = connection.cursor()

# select all the tables from the database
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()
# for each of the tables , select all the records from the table and write to json file (table_name.json file)
for table_name in tables:
		# table_name = table_name[0]
		print table_name['name']
		    

		conn = sqlite3.connect("path/to/sqlite/db")
		conn.row_factory = dict_factory
		 
		cur1 = conn.cursor()
		 
		cur1.execute("SELECT * FROM "+table_name['name'])
		 
		# fetch all.
		 
		results = cur1.fetchall()
		 
		print results

		# generate and save JSON files with the table name for each of the database tables
		with open(table_name['name']+'.json', 'a') as the_file:
		    the_file.write(format(results).replace(" u'", "'").replace("'", "\""))

connection.close()


Enjoy..
