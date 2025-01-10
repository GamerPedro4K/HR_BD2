#
#! payment_methods.py
#? python manage py seed --seeder 25_payment_methods

import random
from django.db import connection
from faker import Faker

""" 
CREATE TABLE IF NOT EXISTS payment_methods (
    id_payment_method UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(50) NOT NULL,
    description TEXT NOT NULL,
    icon VARCHAR(100) NOT NULL,
    hex_color VARCHAR(6) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP DEFAULT NULL
);
"""

def seed(quantity=5):
    fake = Faker()
    with connection.cursor() as cursor:
        cursor.execute("SELECT id_payment_method FROM payment_methods ORDER BY RANDOM();")
        payment_methods = [row[0] for row in cursor.fetchall()]

        if not payment_methods:
            for _ in range(quantity):
                name = fake.word()
                description = fake.text()
                icon = fake.word()
                hex_color = fake.hex_color()
                cursor.execute(
                    """
                    INSERT INTO payment_methods (name, description, icon, hex_color)
                    VALUES (%s, %s, %s, %s);
                    """,
                    [name, description, icon, hex_color]
                )
                if (quantity >= 4) and ((_ + 1) % (quantity // 4) == 0):  # 25% checkpoints
                    print(f"Progress: {((_ + 1) / quantity) * 100:.0f}% completed.")
        else:
            print("Payment methods already seeded.")

def delete(quantity=None):
    with connection.cursor() as cursor:
        if quantity is not None and quantity > 0:
            cursor.execute(
                f"""
                DELETE FROM payment_methods 
                WHERE id_payment_method IN (
                    SELECT id_payment_method FROM payment_methods 
                    ORDER BY id_payment_method ASC 
                    LIMIT %s
                );
                """,
                [quantity]
            )
        else:
            cursor.execute("DELETE FROM payment_methods;")
        print("Deleted all payment methods.")

