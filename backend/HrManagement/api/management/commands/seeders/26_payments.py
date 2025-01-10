#
#! payments.py
#? python manage.py seed --seeder 26_payments

import random
from django.db import connection
from faker import Faker

""" 
CREATE TABLE IF NOT EXISTS payments (
    id_payment UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    id_employee UUID NOT NULL,
    id_employee_supervisor UUID NOT NULL,
    id_payment_method UUID NOT NULL,
    FOREIGN KEY (id_employee) REFERENCES employees(id_employee),
    FOREIGN KEY (id_employee_supervisor) REFERENCES employees(id_employee),
    FOREIGN KEY (id_payment_method) REFERENCES payment_methods(id_payment_method),
    amount DECIMAL(10,2) NOT NULL,
    payment_date DATE NOT NULL,
    extra_amount DECIMAL(10,2),
    deduction_amount DECIMAL(10,2),
    bonus_amount DECIMAL(10,2),
    payment_note TEXT,
    src VARCHAR(200),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP DEFAULT NULL
);
"""

def seed(quantity=100):
    fake = Faker()
    with connection.cursor() as cursor:
        # Buscar os funcionários elegíveis
        cursor.execute("""
            SELECT id_employee 
            FROM employees
            WHERE id_employee NOT IN (
                SELECT DISTINCT id_employee FROM payments
            )
            ORDER BY RANDOM();
        """)
        employees = [row[0] for row in cursor.fetchall()]

        # Buscar os métodos de pagamento disponíveis
        cursor.execute("SELECT id_payment_method FROM payment_methods ORDER BY RANDOM();")
        payment_methods = [row[0] for row in cursor.fetchall()]

        if not employees:
            print("No employees found. Please create employees before running the payments seeder.")
            return

        quantity = min(quantity, len(employees))

        for _ in range(quantity):
            id_employee = employees[_]
            id_employee_supervisor = fake.random_element(elements=employees)
            id_payment_method = fake.random_element(elements=payment_methods)
            extra_amount = fake.random_int(min=100, max=1000) if fake.boolean(chance_of_getting_true=75) else 0
            deduction_amount = fake.random_int(min=100, max=1000) if fake.boolean(chance_of_getting_true=75) else 0
            bonus_amount = fake.random_int(min=100, max=1000) if fake.boolean(chance_of_getting_true=75) else 0

            amount = (extra_amount or 0) + (bonus_amount or 0) - (deduction_amount or 0)
            amount = max(0, amount) 

            payment_date = fake.date_this_year()
            payment_note = fake.text() if fake.boolean(chance_of_getting_true=75) else None
            src = "https://images.pexels.com/photos/261679/pexels-photo-261679.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1"

            cursor.execute(
                """
                INSERT INTO payments (
                    id_employee, id_employee_supervisor, id_payment_method, 
                    amount, payment_date, extra_amount, deduction_amount, 
                    bonus_amount, payment_note, src
                )
                VALUES (%s, %s, %s, COALESCE(%s, 0), %s, %s, %s, %s, %s, %s);
                """,
                (id_employee, id_employee_supervisor, id_payment_method, amount, payment_date, extra_amount, deduction_amount, bonus_amount, payment_note, src)
            )

            # Checkpoints de progresso (25%)
            if (quantity >= 4) and ((_ + 1) % (quantity // 4) == 0):
                print(f"Progress: {((_ + 1) / quantity) * 100:.0f}% completed.")

def delete(quantity=None):
    with connection.cursor() as cursor:
        if quantity is not None and quantity > 0:
            cursor.execute(
                f"""
                DELETE FROM payments 
                WHERE id_payment IN (
                    SELECT id_payment 
                    FROM payments 
                    WHERE deleted_at IS NULL
                    ORDER BY RANDOM()
                    LIMIT {quantity}
                );
                """
            )
        else:
            cursor.execute("DELETE FROM payments WHERE deleted_at IS NULL;")
