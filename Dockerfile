FROM python:3.9-buster

ENV PYTHONUNBUFFERED=1

WORKDIR /root
COPY requirements.txt /root/
RUN pip install -r requirements.txt

COPY brixilated/ /root/
