#
#! contract_state_contract.py
#? python manage.py seed --seeder 15_contract_state_contract

from django.db import connection
from faker import Faker

""" 
CREATE TABLE IF NOT EXISTS contract_state_contract (
    id_contract_state UUID NOT NULL,
    id_contract UUID NOT NULL,
    PRIMARY KEY (id_contract_state, id_contract),
    FOREIGN KEY (id_contract_state) REFERENCES contract_state(id_contract_state),
    FOREIGN KEY (id_contract) REFERENCES contract(id_contract),
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
                        WHERE id_contract NOT IN (SELECT id_contract FROM contract_state_contract)     
                        ORDER BY RANDOM();
                       """)
        contracts = [row[0] for row in cursor.fetchall()]
        
        cursor.execute("SELECT id_contract_state FROM contract_state ORDER BY RANDOM();")
        contract_states = [row[0] for row in cursor.fetchall()]

        if not contracts or not contract_states:
            print("No contracts or contract states found. Please create contracts and contract states before running the contract state contract seeder.")
            return
        
        quantity = min(quantity, len(contracts))

        for _ in range(quantity):
            id_contract = contracts[_]
            id_contract_state = fake.random_element(elements=contract_states)
            cursor.execute(
                """
                INSERT INTO contract_state_contract (id_contract_state, id_contract)
                VALUES (%s, %s);
                """,
                [id_contract_state, id_contract]
            )
            if (quantity >= 4) and ((_ + 1) % (quantity // 4) == 0):  # 25% checkpoints
                print(f"Progress: {((_ + 1) / quantity) * 100:.0f}% completed.")

def delete(quantity=None):
    with connection.cursor() as cursor:
        if quantity is not None and quantity > 0:
            cursor.execute(
                f"""
                DELETE FROM contract_state_contract
                WHERE id_contract IN (
                    SELECT id_contract
                    FROM contract
                    ORDER BY RANDOM()
                    LIMIT %s
                );
                """,
                [quantity]
            )
            print(f"{quantity} contract state contracts deleted.")
        else:
            cursor.execute("DELETE FROM contract_state_contract;")
            print("All contract state contracts deleted.")