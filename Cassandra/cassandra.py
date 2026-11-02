from datetime import datetime

KEYSPACE = "taskflow"

CREATE_TABLES = {
    "task_changes_by_task": """
        CREATE TABLE IF NOT EXISTS task_changes_by_task (
            task_id text,
            change_timestamp timestamp,
            change_id uuid,
            employee_id text,
            change_type text,
            old_value text,
            new_value text,
            PRIMARY KEY ((task_id), change_timestamp, change_id)
        ) WITH CLUSTERING ORDER BY (change_timestamp DESC, change_id ASC)
    """,
    "activity_by_employee_month": """
        CREATE TABLE IF NOT EXISTS activity_by_employee_month (
            employee_id text,
            year_month text,
            activity_timestamp timestamp,
            activity_id uuid,
            task_id text,
            project_id text,
            activity_type text,
            description text,
            PRIMARY KEY ((employee_id, year_month), activity_timestamp, activity_id)
        ) WITH CLUSTERING ORDER BY (activity_timestamp DESC, activity_id ASC)
    """,
    "activity_by_project_day": """
        CREATE TABLE IF NOT EXISTS activity_by_project_day (
            project_id text,
            activity_date text,
            activity_timestamp timestamp,
            activity_id uuid,
            task_id text,
            employee_id text,
            activity_type text,
            description text,
            PRIMARY KEY ((project_id, activity_date), activity_timestamp, activity_id)
        ) WITH CLUSTERING ORDER BY (activity_timestamp DESC, activity_id ASC)
    """,
    "hours_by_employee_month": """
        CREATE TABLE IF NOT EXISTS hours_by_employee_month (
            employee_id text,
            year_month text,
            log_date timestamp,
            log_id uuid,
            task_id text,
            project_id text,
            hours_worked decimal,
            PRIMARY KEY ((employee_id, year_month), log_date, log_id)
        ) WITH CLUSTERING ORDER BY (log_date DESC, log_id ASC)
    """,
    "comments_by_task": """
        CREATE TABLE IF NOT EXISTS comments_by_task (
            task_id text,
            comment_timestamp timestamp,
            comment_id uuid,
            employee_id text,
            employee_name text,
            comment_text text,
            PRIMARY KEY ((task_id), comment_timestamp, comment_id)
        ) WITH CLUSTERING ORDER BY (comment_timestamp DESC, comment_id ASC)
    """,
    "completed_tasks_by_team": """
        CREATE TABLE IF NOT EXISTS completed_tasks_by_team (
            team_id text,
            completed_at timestamp,
            task_id text,
            task_title text,
            project_id text,
            employee_id text,
            PRIMARY KEY ((team_id), completed_at, task_id)
        ) WITH CLUSTERING ORDER BY (completed_at DESC, task_id ASC)
    """,
}

QUERIES = {
    "R1": """
        SELECT task_id, change_timestamp, employee_id, change_type, old_value, new_value
        FROM task_changes_by_task
        WHERE task_id = ?
        LIMIT 20
    """,
    "R2": """
        SELECT employee_id, activity_timestamp, task_id, project_id, activity_type, description
        FROM activity_by_employee_month
        WHERE employee_id = ? AND year_month = ?
          AND activity_timestamp >= ? AND activity_timestamp <= ?
    """,
    "R3": """
        SELECT project_id, activity_date, activity_timestamp, task_id, employee_id, activity_type, description
        FROM activity_by_project_day
        WHERE project_id = ? AND activity_date = ?
    """,
    "R4": """
        SELECT employee_id, year_month, log_date, task_id, project_id, hours_worked
        FROM hours_by_employee_month
        WHERE employee_id = ? AND year_month = ?
    """,
    "R5": """
        SELECT task_id, comment_timestamp, employee_id, employee_name, comment_text
        FROM comments_by_task
        WHERE task_id = ?
        LIMIT 10
    """,
    "R6": """
        SELECT team_id, completed_at, task_id, task_title, project_id, employee_id
        FROM completed_tasks_by_team
        WHERE team_id = ? AND completed_at >= ? AND completed_at <= ?
    """,
}

_prepared = {}


def create_schema(session):
    for statement in CREATE_TABLES.values():
        session.execute(statement)


def _stmt(session, key):
    if key not in _prepared:
        _prepared[key] = session.prepare(QUERIES[key])
    return _prepared[key]


def insert_rows(session, table, rows):
    if not rows:
        return 0
    columns = list(rows[0].keys())
    cql = f"INSERT INTO {table} ({', '.join(columns)}) VALUES ({', '.join('?' for _ in columns)})"
    statement = session.prepare(cql)
    for row in rows:
        session.execute(statement, [row[c] for c in columns])
    return len(rows)


def year_month(value):
    return value.strftime("%Y-%m")


def months_between(start, end):
    months = []
    year, month = end.year, end.month
    while (year, month) >= (start.year, start.month):
        months.append(f"{year:04d}-{month:02d}")
        month -= 1
        if month == 0:
            year, month = year - 1, 12
    return months


def get_task_changes(session, task_id):
    return list(session.execute(_stmt(session, "R1"), (task_id,)))


def get_employee_activity(session, employee_id, start: datetime, end: datetime):
    rows = []
    for ym in months_between(start, end):
        rows.extend(session.execute(_stmt(session, "R2"), (employee_id, ym, start, end)))
    return rows


def get_project_activity_by_day(session, project_id, day: str):
    return list(session.execute(_stmt(session, "R3"), (project_id, day)))


def get_employee_hours(session, employee_id, ym: str):
    return list(session.execute(_stmt(session, "R4"), (employee_id, ym)))


def get_task_comments(session, task_id):
    return list(session.execute(_stmt(session, "R5"), (task_id,)))


def get_team_completed_tasks(session, team_id, start: datetime, end: datetime):
    return list(session.execute(_stmt(session, "R6"), (team_id, start, end)))