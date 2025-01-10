import random
from faker import Faker
from api.utils.mongo_client import get_mongo_db
from datetime import datetime
from django.db import connection

"""
Seeder para popular a coleção no MongoDB: schedule.
"""

def seed(quantity=100):
    fake = Faker()
    db = get_mongo_db()
    schedule_collection = db['schedule']

    weekdays = ["monday", "tuesday", "wednesday", "thursday", "friday"]

    with connection.cursor() as cursor:
        cursor.execute("SELECT id_employee FROM employees;")
        employees = [str(row[0]) for row in cursor.fetchall()]
        if not employees:
            print("No employees found. Please create employees before running the attendance seeder.")
            return

    quantity = min(quantity, len(employees))



    available_employees = [
        emp for emp in employees
        if not schedule_collection.find_one({"id_employee": emp})
    ]
    for _ in range(quantity):
        if not available_employees:
            print("All employees already have records.")
            break

        id_employee = random.choice(available_employees)
        available_employees.remove(id_employee)

        schedule = {
            "id_employee": id_employee,
            "workSchedule": {
                day: {
                    "start": "09:00",
                    "end": "17:00"
                } for day in weekdays
            }
        }
        schedule_collection.insert_one(schedule)

        if (quantity >= 4) and ((_ + 1) % (quantity // 4) == 0):  # 25% checkpoints
            print(f"Progress: {((_ + 1) / quantity) * 100:.0f}% completed.")

    print(f"{quantity} registros inseridos na coleção 'schedule'.")

def delete(quantity=None):
    db = get_mongo_db()
    collection = schedule_collection = db['schedule']
    result = schedule_collection.delete_many({})
    print(f"{result.deleted_count} registros deletados da coleção '{collection}'.")