import random
from faker import Faker
from api.utils.mongo_client import get_mongo_db
from datetime import datetime
from django.db import connection

"""
Seeder para popular a coleção no MongoDB: extra hours.
"""

def seed(quantity=100):
    fake = Faker()
    db = get_mongo_db()
    extrahours_collection = db['extrahours']

    today = datetime.now().date().isoformat()  

    with connection.cursor() as cursor:
        cursor.execute("SELECT id_employee FROM employees;")
        employees = [str(row[0]) for row in cursor.fetchall()]
        if not employees:
            print("No employees found. Please create employees before running the attendance seeder.")
            return

    available_employees = [
        emp for emp in employees
        if not extrahours_collection.find_one({"id_employee": emp, "date": today})
    ]
    for _ in range(quantity):
        if not available_employees:
            print("All employees already have records for today.")
            break

        id_employee = random.choice(available_employees)
        available_employees.remove(id_employee)

        startTime = fake.iso8601()
        endTime = fake.iso8601()

        extrahour = {
            "id_employee": id_employee,
            "date": today,
            "startTime": startTime,
            "endTime": endTime,
        }
        extrahours_collection.insert_one(extrahour)

        if (quantity >= 4) and ((_ + 1) % (quantity // 4) == 0):  # 25% checkpoints
            print(f"Progress: {((_ + 1) / quantity) * 100:.0f}% completed.")

    print(f"{quantity} registros inseridos na coleção 'extrahours'.")

def delete(quantity=None):
    db = get_mongo_db()
    collection = extrahours_collection = db['extrahours']
    result = extrahours_collection.delete_many({})
    print(f"{result.deleted_count} registros deletados da coleção '{collection}'.")