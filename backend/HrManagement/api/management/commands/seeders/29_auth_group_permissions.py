#! auth_group_permissions.py
#? python manage.py seed --seeder 29_auth_group_permissions

from django.db import connection

GROUP_PERMISSIONS = {
    "HR Manager": [
        "view_all_certificate_types",
        "create_certificate_type",
        "view_all_employees",
        "update_employee",
    ],
    "Recruitment Specialist": [
        "view_all_certificate_types",
        "create_certificate_type",
    ],
    "Payroll Manager": [
        "view_all_employees",
        "view_employee_contracts",
    ],
    "Training Coordinator": [
        "view_all_training_types",
        "create_training_type",
    ],
    "Department Head": [
        "view_all_departments",
        "update_department",
    ],
    "Employee": ["view_employee"],
    "Contract Administrator": [
        "view_all_contract_leave_types",
        "update_contract_leave_type",
    ],
    "Benefits Coordinator": [
        "view_all_type_benefits",
        "create_type_benefit",
    ],
    "System Administrator": [
        "view_all_contract_states",
        "create_contract_state",
    ],
}

def seed(quantity):
    with connection.cursor() as cursor:
        # Fetch existing permissions
        cursor.execute("SELECT id, codename FROM auth_permission;")
        permissions = {row[1]: row[0] for row in cursor.fetchall()}

        # Fetch existing groups
        cursor.execute("SELECT id, name FROM auth_group;")
        groups = {row[1]: row[0] for row in cursor.fetchall()}

        total_groups = len(GROUP_PERMISSIONS)
        completed_groups = 0

        for group_name, permission_codenames in GROUP_PERMISSIONS.items():
            group_id = groups.get(group_name)
            if not group_id:
                print(f"Group not found: {group_name}")
                continue

            for codename in permission_codenames:
                permission_id = permissions.get(codename)
                if permission_id:
                    cursor.execute(
                        """
                        SELECT COUNT(*) FROM auth_group_permissions
                        WHERE group_id = %s AND permission_id = %s;
                        """,
                        [group_id, permission_id]
                    )
                    if cursor.fetchone()[0] == 0:  # Only associate if not exists
                        cursor.execute(
                            """
                            INSERT INTO auth_group_permissions (group_id, permission_id)
                            VALUES (%s, %s);
                            """,
                            [group_id, permission_id]
                        )

            completed_groups += 1
            progress = int((completed_groups / total_groups) * 100)
            print(f"Progress: {progress}% completed.")

def delete_all():
    with connection.cursor() as cursor:
        cursor.execute("DELETE FROM auth_group_permissions;")
        print("All permissions deleted.")
