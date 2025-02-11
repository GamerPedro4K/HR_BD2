from django.db import connection

groups = [
    # (name, description)
    ("HR Manager", "Group responsible for managing all HR functionalities."),
    ("Recruitment Specialist", "Group focused on hiring processes and managing candidates."),
    ("Payroll Manager", "Group that handles employee payments, deductions, and bonuses."),
    ("Training Coordinator", "Group responsible for managing employee training and certifications."),
    ("Department Head", "Group managing department-level employee data and roles."),
    ("Employee", "Group for general employees with limited access."),
    ("Contract Administrator", "Group handling contracts, leave types, and contract states."),
    ("Benefits Coordinator", "Group focused on managing employee benefits."),
    ("System Administrator", "Group responsible for overseeing the HR management system."),
    ("Devolper", "Software developer"),
    ("Marketing", "Group responsible for managing marketing campaigns."),
    ("Sales", "Group responsible for managing sales and client acquisition."),
    ("Operations", "Group responsible for managing day-to-day operations."),
    ("Legal", "Group responsible for managing legal documentation and compliance."),
]

def seed(quantity):
    with connection.cursor() as cursor:
        cursor.execute("SELECT name FROM auth_group;")
        existing_groups = {row[0] for row in cursor.fetchall()}

        total_groups = len(groups)
        added_count = 0

        for index, (name, description) in enumerate(groups, start=1):
            if name not in existing_groups:
                cursor.execute(
                    """
                    INSERT INTO auth_group (name)
                    VALUES (%s);
                    """,
                    [name]
                )
                added_count += 1

            if total_groups >= 4 and (index % (total_groups // 4) == 0):
                progress = (index / total_groups) * 100
                print(f"Progress: {progress:.0f}% completed.)")

        print("Progress: 100% completed.")

def delete_all():
    with connection.cursor() as cursor:
        cursor.execute("DELETE FROM auth_group;")
        print("All groups deleted.")
