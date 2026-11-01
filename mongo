from datetime import datetime

from pymongo import ASCENDING
from pymongo.errors import CollectionInvalid

PROJECT_SCHEMA = {
    "$jsonSchema": {
        "bsonType": "object",
        "required": ["project_id", "name", "department", "manager", "start_date", "budget", "status", "settings"],
        "properties": {
            "project_id": {"bsonType": "string"},
            "name": {"bsonType": "string"},
            "description": {"bsonType": "string"},
            "department": {"bsonType": "string"},
            "manager": {
                "bsonType": "object",
                "required": ["employee_id", "name", "email"],
                "properties": {
                    "employee_id": {"bsonType": "string"},
                    "name": {"bsonType": "string"},
                    "email": {"bsonType": "string"},
                },
            },
            "start_date": {"bsonType": "date"},
            "end_date": {"bsonType": "date"},
            "budget": {"bsonType": ["double", "int", "long"]},
            "status": {"enum": ["activo", "pausado", "cerrado"]},
            "settings": {
                "bsonType": "object",
                "properties": {
                    "allowed_statuses": {"bsonType": "array", "items": {"bsonType": "string"}},
                    "priority_levels": {"bsonType": "array", "items": {"bsonType": "string"}},
                    "working_days": {"bsonType": "array", "items": {"bsonType": "string"}},
                    "requires_hour_estimate": {"bsonType": "bool"},
                },
            },
        },
    }
}

TASK_SCHEMA = {
    "$jsonSchema": {
        "bsonType": "object",
        "required": ["task_id", "project_id", "project_name", "title", "status", "priority", "due_date"],
        "properties": {
            "task_id": {"bsonType": "string"},
            "project_id": {"bsonType": "string"},
            "project_name": {"bsonType": "string"},
            "title": {"bsonType": "string"},
            "description": {"bsonType": "string"},
            "status": {"enum": ["pendiente", "en progreso", "en revisión", "terminada"]},
            "priority": {"enum": ["baja", "media", "alta"]},
            "due_date": {"bsonType": "date"},
            "created_at": {"bsonType": "date"},
            "tags": {"bsonType": "array", "items": {"bsonType": "string"}},
            "assigned_to": {
                "bsonType": "object",
                "properties": {
                    "employee_id": {"bsonType": "string"},
                    "name": {"bsonType": "string"},
                },
            },
            "estimated_hours": {"bsonType": ["int", "long"]},
        },
    }
}


def create_collections(db):
    for name, schema in (("projects", PROJECT_SCHEMA), ("tasks", TASK_SCHEMA)):
        try:
            db.create_collection(name, validator=schema)
        except CollectionInvalid:
            db.command("collMod", name, validator=schema)


def create_indexes(db):
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


def create_schema(db):
    create_collections(db)
    create_indexes(db)


def get_project_detail(db, project_id):
    pipeline = [
        {"$match": {"project_id": project_id}},
        {"$lookup": {
            "from": "tasks",
            "localField": "project_id",
            "foreignField": "project_id",
            "as": "tasks",
            "pipeline": [
                {"$project": {"_id": 0, "task_id": 1, "title": 1, "status": 1, "priority": 1, "due_date": 1}},
            ],
        }},
        {"$project": {
            "_id": 0, "project_id": 1, "name": 1, "description": 1,
            "manager": {"name": "$manager.name", "email": "$manager.email"},
            "start_date": 1, "end_date": 1, "budget": 1, "status": 1, "tasks": 1,
        }},
    ]
    result = list(db.projects.aggregate(pipeline))
    return result[0] if result else None


def get_tasks_by_status_priority(db, project_id, status, priority):
    return list(db.tasks.find(
        {"project_id": project_id, "status": status, "priority": priority},
        {"_id": 0, "task_id": 1, "title": 1, "status": 1, "priority": 1, "due_date": 1, "assigned_to": 1},
    ).sort("due_date", ASCENDING))


def get_tasks_by_tag(db, tag):
    return list(db.tasks.find(
        {"tags": tag},
        {"_id": 0, "task_id": 1, "title": 1, "project_name": 1, "status": 1, "tags": 1},
    ))


def get_overdue_tasks(db, project_id, reference_date: datetime):
    return list(db.tasks.find(
        {"project_id": project_id, "due_date": {"$lt": reference_date}, "status": {"$ne": "terminada"}},
        {"_id": 0, "task_id": 1, "title": 1, "due_date": 1, "status": 1, "assigned_to": 1},
    ).sort("due_date", ASCENDING))


def get_project_settings(db, project_id):
    return db.projects.find_one(
        {"project_id": project_id},
        {"_id": 0, "project_id": 1, "name": 1, "settings": 1},
    )


def count_tasks_by_status(db, project_id):
    pipeline = [
        {"$match": {"project_id": project_id}},
        {"$group": {"_id": "$status", "total_tasks": {"$sum": 1}}},
        {"$project": {"_id": 0, "status": "$_id", "total_tasks": 1}},
        {"$sort": {"total_tasks": -1}},
    ]
    return list(db.tasks.aggregate(pipeline))


def get_active_projects_progress(db):
    pipeline = [
        {"$match": {"status": "activo"}},
        {"$lookup": {
            "from": "tasks",
            "localField": "project_id",
            "foreignField": "project_id",
            "as": "tasks",
            "pipeline": [{"$project": {"_id": 0, "status": 1}}],
        }},
        {"$project": {
            "_id": 0, "project_id": 1, "name": 1,
            "total_tasks": {"$size": "$tasks"},
            "completed_tasks": {"$size": {
                "$filter": {"input": "$tasks", "cond": {"$eq": ["$$this.status", "terminada"]}},
            }},
        }},
        {"$addFields": {
            "progress_percentage": {"$cond": [
                {"$eq": ["$total_tasks", 0]},
                0,
                {"$round": [{"$multiply": [{"$divide": ["$completed_tasks", "$total_tasks"]}, 100]}, 2]},
            ]},
        }},
        {"$sort": {"progress_percentage": -1}},
    ]
    return list(db.projects.aggregate(pipeline))


def get_budget_by_department(db, year: int):
    pipeline = [
        {"$match": {"start_date": {"$gte": datetime(year, 1, 1), "$lt": datetime(year + 1, 1, 1)}}},
        {"$group": {
            "_id": "$department",
            "total_projects": {"$sum": 1},
            "total_budget": {"$sum": "$budget"},
        }},
        {"$project": {"_id": 0, "department": "$_id", "total_projects": 1, "total_budget": 1}},
        {"$sort": {"total_budget": -1}},
    ]
    return list(db.projects.aggregate(pipeline))
