#
#! contract_state.py
#? python manage.py seed --seeder 14_contract_state

from django.db import connection
from faker import Faker

""" 
CREATE TABLE IF NOT EXISTS contract_state (
    id_contract_state UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    icon VARCHAR(100) NOT NULL,
    hex_color VARCHAR(6) NOT NULL,
    state VARCHAR(100) NOT NULL,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP DEFAULT NULL
);
"""

#with colors and icons

def seed(quantity=None):
    contract_states = [
    ("Active", "O contrato está em vigor e vigente.", "fas fa-check-circle", "#6CC24A"),  # Soft Green
    ("Pending", "O contrato está aguardando aprovação ou assinatura.", "fas fa-clock", "#F0C808"),  # Muted Yellow
    ("Suspended", "O contrato foi temporariamente interrompido.", "fas fa-pause-circle", "#E29D3A"),  # Warm Amber
    ("Expired", "O contrato chegou ao fim da sua vigência sem ser renovado.", "fas fa-exclamation-circle", "#D77A61"),  # Soft Reddish Coral
    ("Cancelled", "O contrato foi cancelado antes de ser concluído.", "fas fa-times-circle", "#D85757"),  # Subtle Red
    ("Draft", "O contrato está sendo criado ou revisado, mas não foi finalizado.", "fas fa-pencil-alt", "#8FAADC"),  # Gentle Blue
    ("Renewed", "O contrato foi renovado para um novo período.", "fas fa-sync-alt", "#73BDA8"),  # Calm Teal
    ("Closed", "O contrato foi concluído e finalizado, sem mais obrigações.", "fas fa-check-circle", "#B2BABB"),  # Neutral Gray
    ("Under Review", "O contrato está sob análise para revisão ou renegociação.", "fas fa-search", "#F4A261"),  # Soft Orange
    ("Terminated", "O contrato foi encerrado antes da data prevista.", "fas fa-exclamation-circle", "#C44B4F"),  # Faded Red
    ("Nullified", "O contrato foi anulado, como se nunca tivesse existido.", "fas fa-ban", "#A1749D"),  # Muted Purple
    ("Rejected", "O contrato foi rejeitado e não foi aceito ou aprovado.", "fas fa-times-circle", "#E1A3A3"),  # Pale Pinkish Red
]




    with connection.cursor() as cursor:
        cursor.execute("SELECT state FROM contract_state;")
        existing_states = {row[0] for row in cursor.fetchall()}

        for state, description, icon, hex in contract_states:
            if state not in existing_states:
                cursor.execute(
                    """
                    INSERT INTO contract_state (state, description, icon, hex_color)
                    VALUES (%s, %s, %s, %s);
                    """,
                    [state, description, icon, hex]
                )
                print(f"Inserted contract state: {state}")
            else:
                print(f"Contract state '{state}' already exists.")

def delete(quantity=None):
    with connection.cursor() as cursor:
        if quantity is not None and quantity > 0:
            cursor.execute(
                f"""
                DELETE FROM contract_state 
                WHERE id_contract_state IN (
                    SELECT id_contract_state FROM contract_state 
                    ORDER BY id_contract_state ASC 
                    LIMIT %s
                );
                """,
                [quantity]
            )
        else:
            cursor.execute("DELETE FROM contract_state;")