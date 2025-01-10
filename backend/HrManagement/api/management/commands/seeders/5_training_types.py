#
#! training_types.py
#? python manage.py seed --seeder 5_training_types
# This file is used to seed the training_types table with fake data.

from django.db import connection
from faker import Faker

""" 
CREATE TABLE IF NOT EXISTS training_types (
    id_training_type UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(50) NOT NULL,
    description TEXT NOT NULL,
    hours INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP DEFAULT NULL
);
 """

def seed(quantity=100):
    fake = Faker()
    with connection.cursor() as cursor:
        for _ in range(quantity):  
            name = fake.word()
            description = fake.sentence()
            hours = fake.random_int(min=1, max=100)
            cursor.execute(
                """
                INSERT INTO training_types (name, description, hours)
                VALUES (%s, %s, %s);
                """,
                [name, description, hours]
            )
            if (quantity >= 4) and ((_ + 1) % (quantity // 4) == 0):  # 25% checkpoints
                print(f"Progress: {((_ + 1) / quantity) * 100:.0f}% completed.")

def delete(quantity=None):
    with connection.cursor() as cursor:
        if quantity is not None and quantity > 0:
            cursor.execute(
                f"""
                DELETE FROM training_types 
                WHERE id_training_type IN (
                    SELECT id_training_type FROM training_types 
                    ORDER BY id_training_type ASC 
                    LIMIT %s
                );
                """,
                [quantity]
            )
            print(f"{quantity} records deleted from training_types.")
        else:
            cursor.execute("DELETE FROM training_types;")
            print("All records deleted from training_types.")