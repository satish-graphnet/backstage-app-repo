FROM python:3.10-alpine

COPY requirement.txt /tmp

RUN pip install -r /tmp/requirement.txt

COPY ./src /src

CMD python /src/app.py
