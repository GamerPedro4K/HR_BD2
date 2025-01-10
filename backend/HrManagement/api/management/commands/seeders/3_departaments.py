#! departments.py
#? python manage.py seed --seeder 3_departments
# This file is used to seed the departments table with fake data.

from django.db import connection

""" 
CREATE TABLE IF NOT EXISTS departments (
    id_department UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(100) NOT NULL,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP DEFAULT NULL
);
 """

departments = [
    ("Human Resources", "Handles employee-related services and compliance.", "HR Manager"),
    ("Finance", "Manages company finances, budgets, and payroll.", "Payroll Manager"),
    ("IT", "Maintains IT infrastructure and security.", "System Administrator"),
    ("Marketing", "Oversees branding, campaigns, and promotions.", None),
    ("Sales", "Drives revenue through client acquisition and retention.", None),
    ("Operations", "Ensures efficient day-to-day operations.", None),
    ("Legal", "Handles legal matters and compliance.", None),
]
    
def seed(quantity):
    with connection.cursor() as cursor:
        cursor.execute("SELECT name FROM departments;")
        existing_departments = {row[0] for row in cursor.fetchall()}

        cursor.execute("SELECT id, name FROM auth_group;")
        groups = {row[1]: row[0] for row in cursor.fetchall()}

        total_departments = len(departments)

        for idx, (name, description, group_name) in enumerate(departments, start=1):
            if name in existing_departments:
                continue 

            # Insert new department
            cursor.execute(
                """
                INSERT INTO departments (name, description)
                VALUES (%s, %s)
                RETURNING id_department;
                """,
                [name, description]
            )
            id_department = cursor.fetchone()[0]

            # Handle roles
            if group_name and group_name in groups:
                id_auth_group = groups[group_name]
                cursor.execute(
                    """
                    SELECT COUNT(*) FROM roles
                    WHERE role_name = %s AND id_department = %s AND id_auth_group = %s;
                    """,
                    [f"Manager of {name}", id_department, id_auth_group]
                )
                if cursor.fetchone()[0] == 0:
                    cursor.execute(
                        """
                        INSERT INTO roles (role_name, id_department, id_auth_group, hex_color, description)
                        VALUES (%s, %s, %s, %s, %s);
                        """,
                        [f"Manager of {name}", id_department, id_auth_group, "#6CC24A", f"Manages {name} department."]
                    )
            if total_departments >= 4 and (idx % (total_departments // 4) == 0):
                print(f"Progress: {(idx / total_departments) * 100:.0f}% completed.")

        print("Progress: 100% completed.")

def delete_departments(quantity=None):
    with connection.cursor() as cursor:
        if quantity:
            cursor.execute(
                """
                DELETE FROM departments
                WHERE id_department IN (
                    SELECT id_department FROM departments
                    ORDER BY id_department ASC
                    LIMIT %s
                );
                """,
                [quantity]
            )
            print(f"{quantity} departments deleted.")
        else:
            cursor.execute("DELETE FROM departments;")
            print("All departments deleted.")
