#
#! contract_type.py
#? python manage.py seed --seeder 9_contract_type

from django.db import connection
from faker import Faker

""" 
CREATE TABLE IF NOT EXISTS contract_type (
    id_contract_type UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    contract_type_name VARCHAR(100),
    description TEXT,
    termination_notice_period NUMERIC(10, 2),
    overtime_eligible BOOLEAN,
    benefits_eligible BOOLEAN,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP DEFAULT NULL
);
"""

def seed(quantity=None):
    contract_types = [
        {
            "contract_type_name": "Permanent Contract",
            "description": "An indefinite employment agreement offering job stability and full benefits.",
            "termination_notice_period": 30,
            "overtime_eligible": True,
            "benefits_eligible": True,
        },
        {
            "contract_type_name": "Fixed-Term Contract",
            "description": "A temporary agreement with a predefined duration, typically for specific projects.",
            "termination_notice_period": 15,
            "overtime_eligible": True,
            "benefits_eligible": False,
        },
        {
            "contract_type_name": "Part-Time Contract",
            "description": "An agreement for reduced working hours, typically with proportional benefits.",
            "termination_notice_period": 15,
            "overtime_eligible": False,
            "benefits_eligible": True,
        },
        {
            "contract_type_name": "Freelance Contract",
            "description": "A flexible contract for independent workers, often project-based.",
            "termination_notice_period": 7,
            "overtime_eligible": False,
            "benefits_eligible": False,
        },
        {
            "contract_type_name": "Internship Contract",
            "description": "A temporary arrangement for students or recent graduates to gain work experience.",
            "termination_notice_period": 7,
            "overtime_eligible": False,
            "benefits_eligible": False,
        },
        {
            "contract_type_name": "Apprenticeship Contract",
            "description": "A contract focused on skills training, typically for young workers.",
            "termination_notice_period": 7,
            "overtime_eligible": False,
            "benefits_eligible": True,
        },
        {
            "contract_type_name": "Zero-Hours Contract",
            "description": "A flexible contract with no guaranteed hours, offering work on demand.",
            "termination_notice_period": 1,
            "overtime_eligible": False,
            "benefits_eligible": False,
        },
        {
            "contract_type_name": "Seasonal Contract",
            "description": "A contract designed for work during specific seasons or periods.",
            "termination_notice_period": 14,
            "overtime_eligible": True,
            "benefits_eligible": False,
        },
        {
            "contract_type_name": "Consultancy Contract",
            "description": "An agreement for external experts to provide advice or services.",
            "termination_notice_period": 30,
            "overtime_eligible": False,
            "benefits_eligible": False,
        },
        {
            "contract_type_name": "Temporary Work Contract",
            "description": "A short-term contract for temporary assignments, often through an agency.",
            "termination_notice_period": 14,
            "overtime_eligible": True,
            "benefits_eligible": False,
        },
    ]
    
    with connection.cursor() as cursor:
        cursor.execute("SELECT id_contract_type FROM contract_type;")
        existing_records = cursor.fetchall()

        if not existing_records:
            for contract in contract_types:
                cursor.execute(
                    """
                    INSERT INTO contract_type (contract_type_name, description, termination_notice_period, overtime_eligible, benefits_eligible)
                    VALUES (%s, %s, %s, %s, %s);
                    """,
                    [
                        contract["contract_type_name"],
                        contract["description"],
                        contract["termination_notice_period"],
                        contract["overtime_eligible"],
                        contract["benefits_eligible"],
                    ]
                )
            print("Contract types successfully seeded.")
        else:
            print("Contract types already exist in the database.")

def delete(quantity=None):
    with connection.cursor() as cursor:
        if quantity is not None and quantity > 0:
            cursor.execute(
                f"""
                DELETE FROM contract_type 
                WHERE id_contract_type IN (
                    SELECT id_contract_type FROM contract_type 
                    ORDER BY id_contract_type ASC 
                    LIMIT %s
                );
                """,
                [quantity]
            )
        else:
            cursor.execute("DELETE FROM contract_type;")