import random
from faker import Faker
from api.utils.mongo_client import get_mongo_db
from datetime import datetime, timedelta
from django.db import connection

"""
Seeder para popular a coleção no MongoDB: attendance.
"""

def seed(quantity=100):
    fake = Faker()
    db = get_mongo_db()
    attendance_collection = db['attendance']
    quantity_days_prior = 3 # quantidade de dias anteriores para inserir registros

    with connection.cursor() as cursor:
        cursor.execute("SELECT id_employee FROM employees;")
        employees = [str(row[0]) for row in cursor.fetchall()]
        if not employees:
            print("No employees found. Please create employees before running the attendance seeder.")
            return

    quantity = min(quantity, len(employees))

    days = [(datetime.now() - timedelta(days=i)).date().isoformat() for i in range(quantity_days_prior)]

    counter = quantity_days_prior
    total_records = quantity * quantity_days_prior
    for day in days:
        nonAvailableEmployees = attendance_collection.find({"date": day}, {"_id": 0, "id_employee": 1}).distinct("id_employee")
        available_employees = [
            emp for emp in employees
            if not nonAvailableEmployees
        ]
        for _ in range(quantity):
            if not available_employees:
                counter -= 1
                break


            id_employee = random.choice(available_employees)
            available_employees.remove(id_employee) 

            start_time = fake.date_time_this_decade()
            end_time = fake.date_time_this_decade()

            if start_time > end_time:
                start_time, end_time = end_time, start_time


            attendance = {
                "id_employee": id_employee,
                "date": day,
                "sessions": [
                    {
                        "checkin": start_time.strftime("%H:%M:%S"),
                        "checkout": end_time.strftime("%H:%M:%S")
                    }
                ]
            }
            attendance_collection.insert_one(attendance)

            if counter % (total_records // 4) == 0:
                print(f"Progress: {((counter / total_records) * 100):.0f}% completed.")

    if counter == 0:  print("All employees already have records.") 
    print(f"{quantity*counter} registros inseridos na coleção 'attendance'. (Quantidade de dias: {counter})")

def delete(quantity=None):
    db = get_mongo_db()
    attendance_collection = db['attendance']
    result = attendance_collection.delete_many({})
    print(f"{result.deleted_count} registros deletados da coleção 'attendance'.")
