#! roles.py
#? python manage.py seed --seeder 4_roles
# This file is used to seed the roles table with fake data.

import random
from django.db import connection
from faker import Faker

""" 
CREATE TABLE IF NOT EXISTS roles (
    id_role UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    id_department UUID NOT NULL,
    id_auth_group INTEGER NOT NULL,
    role_name VARCHAR(100),
    hex_color VARCHAR(7),
    description TEXT,
    FOREIGN KEY (id_department) REFERENCES departments(id_department),
    FOREIGN KEY (id_auth_group) REFERENCES auth_group(id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP DEFAULT NULL
);
 """

def seed(quantity=100):
    roles = [
        ("HR Specialist", "Human Resources", "HR Manager", "Handles HR-specific tasks and compliance.", "#6CC24A"),
        ("Payroll Specialist", "Finance", "Payroll Manager", "Manages payroll processes.", "#D77A61"),
        ("IT Support", "IT", "System Administrator", "Maintains IT operations and security.", "#8FAADC"),
        ("Marketing Coordinator", "Marketing", None, "Manages marketing campaigns.", "#F4A261"),
        ("Sales Representative", "Sales", None, "Drives client acquisition.", "#D85757"),
        ("Operations Manager", "Operations", None, "Oversees operational workflows.", "#8A7BDF"),
        ("Legal Advisor", "Legal", None, "Handles legal documentation and compliance.", "#C44B4F"),
    ]

    with connection.cursor() as cursor:
        cursor.execute("SELECT id_department, name FROM departments;")
        departments = {row[1]: row[0] for row in cursor.fetchall()}

        cursor.execute("SELECT id, name FROM auth_group;")
        groups = {row[1]: row[0] for row in cursor.fetchall()}

        cursor.execute("SELECT role_name, id_department, id_auth_group FROM roles;")
        existing_roles = {
            (row[0], row[1], row[2]) for row in cursor.fetchall()
        }

        total_roles = len(roles)

        for idx, (role_name, department_name, group_name, description, hex_color) in enumerate(roles, start=1):
            id_department = departments.get(department_name)
            id_auth_group = groups.get(group_name)

            if id_department and id_auth_group and (role_name, id_department, id_auth_group) not in existing_roles:
                cursor.execute(
                    """
                    INSERT INTO roles (role_name, id_department, id_auth_group, hex_color, description)
                    VALUES (%s, %s, %s, %s, %s);
                    """,
                    [role_name, id_department, id_auth_group, hex_color, description]
                )

            # Print progress at 25% intervals
            if total_roles >= 4 and (idx % (total_roles // 4) == 0):
                print(f"Progress: {(idx / total_roles) * 100:.0f}% completed.")

        print("Progress: 100% completed.")

def delete(quantity=None):
    with connection.cursor() as cursor:
        if quantity is not None and quantity > 0:
            cursor.execute(
                f"""
                DELETE FROM roles 
                WHERE id_role IN (
                    SELECT id_role FROM roles 
                    ORDER BY id_role ASC 
                    LIMIT %s
                );
                """,
                [quantity]
            )
        else:
            cursor.execute("DELETE FROM roles;")
