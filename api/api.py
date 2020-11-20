import mysql.connector
import redis
from pykafka import KafkaClient
from pykafka.exceptions import KafkaException
from mysql.connector import Error
from flask import Flask, jsonify

app = Flask("Status_check_API")

class ConnStatus(object):
    """ Class for creating connection object. Class methods check
        connectivity for each component accordingly.
    """
    def __init__(self):
        self.database = False
        self.cache = False
        self.messaging = False

    def check_db(self):
        """ Function to request status of MySQL database.
            Gets response by connecting as a user to DB container.
        """
        try:

            connection = mysql.connector.connect(host='mysql', port='3306',
                                                 user='root', password='password')
            if connection.is_connected():
                self.database = True
            connection.close()
        except Error:
            print("connection check failed")
        return self.database

    def check_cache(self):
        """ Function to request status of Redis Server.
            Works by pinging the server through the redis python module.
        """
        try:
            r = redis.Redis(host='redis', port=6379)

            if r.ping():
                self.cache = True
        except redis.ConnectionError:
            print("Connection check failed")
        return self.cache

    def check_messaging(self):
        """ Function to request the status of Kafka Cluster.
        """
        try:
            client = KafkaClient("kafka:9092")

            if client:
                self.messaging = True
        except KafkaException:
            print("Connection check failed")
        return self.messaging


@app.route("/status", methods=['GET'])
def check_status():
    conn = ConnStatus()
    status = {'Database': '%s' % conn.check_db(),
              'Cache': '%s' % conn.check_cache(),
              'Messaging': '%s' % conn.check_messaging()}
    resp = jsonify(status)
    resp.status_code = 200
    return resp

@app.route("/", methods=['GET'])
def begin():
    user = {'User': 'Lazaros Psarokostas'}
    resp = jsonify(user)
    resp.status_code = 200
    return resp

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True, threaded=True)
