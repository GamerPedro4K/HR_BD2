#
#! contract_benefits.py
#? python manage.py seed --seeder 12_contract_benefits

from django.db import connection
from faker import Faker

"""
CREATE TABLE IF NOT EXISTS contract_benefits (
    id_contract_benefit UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    id_contract UUID NOT NULL,
    id_type_benefit UUID NOT NULL,
    benefit_amount NUMERIC(10, 2),
    FOREIGN KEY (id_contract) REFERENCES contract(id_contract),
    FOREIGN KEY (id_type_benefit) REFERENCES type_benefit(id_type_benefit),
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
                        WHERE id_contract NOT IN (SELECT id_contract FROM contract_benefits)     
                        ORDER BY RANDOM();
                       """)
        contracts = [row[0] for row in cursor.fetchall()]
        
        cursor.execute("SELECT id_type_benefit FROM type_benefit ORDER BY RANDOM();")
        type_benefits = [row[0] for row in cursor.fetchall()]

        if not contracts or not type_benefits:
            print("No contracts or type benefits found. Please create contracts and type benefits before running the contract benefits seeder.")
            return
        
        quantity = min(quantity, len(contracts))

        for _ in range(quantity):
            id_contract = contracts[_]
            id_type_benefit = fake.random_element(elements=type_benefits)
            benefit_amount = fake.random_int(min=100, max=500)
            cursor.execute(
                """
                INSERT INTO contract_benefits (id_contract, id_type_benefit, benefit_amount)
                VALUES (%s, %s, %s);
                """,
                [id_contract, id_type_benefit, benefit_amount]
            )
            if (quantity >= 4) and ((_ + 1) % (quantity // 4) == 0):  # 25% checkpoints
                print(f"Progress: {((_ + 1) / quantity) * 100:.0f}% completed.")

def delete(quantity=None):
    with connection.cursor() as cursor:
        if quantity is not None and quantity > 0:
            cursor.execute(
                f"""
                DELETE FROM contract_benefits 
                WHERE id_contract_benefit IN (
                    SELECT id_contract_benefit FROM contract_benefits 
                    ORDER BY id_contract_benefit ASC 
                    LIMIT %s
                );
                """,
                [quantity]
            )
        else:
            cursor.execute("DELETE FROM contract_benefits;")
