import random
from faker import Faker
from api.utils.mongo_client import get_mongo_db
from datetime import datetime, timedelta
from django.db import connection

"""
Seeder para popular a coleção no MongoDB: extra hours.
"""

def seed(quantity=100):
    fake = Faker()
    db = get_mongo_db()
    extrahours_collection = db['extrahours']
    quantity_days_prior = 3  # Quantidade de dias anteriores

    with connection.cursor() as cursor:
        cursor.execute("SELECT id_employee FROM employees;")
        employees = [str(row[0]) for row in cursor.fetchall()]
        if not employees:
            print("No employees found. Please create employees before running the extra hours seeder.")
            return

    quantity = min(quantity, len(employees))

    # Criar lista com os últimos três dias
    days = [(datetime.now() - timedelta(days=i)).date().isoformat() for i in range(quantity_days_prior)]

    counter = quantity_days_prior
    total_records = quantity * quantity_days_prior
    for day in days:
        nonAvailableEmployees = extrahours_collection.find({"date": day}, {"_id": 0, "id_employee": 1}).distinct("id_employee")
        available_employees = [
            emp for emp in employees
            if emp not in nonAvailableEmployees
        ]
        for _ in range(quantity):
            if not available_employees:
                counter -= 1
                break

            id_employee = random.choice(available_employees)
            available_employees.remove(id_employee)

            # Criar horários aleatórios, garantindo que "end" seja sempre maior que "start"
            start_time = fake.date_time_this_decade()
            end_time = fake.date_time_this_decade()

            if start_time > end_time:
                start_time, end_time = end_time, start_time

            extrahour = {
                "id_employee": id_employee,
                "date": day,
                "start": start_time.strftime("%H:%M:%S"),
                "end": end_time.strftime("%H:%M:%S"),
            }
            extrahours_collection.insert_one(extrahour)

            if counter % (total_records // 4) == 0:
                print(f"Progress: {((counter / total_records) * 100):.0f}% completed.")

    print(f"{quantity*counter} registros inseridos na coleção 'attendance'. (Quantidade de dias: {counter})")


def delete():
    db = get_mongo_db()
    extrahours_collection = db['extrahours']
    result = extrahours_collection.delete_many({})
    print(f"{result.deleted_count} registros deletados da coleção 'extrahours'.")
