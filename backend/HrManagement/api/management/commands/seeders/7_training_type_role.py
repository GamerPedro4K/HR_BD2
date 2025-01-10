#
#! training_type_role.py
#? python manage.py seed --seeder 6_training_type_role

from django.db import connection
from faker import Faker

""" 
CREATE TABLE IF NOT EXISTS training_type_role (
    id_training_type UUID NOT NULL,
    id_role UUID NOT NULL,
    PRIMARY KEY (id_training_type, id_role),
    FOREIGN KEY (id_training_type) REFERENCES training_types(id_training_type),
    FOREIGN KEY (id_role) REFERENCES roles(id_role),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP DEFAULT NULL
);
 """

def seed(quantity=100):
    fake = Faker()
    with connection.cursor() as cursor:
        cursor.execute("SELECT id_training_type FROM training_types ORDER BY RANDOM();")
        training_types = [row[0] for row in cursor.fetchall()]
        cursor.execute("SELECT id_role FROM roles ORDER BY RANDOM();")
        roles = [row[0] for row in cursor.fetchall()]

        if not training_types or not roles:
            print("No training types or roles found. Please create training types and roles before running the training_type_role seeder.")
            return
    
        existing_records = set()

        # Correção: recupere na ordem correta (id_training_type, id_role)
        cursor.execute("SELECT id_training_type, id_role FROM training_type_role;")
        for row in cursor.fetchall():
            existing_records.add((row[0], row[1]))
        
        for _ in range(quantity):
            id_training_type = fake.random_element(elements=training_types)
            id_role = fake.random_element(elements=roles)
            
            key = (id_training_type, id_role)
            
            # Verifique a existência da chave antes de inserir
            if key not in existing_records:
                cursor.execute(
                    """
                    INSERT INTO training_type_role (id_training_type, id_role)
                    VALUES (%s, %s);
                    """,
                    [id_training_type, id_role]
                )
                existing_records.add(key)  
            
            if (quantity >= 4) and ((_ + 1) % (quantity // 4) == 0):  # Checkpoints de 25%
                print(f"Progress: {((_ + 1) / quantity) * 100:.0f}% completed.")


def delete(quantity=None):
    with connection.cursor() as cursor:
        if quantity is not None and quantity > 0:
            cursor.execute(
                f"""
                DELETE FROM training_type_role 
                WHERE (id_training_type, id_role) IN (
                    SELECT id_training_type, id_role FROM training_type_role 
                    ORDER BY id_training_type, id_role ASC 
                    LIMIT %s
                );
                """,
                [quantity]
            )
            print(f"{quantity} records deleted from training_type_role.")
        else:
            cursor.execute("DELETE FROM training_type_role;")
            print("All records deleted from training_type_role.")