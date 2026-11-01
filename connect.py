from pymongo import MongoClient
from cassandra.cluster import Cluster
import pydgraph

# Datos de conexion (los mismos puertos que usamos al levantar los contenedores)
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
    # Conexion a MongoDB, igual que en el lab de libros
    client = MongoClient(MONGO_URI)
    db = client[MONGO_DB]
    return client, db


def get_cassandra_session():
    # Conexion a Cassandra, igual que en el lab de peliculas
    cluster = Cluster([CASSANDRA_HOST], port=CASSANDRA_PORT)
    session = cluster.connect()
    session.execute(CREATE_KEYSPACE)
    session.set_keyspace(KEYSPACE)
    return cluster, session


def get_dgraph_client():
    # Conexion a Dgraph por el puerto 9080 (gRPC) con la libreria pydgraph
    stub = pydgraph.DgraphClientStub(DGRAPH_ADDR)
    client = pydgraph.DgraphClient(stub)
    return stub, client


def close_all(mongo_client, cassandra_cluster, dgraph_stub):
    mongo_client.close()
    cassandra_cluster.shutdown()
    dgraph_stub.close()


# Si corremos este archivo solo, prueba las tres conexiones
if __name__ == "__main__":
    mongo_client, db = get_mongo_db()
    mongo_client.admin.command("ping")
    print("MongoDB conectado, base de datos:", db.name)

    cassandra_cluster, session = get_cassandra_session()
    version = session.execute("SELECT release_version FROM system.local").one()
    print("Cassandra conectado, keyspace:", KEYSPACE, "- version", version.release_version)

    dgraph_stub, dgraph_client = get_dgraph_client()
    print("Dgraph conectado, version", dgraph_client.check_version())

    close_all(mongo_client, cassandra_cluster, dgraph_stub)
    print("Las tres conexiones funcionan")
