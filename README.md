# amleth

A data pipeline for ingesting MQTT topic events and transforming them into records in a  
sqlite3 database.

## TODOS

1. Add metrics to the processing queue and the database
2. Write some basic tests for:
   1. Database.py
   2. process.py
   3. broker.py


## Starting the dev environment

```
$ git clone git@github.com:DanielThurau/amleth.git
$ cd amleth
$ source <VENV_ENV>
$ rm data/application.db
$ cd scripts
$ python3 init_db.py
$ cd ../amleth/amleth
$ python3 main.py
```

## Deploying

```
$ git clone git@github.com:DanielThurau/amleth.git
$ cd amleth 
$ ./scripts/deploy.sh
```
