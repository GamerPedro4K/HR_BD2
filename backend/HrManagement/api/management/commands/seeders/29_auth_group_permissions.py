#! auth_group_permissions.py
#? python manage.py seed --seeder 29_auth_group_permissions

from django.db import connection

GROUP_PERMISSIONS = {
    # HR Management
    "HR Manager": [
        # Certificate Management
        "view_all_certificate_types", "view_certificate_type",
        "create_certificate_type", "update_certificate_type", "delete_certificate_type",
        
        # Employee Management
        "view_all_employees", "view_employee",
        "create_employee", "update_employee",
        
        # Department Management
        "view_all_departments", "view_department",
        
        # Role Management
        "view_all_roles", "view_role",
        
        # Contract Management
        "view_all_contract_types", "view_contract_type",
        "create_contract_type", "update_contract_type",
        
        # Benefits Management
        "view_all_type_benefits", "view_type_benefit",
        "create_type_benefit", "update_type_benefit",
        
        # Analytics
        "view_analytics",
        
        # Auth Groups
        "view_all_auth_groups", "view_auth_group",
        "add_group_permissions", "delete_group_permissions"
    ],
    
    "Recruitment Specialist": [
        # Employee Management
        "view_all_employees", "view_employee",
        "create_employee",
        
        # Certificate Management
        "view_all_certificate_types", "view_certificate_type",
        
        # Training Management
        "view_all_training_types", "view_training_type",
        
        # Department View
        "view_all_departments", "view_department"
    ],
    
    "Payroll Manager": [
        # Payment Management
        "view_all_payment_methods", "view_payment_method",
        "create_payment_method", "update_payment_method",
        
        # Salary Management
        "view_all_salary_history", "view_salary_history",
        "create_salary_history", "update_salary_history",
        
        # Deductions & Bonuses
        "view_all_deductions", "create_deduction",
        "view_all_bonuses", "create_bonus",
        
        # Employee View
        "view_all_employees", "view_employee",
        
        # Analytics
        "view_analytics"
    ],
    
    "Training Coordinator": [
        # Training Management
        "view_all_training_types", "view_training_type",
        "create_training_type", "update_training_type",
        
        # Certificate Management
        "view_all_certificate_types", "view_certificate_type",
        
        # Employee View
        "view_all_employees", "view_employee"
    ],
    
    "Department Head": [
        # Department Management
        "view_all_departments", "view_department",
        "update_department",
        
        # Employee Management
        "view_all_employees", "view_employee",
        "update_employee",
        
        # Role Management
        "view_all_roles", "view_role",
        
        # Analytics
        "view_analytics"
    ],
    
    "Employee": [
        "view_employee",
        "view_department",
        "view_role",
        "view_training_type",
        "view_certificate_type",
        "view_salary_history"
    ],
    
    "Contract Administrator": [
        # Contract Management
        "view_all_contract_types", "view_contract_type",
        "create_contract_type", "update_contract_type",
        
        # Contract State Management
        "view_all_contract_states", "view_contract_state",
        "create_contract_state", "update_contract_state",
        
        # Contract Leave Management
        "view_all_contract_leave_types", "view_contract_leave_type",
        "create_contract_leave_type", "update_contract_leave_type",
        
        # Employee View
        "view_all_employees", "view_employee"
    ],
    
    "Benefits Coordinator": [
        # Benefits Management
        "view_all_type_benefits", "view_type_benefit",
        "create_type_benefit", "update_type_benefit",
        
        # Employee View
        "view_all_employees", "view_employee",
        
        # Contract View
        "view_all_contract_types", "view_contract_type"
    ],
    
    "System Administrator": [
        # Full System Access
        "view_all_certificate_types", "view_certificate_type",
        "create_certificate_type", "update_certificate_type", "delete_certificate_type",
        
        "view_all_contract_leave_types", "view_contract_leave_type",
        "create_contract_leave_type", "update_contract_leave_type", "delete_contract_leave_type",
        
        "view_all_contract_states", "view_contract_state",
        "create_contract_state", "update_contract_state", "delete_contract_state",
        
        "view_all_contract_types", "view_contract_type",
        "create_contract_type", "update_contract_type", "delete_contract_type",
        
        "view_all_departments", "view_department",
        "create_department", "update_department", "delete_department",
        
        "view_all_employees", "view_employee",
        "create_employee", "update_employee",
        
        "view_all_payment_methods", "view_payment_method",
        "create_payment_method", "update_payment_method", "delete_payment_method",
        
        "view_all_training_types", "view_training_type",
        "create_training_type", "update_training_type", "delete_training_type",
        
        "view_all_type_benefits", "view_type_benefit",
        "create_type_benefit", "update_type_benefit", "delete_type_benefit",
        
        "view_all_auth_groups", "view_auth_group",
        "create_auth_group", "update_auth_group", "delete_auth_group",
        
        "view_all_permissions", "add_group_permissions", "delete_group_permissions",
        
        "view_analytics"
    ],
    
    "Developer": [
        # Django Admin Permissions
        "add_logentry", "change_logentry", "delete_logentry", "view_logentry",
        "add_permission", "change_permission", "delete_permission", "view_permission",
        "add_group", "change_group", "delete_group", "view_group",
        "add_user", "change_user", "delete_user", "view_user",
        "add_contenttype", "change_contenttype", "delete_contenttype", "view_contenttype",
        "add_session", "change_session", "delete_session", "view_session",
        
        # Certificate Types
        "view_all_certificate_types", "view_certificate_type",
        "create_certificate_type", "update_certificate_type", "delete_certificate_type",
        
        # Contract Leave Types
        "view_all_contract_leave_types", "view_contract_leave_type",
        "create_contract_leave_type", "update_contract_leave_type", "delete_contract_leave_type",
        
        # Contract States
        "view_all_contract_states", "view_contract_state",
        "create_contract_state", "update_contract_state", "delete_contract_state",
        
        # Contract Types
        "view_all_contract_types", "view_contract_type",
        "create_contract_type", "update_contract_type", "delete_contract_type",
        
        # Departments
        "view_all_departments", "view_department",
        "create_department", "update_department", "delete_department",
        
        # Employees
        "view_all_employees", "view_employee", "view_employee_contracts",
        "create_employee", "update_employee",
        
        # Payment Methods
        "view_all_payment_methods", "view_payment_method",
        "create_payment_method", "update_payment_method", "delete_payment_method",
        
        # Training Types
        "view_all_training_types", "view_training_type",
        "create_training_type", "update_training_type", "delete_training_type",
        
        # Benefits
        "view_all_type_benefits", "view_type_benefit",
        "create_type_benefit", "update_type_benefit", "delete_type_benefit",
        
        # Extra Hours
        "view_all_extra_hours", "view_extra_hours",
        "create_extra_hours", "update_extra_hours", "delete_extra_hours",
        
        # Schedules
        "view_all_schedules", "view_schedule",
        "create_schedule", "update_schedule", "delete_schedule",
        
        # Attendance
        "view_all_attendance", "view_attendance",
        "create_attendance", "update_attendance", "delete_attendance",
        
        # Vacations
        "view_all_vacations", "view_vacation",
        "create_vacation", "update_vacation", "delete_vacation",
        
        # Absence Reasons
        "view_all_absence_reasons", "view_absence_reason",
        "create_absence_reason", "update_absence_reason", "delete_absence_reason",
        
        # Salary History
        "view_all_salary_history", "view_salary_history",
        "create_salary_history", "update_salary_history", "delete_salary_history",
        
        # Deductions
        "view_all_deductions", "view_deduction",
        "create_deduction", "update_deduction", "delete_deduction",
        
        # Bonuses
        "view_all_bonuses", "view_bonus",
        "create_bonus", "update_bonus", "delete_bonus",
        
        # Roles
        "view_all_roles", "view_role",
        "create_role", "update_role", "delete_role",
        
        # Contract State Contract
        "view_contract_state_contract",
        "create_contract_state_contract",
        "update_contract_state_contract",
        "delete_contract_state_contract",
        
        # Auth Groups
        "view_all_auth_groups", "view_auth_group",
        "create_auth_group", "update_auth_group", "delete_auth_group",
        
        # Permissions
        "view_all_permissions", "add_group_permissions", "delete_group_permissions",
        "view_all_permissions_user_group",
        
        # Analytics
        "view_analytics"
    ],
    
    "Marketing": [
        # Limited access for marketing purposes
        "view_all_departments", "view_department",
        "view_employee",  # Limited employee view
        "view_analytics"
    ],
    
    "Sales": [
        # Sales team access
        "view_all_departments", "view_department",
        "view_employee",  # Limited employee view
        "view_analytics"
    ],
    
    "Operations": [
        # Operations team access
        "view_all_departments", "view_department",
        "view_all_employees", "view_employee",
        "view_all_training_types", "view_training_type",
        "view_analytics"
    ],
    
    "Legal": [
        # Legal team access
        "view_all_contract_types", "view_contract_type",
        "view_all_contract_states", "view_contract_state",
        "view_all_contract_leave_types", "view_contract_leave_type",
        "view_all_departments", "view_department",
        "view_employee",  # Limited employee view
        "view_analytics"
    ]
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
