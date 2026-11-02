from datetime import datetime


def create_indexes(db):
    db.projects.create_index({"project_id": 1})
    db.projects.create_index({"start_date": 1})
    db.tasks.create_index({"project_id": 1, "status": 1, "priority": 1, "due_date": 1})
    db.tasks.create_index({"project_id": 1, "due_date": 1})
    db.tasks.create_index({"tags": 1})


def create_schema(db):
    create_indexes(db)


def get_project_detail(db, project_id):
    pipeline = [
        {"$match": {"project_id": project_id}},
        {"$lookup": {
            "from": "tasks",
            "localField": "project_id",
            "foreignField": "project_id",
            "as": "tasks",
        }},
        {"$project": {
            "_id": 0, "project_id": 1, "name": 1, "description": 1,
            "manager.name": 1, "manager.email": 1,
            "start_date": 1, "end_date": 1, "budget": 1, "status": 1,
            "tasks.task_id": 1, "tasks.title": 1, "tasks.status": 1,
            "tasks.priority": 1, "tasks.due_date": 1,
        }},
    ]
    result = list(db.projects.aggregate(pipeline))
    return result[0] if result else None


def get_tasks_by_status_priority(db, project_id, status, priority):
    pipeline = [
        {"$match": {"project_id": project_id, "status": status, "priority": priority}},
        {"$project": {"_id": 0, "task_id": 1, "title": 1, "status": 1, "priority": 1,
                      "due_date": 1, "assigned_to": 1}},
        {"$sort": {"due_date": 1}},
    ]
    return list(db.tasks.aggregate(pipeline))


def get_tasks_by_tag(db, tag):
    return list(db.tasks.find(
        {"tags": tag},
        {"_id": 0, "task_id": 1, "title": 1, "project_name": 1, "status": 1, "tags": 1},
    ))


def get_overdue_tasks(db, project_id, reference_date: datetime):
    pipeline = [
        {"$match": {"project_id": project_id, "due_date": {"$lt": reference_date},
                    "status": {"$ne": "terminada"}}},
        {"$project": {"_id": 0, "task_id": 1, "title": 1, "due_date": 1, "status": 1,
                      "assigned_to": 1}},
        {"$sort": {"due_date": 1}},
    ]
    return list(db.tasks.aggregate(pipeline))


def count_tasks_by_status(db, project_id):
    pipeline = [
        {"$match": {"project_id": project_id}},
        {"$group": {"_id": "$status", "total_tasks": {"$sum": 1}}},
        {"$project": {"_id": 0, "status": "$_id", "total_tasks": 1}},
        {"$sort": {"total_tasks": -1}},
    ]
    return list(db.tasks.aggregate(pipeline))


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