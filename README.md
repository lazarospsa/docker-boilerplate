# Coding Challenge: Multi-layer product

Purpose of this challenge is to design a multi-layer product that requires the following components:

- a **database layer**, which is a MySQL database (A)
- a **cache layer**, which is a Redis sever (B)
- a **messaging layer**, which is an Apache Kafka server (C)
- an **application layer**, which is a REST API web application (D)

All of the components are implemented on separate Docker containers, and the whole infrastracture is deployed with docker-compose.

## Usage

1. docker-compose up
2. Visit http://localhost:8000/status


## Details

Specifically, by executing:

> docker-compose up

in the directory containing the docker-compose.yaml, five containers are starting up (including a zookeeper docker container, which is a
centralized service for maintaining configuration information, naming, providing distributed synchronization, and providing group services,
required for the operation of an Apache Kafka server).

For layers **A, B**, and **C**, images from the Docker Hub are used with minimal required configuration. **As for layer D**, a **Flask API** is implemented
in Python, and a container is created from a Dockerfile, setting the required parameters and installing the needed modules stated in requirements.txt.
All the API related files are located in **/api** folder.

All containers exist in the same private network, with only one entry point to the external network, which is the web application.

Layers **A** and **C** persist data in their respective volumes.

To query the API, make an HTTP GET request to the following URL:

> http://localhost:8000/status

The API is checking the connection status of the other components and sending back a status response in JSON following the schema bellow:
'''
{
  "Database": boolean,
  "Cache": boolean,
  "Messaging": boolean
}
'''
where the **True** status indicates that layer is up, running, and responsive, whereas **False** indicates unresponsive service.


Python - Flask (API)
> http://localhost:8000/status

Golang - Web App
> http://localhost:8001/lazaros