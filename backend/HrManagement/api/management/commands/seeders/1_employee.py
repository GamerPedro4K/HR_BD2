#
#! employee.py
#? python manage.py seed --seeder 1_employee
# This file is used to seed the employees table with fake data.

import random
from django.db import connection
from faker import Faker
from django.contrib.auth.hashers import make_password


""" 
CREATE TABLE IF NOT EXISTS employees (
    id_auth_user INTEGER NOT NULL UNIQUE,
    id_employee UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    phone VARCHAR(50) NOT NULL,
    src VARCHAR(200) NOT NULL,
    birth_date DATE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP DEFAULT NULL
);

create table auth_user
(
    id           integer generated by default as identity
        primary key,
    password     varchar(128)             not null,
    last_login   timestamp with time zone,
    is_superuser boolean                  not null,
    username     varchar(150)             not null
        unique,
    first_name   varchar(150)             not null,
    last_name    varchar(150)             not null,
    email        varchar(254)             not null,
    is_staff     boolean                  not null,
    is_active    boolean                  not null,
    date_joined  timestamp with time zone not null
);
 """

def seed(quantity=100):
    fake = Faker()
    with connection.cursor() as cursor:
        cursor.execute("""SELECT * FROM employees
                       WHERE id_auth_user = 1
                       LIMIT 1;""")
        if cursor.fetchone() is None:
            passw = make_password("seguinte")
            cursor.execute(
                """
                INSERT INTO auth_user (id, username, password, first_name, last_name, email, is_superuser, is_staff, is_active, date_joined)
                VALUES (1, 'benno', %s, 'pedro', 'benno', 'pedro@example.com', True, True, True, CURRENT_TIMESTAMP);
                """,
                [passw]
            )
            cursor.execute("""INSERT INTO employees (id_auth_user, phone, src, birth_date, created_at, updated_at)
                           VALUES (1, '123456789', 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRKVA3tt00vmEdcfrTjLzjCk8eYD4en-wVUQpbPpKxu6DmNQz_XtAJUK137I4PfNGfczyY&usqp=CAU', '1990-01-01', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);""")
        # Fetch existing usernames to ensure uniqueness
        cursor.execute("SELECT username FROM auth_user;")
        existing_usernames = {row[0] for row in cursor.fetchall()}

        # Get the last auth_user ID to calculate the next one
        id_auth_user = 2
        cursor.execute("SELECT id FROM auth_user ORDER BY id DESC LIMIT 1;")
        last_auth_user = cursor.fetchone()
        if last_auth_user:
            id_auth_user = last_auth_user[0] + 1

        for _ in range(quantity):
            # Generate a unique username
            username = fake.user_name()
            while username in existing_usernames:
                username = fake.user_name()
            existing_usernames.add(username)

            # Create the auth_user record
            password = make_password("password")
            first_name = fake.first_name()
            last_name = fake.last_name()
            email = fake.email()
            is_superuser = False
            is_staff = False
            is_active = True
            cursor.execute(
                """
                INSERT INTO auth_user (id, username, password, first_name, last_name, email, is_superuser, is_staff, is_active, date_joined)
                OVERRIDING SYSTEM VALUE
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, CURRENT_TIMESTAMP);
                """,
                [id_auth_user, username, password, first_name, last_name, email, is_superuser, is_staff, is_active]
            )


            # Create the employee record
            phone = fake.phone_number()
            src = f"https://picsum.photos/300/300?random={fake.random_digit}"
            birth_date = fake.date_of_birth(minimum_age=18, maximum_age=65)
            cursor.execute(
                """
                INSERT INTO employees (id_auth_user, phone, src, birth_date, created_at, updated_at)
                VALUES (%s, %s, %s, %s, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);
                """,
                [id_auth_user, phone, src, birth_date]
            )
            id_auth_user += 1

            # Print progress at 25% intervals
            if (quantity >= 4) and ((_ + 1) % (quantity // 4) == 0):
                print(f"Progress: {((_ + 1) / quantity) * 100:.0f}% completed.")


def delete(quantity=None):
    with connection.cursor() as cursor:
        if quantity is not None and quantity > 0:
            cursor.execute(
                f"""
                DELETE FROM employees 
                WHERE id_employee IN (
                    SELECT id_employee FROM employees 
                    ORDER BY id_employee ASC 
                    LIMIT %s
                );
                """,
                [quantity]
            )
            print(f"{quantity} records deleted from employees.")
        else:
            cursor.execute("DELETE FROM employees;")
            print("All records deleted from employees.")