# TaskFlow: Sistema de Gestión de Proyectos Empresariales

Proyecto final de **Bases de Datos No Relacionales**, ITESO, otoño 2026.
Profesora: Ing. Ivanna Haro.

## Integrantes

Jaime Galván Mendoza  759023 
Cesar Alejandro Carpio Esparza  755949 

## ¿Qué es el proyecto?

TaskFlow es una aplicación de consola para empresas medianas que necesitan organizar sus proyectos, repartir las tareas entre sus empleados y darle seguimiento al trabajo. El proyecto solo hace consultas: los datos se cargan como datos de prueba y la aplicación los consulta desde un menú.

Usamos tres bases de datos, cada una para lo que mejor sabe hacer:

- **MongoDB:** guarda la información completa de cada proyecto y sus tareas en documentos flexibles. Sirve para buscar con filtros y hacer agregaciones, como contar tareas por estado o sumar presupuestos por departamento.
- **Cassandra:** guarda la bitácora en el tiempo: cambios de las tareas, actividad, comentarios y horas trabajadas. Sirve para consultar el historial por tarea, por empleado, por proyecto o por fecha.
- **Dgraph:** guarda las conexiones entre empleados, equipos, proyectos y tareas. Sirve para recorrer relaciones, como los integrantes de un equipo, las dependencias entre tareas o la cadena de jefes de un empleado.

Implementamos 6 requerimientos por cada base de datos, 18 en total.

## Estructura del repositorio

```
proyectobases/
├── Cassandra/     tablas y consultas CQL
├── Mongo/         índices y consultas de MongoDB
├── Dgraph/        esquema de Dgraph
├── data/          datos de prueba
├── connect.py     conexión a las tres bases de datos
├── populate.py    pasos para cargar los datos de prueba
├── main.py        menú de consultas
├── requirements.txt  librerías de Python
└── README.md
```

## Flujo de trabajo

> Este flujo es un borrador inicial y lo vamos a ir mejorando conforme avance el proyecto.

**1. Levantar las bases de datos con Docker**

```
docker run --name mongodb -d -p 27017:27017 mongo
docker run --name cassandra-db -d -p 9042:9042 cassandra
docker run --name dgraph -d -p 8080:8080 -p 9080:9080 dgraph/standalone:latest
docker run --name ratel -d -p 8000:8000 dgraph/ratel:latest
```

Si los contenedores ya existen, solo se prenden con `docker start <nombre>`.

**2. Crear el ambiente virtual e instalar las librerías**

python3 -m venv ./venv
source venv/bin/activate
pip install -r requirements.txt

**3. Cargar el esquema de Dgraph**

Abrir Ratel en http://localhost:8000, ir a la pestaña Schema, elegir Bulk Edit y pegar el contenido de `Dgraph/schema.dql`.

**4. Probar las conexiones**

```
python3 connect.py
```

Si las tres bases están prendidas, imprime un mensaje por cada una.

**5. Cargar los datos de prueba**

python3 populate.py

Crea las tablas de Cassandra y los índices de MongoDB, y carga los datos de prueba en las tres bases.

**6. Correr las consultas**

python3 main.py

Muestra el menú con las consultas de cada base de datos para elegir cuál correr.
