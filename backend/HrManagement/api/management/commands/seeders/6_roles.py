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

def seed(quantity=None):
    roles = [
        # (role_name, department_name, group_name, description, hex_color)
        ("HR Specialist", "Human Resources", "HR Manager", "Supports HR operations and employee relations.", "#6CC24A"),
        ("HR Coordinator", "Human Resources", "Recruitment Specialist", "Assists in recruitment and onboarding processes.", "#7ED957"),
        
        ("Financial Analyst", "Finance", "Payroll Manager", "Analyzes financial data and supports budgeting.", "#D77A61"),
        ("Payroll Specialist", "Finance", "Payroll Manager", "Manages employee compensation and payroll processing.", "#E57373"),
        
        ("IT Support Technician", "IT", "System Administrator", "Provides technical support and maintains IT infrastructure.", "#8FAADC"),
        ("Network Administrator", "IT", "System Administrator", "Manages network systems and cybersecurity.", "#5E9CE3"),
        
        ("Marketing Specialist", "Marketing", "Marketing", "Develops and implements marketing strategies.", "#F4A261"),
        ("Digital Marketing Coordinator", "Marketing", "Marketing", "Manages digital marketing campaigns and analytics.", "#FF9800"),
        
        ("Sales Representative", "Sales", "Sales", "Drives sales and manages client relationships.", "#D85757"),
        ("Senior Sales Manager", "Sales", "Sales", "Leads sales team and develops business growth strategies.", "#C62828"),
        
        ("Operations Coordinator", "Operations", "Operations", "Supports daily operational workflows.", "#8A7BDF"),
        ("Operations Manager", "Operations", "Operations", "Oversees and optimizes organizational operations.", "#6A1B9A"),
        
        ("Legal Counsel", "Legal", "Legal", "Provides legal advice and ensures regulatory compliance.", "#C44B4F"),
        ("Compliance Specialist", "Legal", "Legal", "Monitors and ensures organizational compliance.", "#B0413E")
    ]

    with connection.cursor() as cursor:
        # Fetch existing departments and groups
        cursor.execute("""
            SELECT d.name AS department_name, d.id_department, 
                   g.name AS group_name, g.id AS group_id
            FROM departments d
            CROSS JOIN auth_group g
        """)
        department_group_map = {
            (row['department_name'], row['group_name']): 
            {'department_id': row['id_department'], 'group_id': row['group_id']}
            for row in [dict(zip(['department_name', 'id_department', 'group_name', 'group_id'], x)) 
                        for x in cursor.fetchall()]
        }

        # Check existing roles to avoid duplicates
        cursor.execute("SELECT role_name, id_department, id_auth_group FROM roles")
        existing_roles = {(row[0], row[1], row[2]) for row in cursor.fetchall()}

        # Insert roles
        total_roles = len(roles)
        inserted_count = 0

        for idx, (role_name, department_name, group_name, description, hex_color) in enumerate(roles, start=1):
            # Find matching department and group
            key = (department_name, group_name)
            if key not in department_group_map:
                print(f"Warning: No match found for {department_name} and {group_name}")
                continue

            department_id = department_group_map[key]['department_id']
            group_id = department_group_map[key]['group_id']

            # Check if role already exists
            if (role_name, department_id, group_id) not in existing_roles:
                try:
                    cursor.execute(
                        """
                        INSERT INTO roles (
                            role_name, 
                            id_department, 
                            id_auth_group, 
                            hex_color, 
                            description
                        ) VALUES (%s, %s, %s, %s, %s);
                        """,
                        [role_name, department_id, group_id, hex_color, description]
                    )
                    inserted_count += 1
                except Exception as e:
                    print(f"Error inserting role {role_name}: {e}")

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
