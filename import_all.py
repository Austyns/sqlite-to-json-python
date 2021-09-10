
import sqlite3
import json
 
def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

# connect to the SQlite databases
def openConnection(pathToSqliteDb):
	connection = sqlite3.connect(pathToSqliteDb)
	connection.row_factory = dict_factory 
	cursor = connection.cursor()
	return connection, cursor

def getAllRecordsInTable(table_name,pathToSqliteDb):
	conn, curs = openConnection(pathToSqliteDb)
	conn.row_factory = dict_factory
	curs.execute("SELECT * FROM {} ".format(table_name) )
	# fetch all or one we'll go for all.

	results = curs.fetchall()
	_json = [dict(zip([key[0] for key in curs.description], row)) for row in results]
	return json.dumps(_json)


def sqliteToJson(pathToSqliteDb):
	connection, cursor = openConnection(pathToSqliteDb)
	# select all the tables from the database
	cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
	tables = cursor.fetchall()
	# for each of the tables , select all the records from the table
	for table_name in tables:
			# Get the records in table
			results = getAllRecordsInTable(table_name['name'],pathToSqliteDb)

			# generate and save JSON files with the table name for each of the database tables and save in results folder
			with open('./results/'+table_name['name']+'.json', 'w') as the_file:
			    the_file.write(results)

	connection.close()



if __name__ == '__main__':
	# modify path to sqlite db
	pathToSqliteDb = 'path/to/db.sqlite3'
	sqliteToJson(pathToSqliteDb)

