#
#! contract_leave_type.py
#? python manage.py seed --seeder 17_contract_leave_type

from django.db import connection

""" 
CREATE TABLE IF NOT EXISTS contract_leave_type (
    id_leave_type UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    leave_type VARCHAR(100),
    description TEXT,
    is_paid BOOLEAN,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP DEFAULT NULL
);
"""

def seed(quantity=None):
    leave_types_data = [
        ("Holiday", "Férias pagas anuais para os funcionários", True),
        ("Holiday_Current", "Saldo atual de férias do funcionário", True),
        ("Sick Leave", "Licença médica paga para funcionários doentes", True),
        ("Sick Leave_Current", "Saldo atual de licença médica", True),
        ("Sick_Leave_Medical_Cert", "Licença médica com atestado", True),
        ("Sick Leave_Medical_Cert_Current", "Saldo atual de licença médica com atestado", True),
        ("Authorized_Unpaid_Leave", "Licença não remunerada autorizada", False),
        ("Authorized_Unpaid_Leave_Current", "Saldo atual de licença não remunerada autorizada", False),
        ("Unauthorized_Unpaid_Leave", "Licença não remunerada não autorizada", False),
        ("Unauthorized_Unpaid_Leave_Current", "Saldo atual de licença não remunerada não autorizada", False),
        ("Compassionate_Leave", "Licença por luto ou emergências familiares", True),
        ("Compassionate_Leave_Current", "Saldo atual de licença por luto ou emergências", True)
    ]

    with connection.cursor() as cursor:
        # Verifica se já existem registros na tabela
        cursor.execute("SELECT id_leave_type FROM contract_leave_type ORDER BY RANDOM();")
        existing_leave_types = [row[0] for row in cursor.fetchall()]

        if not existing_leave_types:
            for leave_type, description, is_paid in leave_types_data:
                cursor.execute(
                    """
                    INSERT INTO contract_leave_type (leave_type, description, is_paid)
                    VALUES (%s, %s, %s);
                    """,
                    [leave_type, description, is_paid]
                )
            print(f"{len(leave_types_data)} leave types seeded successfully.")
        else:
            print("Leave types already seeded.")

def delete(quantity=None):
    with connection.cursor() as cursor:
        if quantity is not None and quantity > 0:
            cursor.execute(
                f"""
                DELETE FROM contract_leave_type 
                WHERE id_leave_type IN (
                    SELECT id_leave_type FROM contract_leave_type 
                    ORDER BY id_leave_type ASC 
                    LIMIT %s
                );
                """,
                [quantity]
            )
        else:
            cursor.execute("DELETE FROM contract_leave_type;")