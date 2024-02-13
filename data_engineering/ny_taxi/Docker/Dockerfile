FROM python:3.9

RUN apt-get install wget
RUN pip install pyarrow postgres pandas sqlalchemy


COPY ingest_taxi.py ingest_taxi.py

ENTRYPOINT [ "python","ingest_taxi.py" ]