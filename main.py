# main.py
# Menu de consultas de TaskFlow.
# Por ahora solo muestra las consultas planeadas; la logica de cada una
# (las funciones de Cassandra/, Mongo/ y Dgraph/) la conectamos en la siguiente entrega.

MENU = {
    "Cassandra": [
        "Historial de cambios de una tarea",
        "Actividad de un empleado en un rango de fechas",
        "Actividad de un proyecto en un dia especifico",
        "Horas registradas por un empleado en un mes",
        "Ultimos comentarios de una tarea",
        "Tareas completadas por un equipo en un rango de fechas",
    ],
    "MongoDB": [
        "Detalle completo de un proyecto",
        "Tareas de un proyecto por estado y prioridad",
        "Tareas con una etiqueta especifica",
        "Tareas vencidas de un proyecto",
        "Conteo de tareas por estado de un proyecto (agregacion)",
        "Presupuesto y numero de proyectos por departamento (agregacion)",
    ],
    "Dgraph": [
        "Miembros de un equipo y sus tareas en progreso",
        "Dependencias directas de una tarea",
        "Tareas afectadas por el retraso de una tarea",
        "Carga de trabajo de los integrantes de un equipo",
        "Equipos y lideres que participan en un proyecto",
        "Cadena de mando de un empleado",
    ],
}


def print_menu():
    print("\nTaskFlow")
    number = 1
    options = {}
    for database, queries in MENU.items():
        print(f"\n--- {database} ---")
        for query in queries:
            print(f"{number:2d}. {query}")
            options[str(number)] = (database, query)
            number += 1
    print("\n 0. Salir")
    return options


def main():
    while True:
        options = print_menu()
        choice = input("\nElige una opcion: ").strip()
        if choice == "0":
            print("Hasta luego")
            break
        if choice in options:
            database, query = options[choice]
            print(f"\n[{database}] {query}")
            print("Esta consulta se implementa en la siguiente entrega.")
        else:
            print("Opcion no valida, intenta otra vez.")


if __name__ == "__main__":
    main()
