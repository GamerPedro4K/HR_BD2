#
#! certifications.py
#? python manage.py seed --seeder 21_certifications

import random
from django.db import connection
from faker import Faker
from datetime import timedelta

""" 
CREATE TABLE IF NOT EXISTS certifications (
    id_certification UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    id_employee UUID NOT NULL,
    id_certificate_type UUID NOT NULL,
    FOREIGN KEY (id_employee) REFERENCES employees(id_employee),
    FOREIGN KEY (id_certificate_type) REFERENCES certificate_types(id_certificate_type),
    issuing_organization VARCHAR(50) NOT NULL,
    issue_date DATE NOT NULL,
    expiration_date DATE,
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
        
        cursor.execute("SELECT id_certificate_type FROM certificate_types ORDER BY RANDOM();")
        certificate_types = [row[0] for row in cursor.fetchall()]

        if not employees or not certificate_types:
            print("No employees or certificate types found. Please create employees and certificate types before running the certifications seeder.")
            return
        
        quantity = min(quantity, len(employees))
        
        for _ in range(quantity):
            if random.random() < 0.65:
                for _ in range(random.randint(1, 2)):
                    if _ == 2 and random.random() < 0.5:
                        break
                    id_employee = employees[_]
                    id_certificate_type = fake.random_element(elements=certificate_types)
                    issuing_organization = fake.company()
                    issue_date = fake.date_this_year()
                    expiration_date = None
                    if fake.boolean(chance_of_getting_true=75):
                        max_date = issue_date + timedelta(days=3 * 365)
                        expiration_date = fake.date_between(start_date=issue_date, end_date=max_date)
                    cursor.execute(
                        """
                        INSERT INTO certifications (id_employee, id_certificate_type, issuing_organization, issue_date, expiration_date)
                        VALUES (%s, %s, %s, %s, %s);
                        """,
                        [id_employee, id_certificate_type, issuing_organization, issue_date, expiration_date]
                    )
            if (quantity >= 4) and ((_ + 1) % (quantity // 4) == 0):  # 25% checkpoints
                print(f"Progress: {((_ + 1) / quantity) * 100:.0f}% completed.")

def delete(quantity=None):
    with connection.cursor() as cursor:
        if quantity is not None and quantity > 0:
            cursor.execute(
                f"""
                DELETE FROM certifications 
                WHERE id_certification IN (
                    SELECT id_certification 
                    FROM certifications 
                    ORDER BY RANDOM() 
                    LIMIT %s
                );
                """,
                [quantity]
            )
        else:
            cursor.execute("DELETE FROM certifications;")