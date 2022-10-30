FROM python:3.10

WORKDIR /awct

COPY requirements.txt requirements-dev.txt Makefile ./

# complex installation due to test setup simplification
RUN make install-all

COPY ./ ./

RUN make setup
CMD ["awct-manage", "run-app"]
