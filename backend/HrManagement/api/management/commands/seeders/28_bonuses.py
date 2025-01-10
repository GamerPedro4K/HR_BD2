#
#! bonuses.py
#? python manage.py seed --seeder 28_bonuses

import random
from django.db import connection
from faker import Faker

""" 
CREATE TABLE IF NOT EXISTS bonuses (
    id_bonus UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    id_payment UUID,
    id_employee UUID NOT NULL,
    FOREIGN KEY (id_employee) REFERENCES employees(id_employee),
    FOREIGN KEY (id_payment) REFERENCES payments(id_payment),
    bonus_note TEXT,
    amount DECIMAL(10,2) NOT NULL,
    bonus_date DATE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP DEFAULT NULL
);
"""

def seed(quantity=100):
    fake = Faker()
    with connection.cursor() as cursor:
        # Selecionar pagamentos que ainda não têm bônus associados
        cursor.execute("""
            SELECT p.id_payment, p.id_employee, p.bonus_amount, p.payment_date
            FROM payments p
            WHERE p.id_payment NOT IN (
                SELECT b.id_payment FROM bonuses b
            )
            ORDER BY RANDOM();
        """)
        payments = cursor.fetchall()

        if not payments:
            print("No payments found. Please create payments before running the bonuses seeder.")
            return

        quantity = min(quantity, len(payments))

        for i in range(quantity):
            id_payment, id_employee, bonus_amount, bonus_date = payments[i]
            bonus_note = fake.text(max_nb_chars=100)

            # Inserir bônus na tabela
            cursor.execute(
                """
                INSERT INTO bonuses (id_payment, id_employee, bonus_note, amount, bonus_date)
                VALUES (%s, %s, %s, %s, %s);
                """, [id_payment, id_employee, bonus_note, bonus_amount, bonus_date]
            )

            # Checkpoints de progresso (25%)
            if (quantity >= 4) and ((i + 1) % (quantity // 4) == 0):
                print(f"Progress: {((i + 1) / quantity) * 100:.0f}% completed.")

def delete(quantity=None):
    with connection.cursor() as cursor:
        if quantity is None:
            cursor.execute("DELETE FROM bonuses;")
        else:
            cursor.execute("DELETE FROM bonuses ORDER BY RANDOM() LIMIT %s;", [quantity])
