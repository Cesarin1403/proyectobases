from pymongo import MongoClient
from cassandra.cluster import Cluster
import pydgraph

MONGO_URI = "mongodb://localhost:27017/"
MONGO_DB = "taskflow"

CASSANDRA_HOST = "127.0.0.1"
CASSANDRA_PORT = 9042
KEYSPACE = "taskflow"

DGRAPH_ADDR = "localhost:9080"

CREATE_KEYSPACE = """
CREATE KEYSPACE IF NOT EXISTS taskflow
WITH replication = {'class': 'SimpleStrategy', 'replication_factor': 1}
"""


def get_mongo_db():
    client = MongoClient(MONGO_URI)
    db = client[MONGO_DB]
    return client, db


def get_cassandra_session():
    cluster = Cluster([CASSANDRA_HOST], port=CASSANDRA_PORT)
    session = cluster.connect()
    session.execute(CREATE_KEYSPACE)
    session.set_keyspace(KEYSPACE)
    return cluster, session


def get_dgraph_client():
    stub = pydgraph.DgraphClientStub(DGRAPH_ADDR)
    client = pydgraph.DgraphClient(stub)
    return stub, client


def close_all(mongo_client, cassandra_cluster, dgraph_stub):
    mongo_client.close()
    cassandra_cluster.shutdown()
    dgraph_stub.close()



