FROM python:3.7.10-slim-buster as python-base

ENV PYTHONUNBUFFERED=1 
ENV PYTHONDONTWRITEBYTECODE=1 
ENV PIP_NO_CACHE_DIR=off 
ENV PIP_DISABLE_PIP_VERSION_CHECK=on 

FROM python-base as builder-base
RUN apt-get update && apt-get install --no-install-recommends -y curl build-essential

COPY requirements.txt data/requirements.txt
COPY bookscrape.py /data/bookscrape.py
RUN pip install -r /data/requirements.txt

ENV PYTHONPATH=/data:$PYTHONPATH
# CMD [ "python", "/data/bookscrape.py" ]