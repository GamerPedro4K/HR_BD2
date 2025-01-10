#
#! salary_history.py
#? python manage.py seed --seeder 13_salary_history

from django.db import connection
from faker import Faker
from datetime import date

""" 
CREATE TABLE IF NOT EXISTS salary_history (
    id_salary_history UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    id_contract UUID NOT NULL,
    id_employee_aproved_by UUID NOT NULL,
    base_salary NUMERIC(10, 2),
    extra_hour_rate NUMERIC(10, 2),
    start_date DATE,
    FOREIGN KEY (id_contract) REFERENCES contract(id_contract),
    FOREIGN KEY (id_employee_aproved_by) REFERENCES employees(id_employee),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP DEFAULT NULL
);
"""

def seed(quantity=100):
    fake = Faker()
    with connection.cursor() as cursor:
        cursor.execute(""" 
                        SELECT id_contract, id_employee
                        FROM contract
                        WHERE id_contract NOT IN (SELECT id_contract FROM salary_history
                                                    WHERE start_date = CURRENT_DATE)     
                        ORDER BY RANDOM();
                       """)
        contracts_and_employees = cursor.fetchall()


        cursor.execute("""
                        SELECT id_employee 
                        FROM employees
                        ORDER BY RANDOM();
                       """)
        all_employees = [row[0] for row in cursor.fetchall()]

        if not contracts_and_employees or not all_employees:
            print("No contracts or employees found. Please create contracts and employees before running the salary history seeder.")
            return

        quantity = min(quantity, len(contracts_and_employees))

        for _ in range(quantity):
            id_contract, id_employee = contracts_and_employees[_]  # Assign only id_contract
            possible_approvers = [emp for emp in all_employees if emp != id_employee]
            id_employee_aproved_by = fake.random_element(elements=possible_approvers)
            base_salary = fake.random_int(min=1000, max=10000)
            extra_hour_rate = fake.random_int(min=10, max=50)
            start_date = date.today()
            cursor.execute(
                """
                INSERT INTO salary_history (id_contract, id_employee_aproved_by, base_salary, extra_hour_rate, start_date)
                VALUES (%s, %s, %s, %s, %s);
                """,
                [id_contract, id_employee_aproved_by, base_salary, extra_hour_rate, start_date]
            )
            if (quantity >= 4) and ((_ + 1) % (quantity // 4) == 0):  # 25% checkpoints
                print(f"Progress: {((_ + 1) / quantity) * 100:.0f}% completed.")

def delete(quantity=None):
    with connection.cursor() as cursor:
        if quantity is not None and quantity > 0:
            cursor.execute(
                f"""
                DELETE FROM salary_history 
                WHERE id_salary_history IN (
                    SELECT id_salary_history FROM salary_history 
                    ORDER BY id_salary_history ASC 
                    LIMIT %s
                );
                """,
                [quantity]
            )
        else:
            cursor.execute("DELETE FROM salary_history;")