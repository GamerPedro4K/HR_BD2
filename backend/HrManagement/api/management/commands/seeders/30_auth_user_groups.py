#! auth_user_groups.py
#? python manage.py seed --seeder 30_auth_user_groups

from django.db import connection

def seed(quantity=None):
    with connection.cursor() as cursor:
        # Get existing user-group mappings to avoid duplicates
        cursor.execute("""
            SELECT user_id, group_id 
            FROM auth_user_groups;
        """)
        existing_mappings = {(row[0], row[1]) for row in cursor.fetchall()}

        # First handle user ID 1 with group ID 10
        if (1, 10) not in existing_mappings:
            cursor.execute("""
                INSERT INTO auth_user_groups (user_id, group_id)
                VALUES (1, 10)
                ON CONFLICT (user_id, group_id) DO NOTHING;
            """)

        # Complex query to get user-role-group relationships for other users
        cursor.execute("""
            WITH employee_contracts AS (
                -- Get employees with their latest contracts and roles
                SELECT 
                    au.id as user_id,
                    e.id_employee,
                    lcv.id_role,
                    r.id_auth_group as group_id
                FROM auth_user au
                JOIN employees e ON e.id_auth_user = au.id
                JOIN latest_contract_materialized_view lcv ON lcv.id_employee = e.id_employee
                JOIN roles r ON r.id_role = lcv.id_role
                WHERE au.is_active = true
                AND e.deleted_at IS NULL
                AND au.id != 1  -- Exclude user ID 1 as it's handled separately
            )
            SELECT 
                user_id,
                group_id
            FROM employee_contracts
            WHERE (user_id, group_id) NOT IN (
                SELECT user_id, group_id 
                FROM auth_user_groups
            );
        """)
        
        new_mappings = cursor.fetchall()
        total_mappings = len(new_mappings)
        
        if total_mappings > 0:
            # Insert new mappings in batches
            batch_size = 100
            for i in range(0, total_mappings, batch_size):
                batch = new_mappings[i:i + batch_size]
                values_str = ','.join(['(%s, %s)' for _ in batch])
                flat_values = [val for pair in batch for val in pair]
                
                cursor.execute(f"""
                    INSERT INTO auth_user_groups (user_id, group_id)
                    VALUES {values_str}
                    ON CONFLICT (user_id, group_id) DO NOTHING;
                """, flat_values)
                
                progress = min(100, int((i + batch_size) / total_mappings * 100))
                print(f"Progress: {progress}% completed")
        
        print("Progress: 100% completed")
        print(f"Added {total_mappings} new user-group mappings")

def delete(quantity=None):
    with connection.cursor() as cursor:
        if quantity is not None and quantity > 0:
            cursor.execute("""
                DELETE FROM auth_user_groups
                WHERE ctid IN (
                    SELECT ctid
                    FROM auth_user_groups
                    LIMIT %s
                );
            """, [quantity])
            print(f"{quantity} user-group mappings deleted")
        else:
            cursor.execute("DELETE FROM auth_user_groups;")
            print("All user-group mappings deleted")