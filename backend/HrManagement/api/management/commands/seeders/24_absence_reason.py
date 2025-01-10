#
#! absence_reason.py
#? python manage.py seed --seeder 24_absence_reason

import random
from django.db import connection
from faker import Faker
from datetime import timedelta

""" 
CREATE TABLE IF NOT EXISTS absence_reason (
    id_absence_reason UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    id_employee UUID NOT NULL,
    id_employee_supervisor UUID NOT NULL,
    id_employee_substitute UUID NOT NULL,
    FOREIGN KEY (id_employee) REFERENCES employees(id_employee),
    FOREIGN KEY (id_employee_supervisor) REFERENCES employees(id_employee),
    FOREIGN KEY (id_employee_substitute) REFERENCES employees(id_employee),
    name VARCHAR(50) NOT NULL,
    description TEXT NOT NULL,
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
                WHERE id_employee IN (
                        SELECT id_employee 
                        FROM employees 
                        WHERE id_employee NOT IN 
                            (SELECT id_employee FROM absence_reason)
                        AND id_employee NOT IN
                            (SELECT id_employee_supervisor FROM absence_reason)
                        AND id_employee NOT IN
                            (SELECT id_employee_substitute FROM absence_reason)
                          ORDER BY RANDOM())
                ORDER BY RANDOM();
               """)
        employees = [row[0] for row in cursor.fetchall()]

        if not employees:
            print("No employees found. Please create employees before running the absence_reason seeder.")
            return
        
        quantity = min(quantity, len(employees))
        
        for _ in range(quantity):
            if random.random() < 0.14:
                id_employee = employees[_]
                id_employee_supervisor = fake.random_element(elements=employees)
                id_employee_substitute = fake.random_element(elements=employees)
                name = fake.word()
                description = fake.text()
                start_date = fake.date_this_year()
                end_date = fake.date_between_dates(date_start=start_date, date_end=start_date + timedelta(days=365 * 3))
                
                cursor.execute(
                    """
                    INSERT INTO absence_reason (id_employee, id_employee_supervisor, id_employee_substitute, name, description, start_date, end_date)
                    VALUES (%s, %s, %s, %s, %s, %s, %s);
                    """,
                    (id_employee, id_employee_supervisor, id_employee_substitute, name, description, start_date, end_date)
                )
            if (quantity >= 4) and ((_ + 1) % (quantity // 4) == 0):  # 25% checkpoints
                print(f"Progress: {((_ + 1) / quantity) * 100:.0f}% completed.")
    

def delete(quantity=None):
    with connection.cursor() as cursor:
        if quantity is not None and quantity > 0:
            cursor.execute(
                f"""
                DELETE FROM absence_reason 
                WHERE id_absence_reason IN (
                    SELECT id_absence_reason 
                    FROM absence_reason 
                    ORDER BY RANDOM() 
                    LIMIT {quantity}
                );
                """
            )
        else:
            cursor.execute("DELETE FROM absence_reason;")