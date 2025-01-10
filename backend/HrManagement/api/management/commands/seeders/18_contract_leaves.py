#
#! contract_leaves.py
#? python manage.py seed --seeder 18_contract_leaves

from django.db import connection
from faker import Faker
import random

"""
CREATE TABLE IF NOT EXISTS contract_leaves (
    id_contract_leave UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    id_contract UUID NOT NULL,
    id_leave_type UUID NOT NULL,
    hours NUMERIC(10, 2),
    hours_taken NUMERIC(10, 2),
    FOREIGN KEY (id_contract) REFERENCES contract(id_contract),
    FOREIGN KEY (id_leave_type) REFERENCES contract_leave_type(id_leave_type),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP DEFAULT NULL
);
"""

def seed(quantity=100):
    fake = Faker()
    with connection.cursor() as cursor:
        cursor.execute("""
                        SELECT id_contract 
                        FROM contract
                        WHERE id_contract NOT IN (SELECT id_contract FROM contract_leaves)     
                        ORDER BY RANDOM();
                       """)
        contracts = [row[0] for row in cursor.fetchall()]
        
        cursor.execute("SELECT id_leave_type FROM contract_leave_type ORDER BY RANDOM();")
        leave_types = [row[0] for row in cursor.fetchall()]

        if not contracts or not leave_types:
            print("No contracts or leave types found. Please create contracts and leave types before running the contract leaves seeder.")
            return
        
        quantity = min(quantity, len(contracts))

        for _ in range(quantity):
            if random.random() <= 0.75:
                continue
            id_contract = contracts[_]
            id_leave_type = fake.random_element(elements=leave_types)
            hours = fake.random_int(min=10, max=100)
            hours_taken = fake.random_int(min=0, max=hours)
            cursor.execute(
                """
                INSERT INTO contract_leaves (id_contract, id_leave_type, hours, hours_taken)
                VALUES (%s, %s, %s, %s);
                """,
                [id_contract, id_leave_type, hours, hours_taken]
            )
            if (quantity >= 4) and ((_ + 1) % (quantity // 4) == 0):  # 25% checkpoints
                print(f"Progress: {((_ + 1) / quantity) * 100:.0f}% completed.")
    
def delete(quantity=None):
    with connection.cursor() as cursor:
        if quantity is not None and quantity > 0:
            cursor.execute(
                f"""
                DELETE FROM contract_leaves
                WHERE id_contract IN (
                    SELECT id_contract
                    FROM contract
                    WHERE deleted_at IS NULL
                    ORDER BY RANDOM()
                    LIMIT %s
                );
                """,
                [quantity]
            )
            print(f"{quantity} contract leaves deleted.")
        else:
            cursor.execute("DELETE FROM contract_leaves;")
            print("All contract leaves deleted.")