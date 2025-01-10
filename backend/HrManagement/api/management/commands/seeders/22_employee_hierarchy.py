#
#! employee_hierarchy.py
#? python manage.py seed --seeder 22_employee_hierarchy

import random
from django.db import connection

"""
CREATE TABLE IF NOT EXISTS employee_hierarchy (
    id_employee_hierarchy UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    id_employee UUID NOT NULL,
    id_employee_superior UUID,
    FOREIGN KEY (id_employee) REFERENCES employees(id_employee),
    FOREIGN KEY (id_employee_superior) REFERENCES employees(id_employee),
    start_date DATE NOT NULL,
    end_date DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP DEFAULT NULL
);
"""

def seed(quantity=100):
    with connection.cursor() as cursor:
        cursor.execute("""
                        SELECT id_employee 
                        FROM employees
                        WHERE id_employee NOT IN (SELECT id_employee_superior FROM employee_hierarchy)
                        AND id_employee NOT IN (SELECT id_employee FROM employee_hierarchy)
                        ORDER BY RANDOM();
                       """)
        employees = [row[0] for row in cursor.fetchall()]
        
        if not employees:
            print("No employees found. Please create employees before running the employee hierarchy seeder.")
            return
        
        quantity = min(quantity, len(employees))
        created_ids = set()

        for _ in range(quantity):
            id_employee = employees[_]
            id_employee_superior = (
                random.choice([emp for emp in employees if emp not in created_ids]) 
                if random.random() < 0.5 else None
            )
            
            # Ensure there is no circular hierarchy by preventing an employee from being their own superior
            if id_employee_superior == id_employee:
                id_employee_superior = None

            # Mark this employee as created to avoid using it again as superior in future iterations
            created_ids.add(id_employee)

            start_date = "2021-01-01"
            end_date = None
            cursor.execute(
                """
                INSERT INTO employee_hierarchy (id_employee, id_employee_superior, start_date, end_date)
                VALUES (%s, %s, %s, %s);
                """,
                [id_employee, id_employee_superior, start_date, end_date]
            )
            if (quantity >= 4) and ((_ + 1) % (quantity // 4) == 0):  # 25% checkpoints
                print(f"Progress: {((_ + 1) / quantity) * 100:.0f}% completed.")
    

            
def delete(quantity=None):
    with connection.cursor() as cursor:
        if quantity is not None and quantity > 0:
            cursor.execute(f"""
                            DELETE 
                            FROM employee_hierarchy
                            ORDER BY RANDOM()
                            LIMIT {quantity};
                            """)
        else:
            cursor.execute("DELETE FROM employee_hierarchy;")
