#
#! trainings.py
#? python manage.py seed --seeder 23_trainings

import random
from django.db import connection
from faker import Faker
from datetime import timedelta

""" 
CREATE TABLE IF NOT EXISTS trainings (
    id_training UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    id_employee UUID NOT NULL,
    id_training_type UUID NOT NULL,
    FOREIGN KEY (id_employee) REFERENCES employees(id_employee),
    FOREIGN KEY (id_employee_instructor) REFERENCES employees(id_employee),
    FOREIGN KEY (id_training_type) REFERENCES training_types(id_training_type),
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP DEFAULT NULL
);
"""

def seed(quantity=100):
    fake = Faker()
    with connection.cursor() as cursor:
        cursor.execute("""
                SELECT id_employee 
                FROM employees
                WHERE id_employee NOT IN (SELECT id_employee FROM trainings)
                ORDER BY RANDOM();
               """)
        employees = [row[0] for row in cursor.fetchall()]

        cursor.execute("SELECT id_training_type FROM training_types ORDER BY RANDOM();")

        training_types = [row[0] for row in cursor.fetchall()]
        
        if not employees:
            print("No employees found. Please create employees before running the trainings seeder.")
            return
        
        quantity = min(quantity, len(employees))
        
        for _ in range(quantity):
            if random.random() < 0.60:
                id_employee = employees[_]
                id_training_type = fake.random_element(elements=training_types)
                start_date = fake.date_this_year()
                end_date = start_date + timedelta(days=random.randint(1, 365))
        
                cursor.execute(
                    """
                    INSERT INTO trainings (id_employee, id_training_type, start_date, end_date)
                    VALUES (%s, %s, %s, %s);
                    """,
                    (id_employee, id_training_type, start_date, end_date)
                )
            if (quantity >= 4) and ((_ + 1) % (quantity // 4) == 0):  # 25% checkpoints
                print(f"Progress: {((_ + 1) / quantity) * 100:.0f}% completed.")
    

def delete(quantity=None):
    with connection.cursor() as cursor:
        if quantity is not None and quantity > 0:
           cursor.execute(f"DELETE FROM trainings WHERE id_training IN (SELECT id_training FROM trainings ORDER BY RANDOM() LIMIT {quantity});")
        else:
            cursor.execute("DELETE FROM trainings;")

