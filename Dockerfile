FROM python:3.10-alpine

COPY requirement.txt /tmp

RUN pip install -r /tmp/requirement.txt

COPY ./src /src

ARG API_KEY
ARG NHS_KID
ARG NHS_API_KEY
ARG NHS_PRIVATE_KEY

ENV API_KEY=$API_KEY
ENV NHS_KID=$NHS_KID
ENV NHS_API_KEY=$NHS_API_KEY
ENV NHS_PRIVATE_KEY=$NHS_PRIVATE_KEY

CMD python /src/app.py
