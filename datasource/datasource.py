import pandas as pd
import json
import imdb
import sqlite3 as sl

with open("config.json") as json_data:
    config = json.load(json_data)

'''
See https://imdbpy.readthedocs.io/en/latest/
'''

def imdbSearch():
    dataset = []
    try:
        ia = imdb.IMDb()
        dataset = [x['title'] for x in ia.get_top250_movies()]
    except Exception as err:
        print("imdbSearch: "+str(err))

    return(dataset)

def sql3Search(dbname, dbtable, dbcolumn):
    dataset = []
    try:
        conn = sl.connect(dbname)
        with conn:
            # expects a unique text column
            df = pd.read_sql_query("SELECT "+dbcolumn+" FROM "+dbtable, conn)
            for row in df.itertuples():
                dataset.append(row[1])
    except Exception as err:
        print("sql3Search: "+str(err))
    finally:
        conn.close()

    return(dataset)
