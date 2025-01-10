#
#! contract.py
#? python manage.py seed --seeder 10_contract

from django.db import connection
from faker import Faker

""" 
CREATE TABLE IF NOT EXISTS contract (
    id_contract UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    id_employee UUID NOT NULL,
    id_role UUID NOT NULL,
    id_contract_type UUID NOT NULL,
    FOREIGN KEY (id_role) REFERENCES roles(id_role),
    FOREIGN KEY (id_employee) REFERENCES employees(id_employee),
    FOREIGN KEY (id_contract_type) REFERENCES contract_type(id_contract_type),
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
                        WHERE id_employee NOT IN (SELECT id_employee FROM contract)     
                        ORDER BY RANDOM();
                       """)
        employees = [row[0] for row in cursor.fetchall()]
        
        cursor.execute("SELECT id_contract_type FROM contract_type ORDER BY RANDOM();")
        contract_types = [row[0] for row in cursor.fetchall()]

        cursor.execute("SELECT id_role FROM roles ORDER BY RANDOM();")
        roles = [row[0] for row in cursor.fetchall()]

        if not employees or not contract_types:
            print("No employees or contract types found. Please create employees and contract types before running the contract seeder.")
            return
        
        if not roles:
            print("No roles found. Please ensure there are roles in the database.")
            return
        
        quantity = min(quantity, len(employees))

        for _ in range(quantity):
            id_employee = employees[_]
            id_contract_type = fake.random_element(elements=contract_types)
            id_role = fake.random_element(elements=roles)
            cursor.execute(
                """
                INSERT INTO contract (id_employee, id_contract_type, id_role)
                VALUES (%s, %s, %s);
                """,
                [id_employee, id_contract_type, id_role]
            )
            if (quantity >= 4) and ((_ + 1) % (quantity // 4) == 0):  # 25% checkpoints
                print(f"Progress: {((_ + 1) / quantity) * 100:.0f}% completed.")

def delete(quantity=None):
    with connection.cursor() as cursor:
        if quantity is not None and quantity > 0:
            cursor.execute(
                f"""
                DELETE FROM contract 
                WHERE id_contract IN (
                    SELECT id_contract FROM contract 
                    ORDER BY id_contract ASC 
                    LIMIT %s
                );
                """,
                [quantity]
            )
        else:
            cursor.execute("DELETE FROM contract;")