import json
import pandas as pd
import sqlite3 as sl

def __getDataFromMedium():
    ###
    #  This web site MEDIUM contains a series of free public datasets
    #  https://www.freecodecamp.org/news/https-medium-freecodecamp-org-best-free-open-data-sources-anyone-can-use-a65b514b0f2d/
    #
    #  the dataset contains these columns separated by tabs
    #  Quartier	date	Title	Recommends	Read ratio
    ###

    # csv data is here
    URL = "https://raw.githubusercontent.com/freeCodeCamp/open-data/master/medium-fCC-data/data/fccmediumTitles%20-%20Cleaned_Data.tsv"
    # we want column Title only
    COLUMNS = ['Title']
    DISPLAY_WIDTH = 1024
    COLUMN_WIDTH = -1

    # use panda to read csv data from website
    pd.set_option('display.max_rows', None, 'display.max_columns', None, 'display.width', DISPLAY_WIDTH,
                  'display.max_colwidth', COLUMN_WIDTH)
    # creates a panda dataframe
    df = pd.read_csv(URL, sep='\t', usecols=COLUMNS, low_memory=True)

    # isolate the title column from the 0 based result set, creates a list
    rows = []
    for row in df.itertuples():
        rows.append((row[0]+1, row[1]))

    return rows

def createAndLoadDatabase(dbname,dbtable,dbcolumn):
    # create DB if not exists, open a connection to it
    try:
        con = sl.connect(dbname)
        with con:
            # drop table if exists...
            con.execute("DROP TABLE IF EXISTS "+dbtable+";")
    except Exception as err:
       print(str(err))

    try:
        with con:
            # to create a new one
            con.execute("CREATE TABLE IF NOT EXISTS "+dbtable+" (id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,"+dbcolumn+" TEXT );")
    except Exception as err:
        print(str(err))

    try:
        with con:
            sql = "INSERT INTO "+dbtable+" (id, "+dbcolumn+") values(?,?)"
            data = __getDataFromMedium()
            con.executemany(sql, data)
    except Exception as err:
        print(str(err))

    try:
        con = sl.connect(dbname)
        with con:
            data = con.execute("SELECT "+dbcolumn+" FROM "+dbtable)
            print("Printing data...\n")
            for row in data:
                print(row)
    except Exception as err:
        print(str(err))

    return

if __name__ == '__main__':
    with open("../config.json") as json_data:
        config = json.load(json_data)

    dbname = config['search-app']['dbname']
    dbtable = config['search-app']['dbtable']
    dbcolumn = config['search-app']['dbcolumn']

    createAndLoadDatabase(dbname,dbtable,dbcolumn)
