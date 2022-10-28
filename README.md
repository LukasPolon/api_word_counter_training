# api_word_counter_training

## Requirements:
1. "word_counter" endpoint:
   1. Receives a text input and counts the number of appearances for each word in the
      input. 
   2. The endpoint should not return data (but you may return success status, etc.). 
   3. The endpoint should be able to accept the input in three ways:
      i. A simple string is sent in the request.
      ii. A file path (the file's contents will be used as an input).
      iii. A URL (the data returned from the URL will be used as an input). 
   4. The input may be very large (up to tens of gigabytes). 
   5. The result (the number of appearances of each word) should be persisted, and
      used by the "word_statistics" endpoint.
2. "word_statistics" endpoint:
   1. Receives a word and returns the number of times the word appeared so far (in all
   previous calls).

### Dependencies:
Python3.10, Docker (tested on 20.10.11), Docker-compose (tested on 1.29.2)

Application was created in Windows environment.

### Usage (in order):
``` 
make install-all        : install virtualenv, main dependencies, lint dependencies and test dependencies
make mypy               : run static code analysis
make unittests          : run unit tests


cd deployment
docker-compose up -d    : run database and httpd service in a containers
cd ..

source ./.venv/bin/activate (or ./.venv/Scripts/activate.bat)
make develop

make functional-tests   : run functional tests
```

Ports used by the application and where to change them if case of they are already in use:
- 5432: PG database -> deployment/docker-compose.yaml & app/constants.py
- 8080: httpd -> deployment/docker-compose.yaml
- 8000: api -> app/manager.py & tests/functional/conftest.py

### CLI usage:
```
source ./.venv/bin/activate

awct-manage run-app             : run uvicorn server with application
awct-manage db [create|delete]  : create or delete database schema

```

### CURL usage examples:

- database must be up and created
- uvicorn server must be running


/word_counter
```
curl --location --request "POST" "http://127.0.0.1:8000/word_counter/" \
--header "Content-Type: multipart/form-data" \
--form "file=@<file_path>"

curl --location --request "POST" "http://127.0.0.1:8000/word_counter/?string_param=<content>"

curl --location --request "POST" "http://127.0.0.1:8000/word_counter/?url=http://127.0.0.1:8080/test_file.txt"
```

/word_statistics
```
curl --location --request "GET" "http://127.0.0.1:8000/word_statistics/?word=<word>"
```

### Assumptions:
- Uploaded file size must not cause memory issues during upload, but time of the upload is not taken into account
- Uploaded file is a document which can consist of: words, non-alphanumeric characters, line breakers (\n)
- Database stores records about words, including date and time of the upload
- API does not follow REST
- unit tests and functional tests are examples


### Needs to be done better:
- functional tests -> application should run in a container, fixtures should rarely use subprocess to prepare environment
- there is Interface Segregation Principle violation in Publisher protocols
- there is almost no error handling - custom exceptions and handlers are needed
- handlers and factories from word_counter router could be moved to separated module, or re-designed
- Database credentials should be stored more safely, not hardcoded


#### Comment: database commit is a major bottleneck in the API. It may be solved by:
- using threading: database commit is a good task for threads, but it provides minor performance improvement (fun fact: ThreadPoolExecutor have big, unexpected issues with Gensim)
- using multiprocessing: each Chunk can be processed separately, so it is possible to aggregate sets of Chunks and execute them in separated process
- using message brokers (e.g. RabbitMQ): separated, scalable services would receive and save data
- using task queues (e.g. Celery), similar to message brokers (Celery actually uses one)
- re-designing database - data can be saved in e.g. noSQL database in one document; incrementation of the value may be faster