
import sqlite3
import json
import argparse


def get_sqldb_path():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--path',
        '-p',
        type=str,
        required=True,
        help="path to you sqlite databse (ex: '/home/username/db.sqlite3')"
    )
    args = parser.parse_args()
    path = args.path
    return path


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


def getAllRecordsInTable(table_name, pathToSqliteDb):
    conn, curs = openConnection(pathToSqliteDb)
    conn.row_factory = dict_factory
    curs.execute("SELECT * FROM '{}' ".format(table_name))
    # fetchall as result
    results = curs.fetchall()
    # close connection
    conn.close()
    return json.dumps(results)


def sqliteToJson(pathToSqliteDb):
    connection, cursor = openConnection(pathToSqliteDb)
    # select all the tables from the database
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    # for each of the tables , select all the records from the table
    for table_name in tables:
        # Get the records in table
        results = getAllRecordsInTable(table_name['name'], pathToSqliteDb)

        # generate and save JSON files with the table name for each of the database tables and save in results folder
        with open('./results/'+table_name['name']+'.json', 'w') as the_file:
            the_file.write(results)
    # close connection
    connection.close()


if __name__ == '__main__':
    db_path = get_sqldb_path()
    sqliteToJson(db_path)
