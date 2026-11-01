from connect import get_mongo_db, get_cassandra_session, get_dgraph_client, close_all
from schema import create_cassandra_tables, create_mongo_indexes

mongo_client, db = get_mongo_db()
cassandra_cluster, session = get_cassandra_session()

create_cassandra_tables(session)
create_mongo_indexes(db)