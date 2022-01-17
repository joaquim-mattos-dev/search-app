# The Project
This application is a Flask / Python application, created to demonstrate how to construct an API to search for data while suggesting completion as the user invokes the API. One can use a browser or the linux command <b>curl</b> to show the data. It has 3 endpoints:

1. http://host:port/autocomplete?str=a_word

Where a_word is a letter, a partial word, or sentences. Example:

```angular2html
    curl -H "Content-Type:text/plain" -s  http://localhost:5000/?str=mac
```

2.  http://host:port/

This option simply list all data available. Example:


```angular2html
    curl -H "Content-Type:text/plain" -s  http://localhost:5000
```


3. http://host:port/web

This last option is supposed to be used in a browser only, so the user can experience autocomplete while typing in an input field.

# Dataset
This app uses its own data. The datasource is a separate component where is possible to quickly configure from where you want to collect your data. This implementation includes public data from the IMDB Movies website as well as a SQLlite database populated with public data from the website medium. You can find the links below:

[Movies database (used only 250 titles here)](https://rapidapi.com/blog/how-to-use-imdb-api/)


[Mwdium.com Articles Titles - csv](https://raw.githubusercontent.com/freeCodeCamp/open-data/master/medium-fCC-data/data/fccmediumTitles%20-%20Cleaned_Data.tsv)

A configuration file <b>config.json</b> holds information of the Active datasource as well as the information to create the database, if you opt for this option.

```angular2html
    "ds-available": ["imdb", "sql3"],
    "ds-active":"sql3",
    "dbname": "db/sql3.db",
    "dbtable": "mytable",
    "dbcolumn": "contents"

```

The example above is using "SQLlite" as datasource. In order to read the CSV file and build the SQLlite DB, you just need to execute the program "dbload", which will read the Medium article tiles, create a database "sql3.db" in the db directory. Parameters are read from config.json. In a Linux shell, go to the "util" directory and type:

```angular2html
    $ python3 dbload.py 
```

If the database does not exists, it will be created. If it does, the table is dropped and rebuilt.

# How to build
The easiest way is to build "search=app" as a Docker container, assuming you have Docker available in your environment. In the project root folder, there is a suitable Dockerfile you can use, with the command below:
```angular2html
    docker build -t search-app:1.0 . 
```
This will create a Python Slim based Docker image.

# How to run
Once the container is created, you can run it with the command below:
```angular2html
    docker run -d --rm --name search-app -p 5000:5000 search-app:1.0
```

Where:

    -d to force Docker daemon mode
    --rm to automatically remove the container when stopped
    --name to assign a user friendly name for the App
    -p allows to map host port : container port
    The last name is the Docker image to run.

# Using the app
Now that the app is up and running, you can start consuming data. 

Please see screenshots under "static/screenshots" directory on this repo for more information on how to get data from this App.

# Deploy to Cloud
There are basically two ways to deploy this app on any cloud: using <b>NON-MANAGED</b> and <b>MANAGED</b> cloud services. And remember, each cloud provider has its own rules and process to accomplish this.

## Non-Managed cloud services
For non-managed services, it means you have to set up your own virtual machines, just like you would on your bare metal machine. That means setting up the whole environment, including all tools and libraries, as explained above.  

## Managed cloud services
Managed services mean you are able to easily build the app using the cloud provider Docker services. Again, each provider has a slightly different process.

#### AWS

AWS uses ECS (EC2 Container Service) to natively deploy Docker containers. Once you have proper access to this service, you need to download the ECS CLI to interact with the environment, create your ECS context and build/deploy your containers. You can find more information [on Docker](https://docs.docker.com/cloud/ecs-integration/) and [on AWS](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/docker-basics.html).

Last update: <b>01/17/2022.</b>