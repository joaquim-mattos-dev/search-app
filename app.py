import json
from flask import Flask, request, render_template
import datasource.datasource as ds

'''
    this is a Python / Flask application, which runs on any environment with python and flask installed
    It's quite flexible to be used with browser or not, from a defined datasource
    It also format output to command line curl or browser, accordingly 
'''

app = Flask(__name__)

# config.json contains a few important parameters to control host, port and datasource
# datasource can be IMDB website or a RDBMS such as SQLite
with open("config.json") as json_data:
    config = json.load(json_data)

webhost = config['search-app']['webhost']
webport = config['search-app']['webport']
dsactive = config['search-app']['ds-active']

# getData allows the application to be datasource independent
# and relies on a formatted dataset coming from the datasource
def getData(dsactive):
    dataset = []
    if dsactive == "imdb":
        dataset = ds.imdbSearch()
    elif dsactive == "sql3":
        dbname = config['search-app']['dbname']
        dbtable = config['search-app']['dbtable']
        dbcolumn = config['search-app']['dbcolumn']
        dataset = ds.sql3Search(dbname,dbtable,dbcolumn)

    return(dataset)

# this route allows for autocomplete with partial word
# responds to http://host:port/autocomplete?str=anyword
@app.route("/autocomplete", methods=["GET"])
def getAutocomplete():
    if request.method == "GET":
        # get word from parameter .../autocomplete/?str=word
        word = request.args.get('str')
        res = [str(e) for e in getData(dsactive) if word.lower() in str(e).lower()]
        joined_string = "\n".join(res)

        return(joined_string)

# responds to http://host:port
# get ALL raw data from (configured) datasource
#
@app.route("/", methods=["GET"])
def getrawdata():
    if request.method == "GET":
        res = [str(e) for e in getData(dsactive)]
        joined_string = "\n".join(res)

        return(joined_string)

# responds to http://host:port/web
# supposed to be called in a browser to show input lookup
@app.route("/web", methods=["GET"])
def home():
    if request.method == "GET":
        return render_template("index.html", movie_titles=getData(dsactive))

if __name__ == '__main__':
    app.run(host=webhost, port=webport, debug=False)
