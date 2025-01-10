#
#! vacations.py
#? python manage.py seed --seeder 19_vacations

from django.db import connection
from faker import Faker
import random
from datetime import timedelta, datetime

""" 
CREATE TABLE IF NOT EXISTS vacations (
    id_vacation UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    id_employee UUID NOT NULL,
    FOREIGN KEY (id_employee) REFERENCES employees(id_employee),
    aproved_date DATE NOT NULL,
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
                        ORDER BY RANDOM();
                       """)
        employees = [row[0] for row in cursor.fetchall()]
        
        if len(employees) < 2:
            print("No employees found. Please create at least two employees before running the vacations seeder.")
            return
        
        quantity = min(quantity, len(employees) // 2)
        
        for _ in range(quantity):
            if random.random() <= 0.75:
                continue
            id_employee = employees[_]
            aproved_date = fake.date_this_year()

            # Define um período de um ano a partir de `aproved_date`
            one_year_later = aproved_date + timedelta(days=365)
            start_date = fake.date_between_dates(date_start=aproved_date, date_end=one_year_later)
            end_date = fake.date_between_dates(date_start=start_date, date_end=start_date + timedelta(days=365))
            
            cursor.execute(
                """
                INSERT INTO vacations (id_employee, aproved_date, start_date, end_date)
                VALUES (%s, %s, %s, %s);
                """,
                [id_employee, aproved_date, start_date, end_date]
            )
            if (quantity >= 4) and ((_ + 1) % (quantity // 4) == 0):  # 25% checkpoints
                print(f"Progress: {((_ + 1) / quantity) * 100:.0f}% completed.")


def delete(quantity=None):
    with connection.cursor() as cursor:
        if quantity is not None and quantity > 0:
            cursor.execute(
                f"""
                DELETE FROM vacations
                WHERE id_vacation IN (
                    SELECT id_vacation
                    FROM vacations
                    ORDER BY RANDOM()
                    LIMIT {quantity}
                );
                """
            )
        else:
            cursor.execute("DELETE FROM vacations;")