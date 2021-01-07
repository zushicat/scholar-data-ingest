# scholar-data-ingest
Ingest data of academic papers into a postgreSQL database instance.    

Right now, this is limited to data from [Semantic Scholar](https://www.semanticscholar.org/).    
See also:
- http://s2-public-api-prod.us-west-2.elasticbeanstalk.com/corpus/
- https://api.semanticscholar.org/    


## Install

### Prerequisite
In case of docker problems, try: docker --> preferences --> allocate more memory

### Build and start container (API and PostgreSQL DB)
```
$ docker-compose up
```
  
Both the Rest API and the postgreSQL database should be running after the building process. (This may take a while.)    

Right now, following ports are used:
- API: localhost:8080
- DB: localhost:5432

(You can change the ports in docker-compose.yml)


## Usage

### Bulk ingest
Semantic Scholar offers a bulk download divided into around 6000 batches with 30000 JSON line entries each.
To ingest these files, it is assumed that you download and decrompress the files of interest into the directory /data/tmp.    
All files passed by Rest API method call will be ingested into the database instance named "scholar".

See chapter "Rest API requests" below on how to initiate the process.    

See:
- http://s2-public-api-prod.us-west-2.elasticbeanstalk.com/corpus/
- http://s2-public-api-prod.us-west-2.elasticbeanstalk.com/corpus/download/

Getting files with curl (i.e. for OSX user):
- get the manifest.txt file
```
$ curl -O https://s3-us-west-2.amazonaws.com/ai2-s2-research-public/open-corpus/2020-11-06/manifest.txt
```
- get individual files from manifest.txt listing (strongly recommended due to the amount of data)
```
$ curl -O https://s3-us-west-2.amazonaws.com/ai2-s2-research-public/open-corpus/2020-11-06/s2-corpus-000.gz
```

**Place the individual bulk files into /data/tmp for ingestion.** (./data is defined as enviromental variable DATA_LOCATION in Dockerfile.)


## Semantic Scholar JSON
Check out this [JSON example](readme_files/semantic_scholar_corpus_entry_example.json) of  incoming data from an downloaded Semantic Scholar corpus batch.

## Database schema
![Database schema](readme_files/database_schema.png)

When the container is build, an empty database instance will be created with [this schema SQL file](data/postgres/schema.sql).

## Rest API requests / responses
As of now, the responses are not terribly informative.

### ping
Request
```
POST http://localhost:8080
Content-Type: application/json

{
    "jsonrpc": "2.0",
    "id": 12345,
    "method": "ping",
    "params": {}
}
```

Response
```
{
  "result": {
    "status": "ok",
    "response": "pong"
  },
  "id": 12345,
  "jsonrpc": "2.0"
}
```

### ingest.bulk
As of now, in case of id conflict (on the respective table) the new entry will simply be ignored.    
If you use language detection, ingesting will take considerably longer, depending on the number of words. (See: used_words_for_lang_detection in _ingester._create_table_entries)    

Request
```
POST http://localhost:8080
Content-Type: application/json

{
    "jsonrpc": "2.0",
    "id": 12345,
    "method": "ingest.bulk",
    "params": {
        "files": [
            "s2-corpus-000",
            "s2-corpus-001"
        ],
        "use_lang_detection": true
    }
}
```
- files: Names of bulk files in /data/tmp
- use_lang_detection: use language detection, applied on each title

For detection of short texts, a modified version of [ldig](https://github.com/shuyo/ldig) is used (latin text model only).    

Response
```
{
  "result": {
    "status": "ok",
    "response": "ingested"
  },
  "id": 12345,
  "jsonrpc": "2.0"
}
```

### truncate
Truncate passed tables and reset index to 1.

Request
```
POST http://localhost:8080
Content-Type: application/json

{
    "jsonrpc": "2.0",
    "id": 12345,
    "method": "truncate",
    "params": {
        "table_names": [
            "text",
            "author",
            "paper"
        ]
    }
}
```

Response
```
{
  "result": {
    "status": "ok",
    "response": "truncated"
  },
  "id": 12345,
  "jsonrpc": "2.0"
}
```

### export.csv
Export table as csv files to /data/csv (using the table name as file name).    

Request
```
POST http://localhost:8080
Content-Type: application/json

{
    "jsonrpc": "2.0",
    "id": 12345,
    "method": "export.csv",
    "params": {
        "table_names": [
            "text",
            "author",
            "paper"
        ]
    }
}
```

Response
```
{
  "result": {
    "status": "ok",
    "response": "csv exported"
  },
  "id": 12345,
  "jsonrpc": "2.0"
}
```