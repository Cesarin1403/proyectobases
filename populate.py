# populate.py
# Por ahora este archivo solo describe, paso a paso, como vamos a cargar los datos
# de prueba en las tres bases de datos. El codigo lo agregamos en la siguiente entrega.

# Generar los datos de prueba
# - Usamos la libreria random de Python, igual que en el lab de logistica.
# - En la carpeta data/ guardamos listas fijas en archivos CSV, como el books.csv del
#   lab de libros: nombres de empleados, departamentos, estados, prioridades y etiquetas.
# - Con random.choice() elegimos valores de esas listas, con random.randint() inventamos
#   cantidades, horas y fechas, y con uuid.uuid4() creamos los ids de los eventos.
# - Primero generamos lo "base": empleados, equipos, proyectos y tareas, cada uno con
#   su id (EMP-001, TEAM-01, PRJ-001, TSK-0001).
# - Las tres bases usan los mismos ids, asi un empleado o una tarea es la misma en
#   MongoDB, Cassandra y Dgraph.

# Conectarnos

# - Usamos las funciones de connect.py: get_mongo_db(), get_cassandra_session()
#   y get_dgraph_client().

# MongoDB

# - Crear los indices con create_indexes(db) de Mongo/mongo.py.
# - Insertar los proyectos generados en la coleccion projects con insert_many().
#   Cada proyecto lleva adentro a su gerente (manager) y su configuracion (settings).
# - Insertar las tareas generadas en la coleccion tasks con insert_many().
#   A cada tarea le copiamos project_name y el responsable (assigned_to) para no
#   tener que juntar colecciones en las consultas.

# Cassandra

# - Crear las 6 tablas con create_schema(session) de Cassandra/cassandra.py.
# - Generar el historial a partir de las tareas: cambios de estado, reasignaciones,
#   comentarios y registros de horas, cada uno con su fecha y su uuid (uuid.uuid4()).
# - Insertar cada evento en todas las tablas donde se necesita (desnormalizacion):
#     * task_changes_by_task         -> todos los cambios de una tarea
#     * activity_by_employee_month   -> la actividad del empleado, con su year_month
#     * activity_by_project_day      -> la actividad del proyecto, con su activity_date
#     * hours_by_employee_month      -> solo los registros de horas
#     * comments_by_task             -> solo los comentarios
#     * completed_tasks_by_team      -> solo cuando una tarea pasa a "terminada"
# - Los INSERT se hacen con session.prepare() y session.execute() usando "?".

# Dgraph

# - Aplicar el esquema de Dgraph/schema.dql (en Ratel con Bulk Edit, o desde Python
#   con alter).
# - Hacer una mutacion "set" en JSON con los nodos Employee, Team, Project y Task,
#   cada uno con su dgraph.type.
# - Usar nodos en blanco (_:emp1, _:team1, ...) para crear en la misma mutacion las
#   relaciones members, leader, assigned_tasks, depends_on, teams y reports_to.

# Revisar que todo se cargo

# - MongoDB: contar documentos con count_documents({}).
# - Cassandra: SELECT de una particion de cada tabla.
# - Dgraph: una consulta con type(Employee) y count(uid) en Ratel.
# - Cerrar las conexiones con close_all().
