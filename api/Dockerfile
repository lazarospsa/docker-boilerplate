FROM python:3
#WORKDIR .
COPY . /usr/src/app
WORKDIR /usr/src/app
RUN apt-get update
RUN pip3 install -r requirements.txt
CMD python3 api.py
