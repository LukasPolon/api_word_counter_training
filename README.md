# api_word_counter_training
### Usage (in order):
``` 
make install-all        : install virtualenv, main dependencies, lint dependencies and test dependencies
make mypy               : run static code analysis
make unittests          : run unit tests

source ./.venv/bin/activate (or ./.venv/Scripts/activate.bat)
make develop

make functional-tests   : run functional tests
```
### CLI usage:
```
source ./.venv/bin/activate

awct-manage run-app             : run uvicorn server
awct-manage db [create|delete]  : create or delete database schema

```

### Dependencies:
Python3.10, Docker (tested on 20.10.11), Docker-compose (tested on 1.29.2)

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