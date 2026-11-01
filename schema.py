from pymongo import ASCENDING

CASSANDRA_TABLES = [
    """
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
    """
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
    """
    CREATE TABLE IF NOT EXISTS activity_by_project_day (
        project_id text,
        activity_date date,
        activity_timestamp timestamp,
        activity_id uuid,
        task_id text,
        employee_id text,
        activity_type text,
        description text,
        PRIMARY KEY ((project_id, activity_date), activity_timestamp, activity_id)
    ) WITH CLUSTERING ORDER BY (activity_timestamp DESC, activity_id ASC)
    """,
    """
    CREATE TABLE IF NOT EXISTS status_changes_by_task (
        task_id text,
        change_timestamp timestamp,
        change_id uuid,
        previous_status text,
        new_status text,
        employee_id text,
        PRIMARY KEY ((task_id), change_timestamp, change_id)
    ) WITH CLUSTERING ORDER BY (change_timestamp ASC, change_id ASC)
    """,
    """
    CREATE TABLE IF NOT EXISTS hours_by_employee_month (
        employee_id text,
        year_month text,
        log_date date,
        log_id uuid,
        task_id text,
        project_id text,
        hours_worked decimal,
        PRIMARY KEY ((employee_id, year_month), log_date, log_id)
    ) WITH CLUSTERING ORDER BY (log_date DESC, log_id ASC)
    """,
    """
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
    """
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
    """
    CREATE TABLE IF NOT EXISTS activity_by_project_employee (
        project_id text,
        employee_id text,
        activity_timestamp timestamp,
        activity_id uuid,
        task_id text,
        activity_type text,
        description text,
        PRIMARY KEY ((project_id, employee_id), activity_timestamp, activity_id)
    ) WITH CLUSTERING ORDER BY (activity_timestamp DESC, activity_id ASC)
    """,
]


def create_cassandra_tables(session):
    for statement in CASSANDRA_TABLES:
        session.execute(statement)


def create_mongo_indexes(db):
    db.projects.create_index([("project_id", ASCENDING)], unique=True)
    db.projects.create_index([("status", ASCENDING)])
    db.projects.create_index([("start_date", ASCENDING)])
    db.tasks.create_index([("task_id", ASCENDING)], unique=True)
    db.tasks.create_index([
        ("project_id", ASCENDING),
        ("status", ASCENDING),
        ("priority", ASCENDING),
        ("due_date", ASCENDING),
    ])
    db.tasks.create_index([("project_id", ASCENDING), ("due_date", ASCENDING)])
    db.tasks.create_index([("tags", ASCENDING)])