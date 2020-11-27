# scholar-data-digest
Request and digest data of academic papers into a postgreSQL database instance.    

Right now, this is limited to data from [Semantic Scholar](https://www.semanticscholar.org/).    
See also:
- http://s2-public-api-prod.us-west-2.elasticbeanstalk.com/corpus/
- https://api.semanticscholar.org/    


## Install

### Prerequisite
- sudo pip3 install black
- sudo pip3 install poetry
- in case of docker problems, try: docker --> preferences --> allowcate more memory

### Build and start container (API and PostgreSQL DB)
```
$ docker-compose up --build
```
(When the container is build, you may drop the --build parameter when starting again after stopping the container.)    

Both the Rest API and the postgreSQL database should be running after the building process. (This may take a while.)    

Right now, following ports are used:
- API: localhost:8080
- DB: localhost:5432

(You can change the ports in docker-compose.yml)


## Usage

### Bulk ingest
Semantic Scholar offers a bulk download divided into around 6000 batches with 30000 JSON line entries each.
To digest these files, it is assumed that you download and decrompress the files of interest into some data directory. All files passed by Rest API method call will be digested into the database instance named "scholar".

See chapter "Rest API requests" below on how to initiate the process.    

See:
- http://s2-public-api-prod.us-west-2.elasticbeanstalk.com/corpus/
- http://s2-public-api-prod.us-west-2.elasticbeanstalk.com/corpus/download/

Getting files with curl (i.e. for OSX user):
- get the manifest.txt file
```
$ curl -O https://s3-us-west-2.amazonaws.com/ai2-s2-research-public/open-corpus/2020-11-06/manifest.txt
```
- get individual files from manifest.txt listing (stringly recommended)
```
$ curl -O https://s3-us-west-2.amazonaws.com/ai2-s2-research-public/open-corpus/2020-11-06/s2-corpus-000.gz
```

## Semantic Scholar JSON
Check out this [JSON example](readme_files/semantic_scholar_corpus_entry_example.json) from corpus download.

## Database schema
![Database schema](readme_files/database_schema.png)

## Rest API requests

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
Request
```
POST http://localhost:8080
Content-Type: application/json

{
    "jsonrpc": "2.0",
    "id": 12345,
    "method": "ingest.bulk",
    "params": {
        "filepaths": [
            "/Users/karin/programming/data/academic_paper/semanticscholar/s2-corpus-000"
        ]
    }
}
```

Response
```
SOMETHING
```