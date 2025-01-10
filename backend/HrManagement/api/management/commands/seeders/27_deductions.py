#
#! deductions.py
#? python manage.py seed --seeder 27_deductions

import random
from django.db import connection
from faker import Faker

""" 
CREATE TABLE IF NOT EXISTS deductions (
    id_deduction UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    id_payment UUID NOT NULL,
    id_absence_reason UUID NOT NULL,
    FOREIGN KEY (id_payment) REFERENCES payments(id_payment),
    FOREIGN KEY (id_absence_reason) REFERENCES absence_reason(id_absence_reason),
    deduction_note TEXT,
    amount DECIMAL(10,2) NOT NULL,
    deduction_date DATE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP DEFAULT NULL
);
"""

def seed(quantity=100):
    fake = Faker()
    with connection.cursor() as cursor:
        # Fetch payments with necessary columns
        cursor.execute("""
            SELECT id_payment, payment_date, COALESCE(deduction_amount, 0) AS deduction_amount
            FROM payments
            WHERE id_payment NOT IN (SELECT id_payment FROM deductions)
            ORDER BY RANDOM();
        """)
        payments = cursor.fetchall()  # Fetch all rows as tuples

        # Fetch absence reasons
        cursor.execute("SELECT id_absence_reason FROM absence_reason ORDER BY RANDOM();")
        absence_reasons = [row[0] for row in cursor.fetchall()]

        if not payments:
            print("No payments found. Please create payments before running the deductions seeder.")
            return

        if not absence_reasons:
            print("No absence reasons found. Please create absence reasons before running the deductions seeder.")
            return

        quantity = min(quantity, len(payments))

        for idx in range(quantity):
            id_payment, deduction_date, deduction_amount = payments[idx]
            id_absence_reason = fake.random_element(elements=absence_reasons)
            deduction_note = fake.text()
            
            # Ensure deduction_amount is valid
            if deduction_amount <= 0:
                deduction_amount = fake.random_int(min=50, max=500)

            cursor.execute(
                """
                INSERT INTO deductions (id_payment, id_absence_reason, deduction_note, amount, deduction_date)
                VALUES (%s, %s, %s, %s, %s);
                """,
                [id_payment, id_absence_reason, deduction_note, deduction_amount, deduction_date]
            )

            # Print progress at 20% intervals
            if quantity >= 5 and (idx + 1) % (quantity // 5) == 0:
                print(f"Progress: {((idx + 1) / quantity) * 100:.0f}% completed.")

        print("Progress: 100% completed.")


def delete(quantity=None):
    with connection.cursor() as cursor:
        if quantity is not None:
            cursor.execute(f"DELETE FROM deductions ORDER BY RANDOM() LIMIT {quantity};")
        else:
            cursor.execute("DELETE FROM deductions;")
