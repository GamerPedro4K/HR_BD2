#
#! employee_location.py
#? python manage.py seed --seeder 8_employee_location

from django.db import connection
from faker import Faker

""" 
CREATE TABLE IF NOT EXISTS employee_location (
    id_location UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    id_employee UUID NOT NULL DISTINCT,
    address VARCHAR(200),
    city VARCHAR(100),
    district VARCHAR(20),
    country VARCHAR(2),
    zip_code VARCHAR(8),
    FOREIGN KEY (id_employee) REFERENCES employees(id_employee),
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
                        WHERE id_employee NOT IN (SELECT id_employee FROM employee_location)     
                        ORDER BY RANDOM();
                       """)
        employees = [row[0] for row in cursor.fetchall()]

        if not employees:
            print("No employees found. Please create employees before running the employee_location seeder.")
            return
        
        quantity = min(quantity, len(employees))

        for _ in range(quantity):
            id_employee = employees[_]
            address = fake.street_address()
            city = fake.city()
            district = fake.state_abbr()
            country = fake.country_code(representation="alpha-2")
            zip_code = fake.zipcode()
            cursor.execute(
                """
                INSERT INTO employee_location (id_employee, address, city, district, country, zip_code)
                VALUES (%s, %s, %s, %s, %s, %s);
                """,
                [id_employee, address, city, district, country, zip_code]
            )
            if (quantity >= 4) and ((_ + 1) % (quantity // 4) == 0):  # 25% checkpoints
                print(f"Progress: {((_ + 1) / quantity) * 100:.0f}% completed.")
        
def delete(quantity=None):
    with connection.cursor() as cursor:
        if quantity is not None and quantity > 0:
            cursor.execute(
                f"""
                DELETE FROM employee_location 
                WHERE id_location IN (
                    SELECT id_location FROM employee_location 
                    ORDER BY id_location ASC 
                    LIMIT %s
                );
                """,
                [quantity]
            )
            print(f"{quantity} records deleted from employee_location.")
        else:
            cursor.execute("DELETE FROM employee_location;")