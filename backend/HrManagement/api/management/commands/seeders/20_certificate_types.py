#
#! certificate_types.py
#? python manage.py seed --seeder 20_certificate_types

from django.db import connection
from faker import Faker


"""
CREATE TABLE IF NOT EXISTS certificate_types (
    id_certificate_type UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(50) NOT NULL,
    description TEXT NOT NULL,
    icon VARCHAR(100) NOT NULL,
    hex_color VARCHAR(6) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP DEFAULT NULL
);
"""

fontAwesomeIcons = [
  "home",
  "user",
  "users",
  "envelope",
  "phone",
  "lock",
  "unlock",
  "camera",
  "shopping-cart",
  "heart",
  "star",
  "book",
  "calendar",
  "cloud",
  "file",
  "folder",
  "globe",
  "bell",
  "map",
  "music",
  "play",
  "pause",
  "stop",
  "trash",
  "search",
  "cog",
  "edit",
  "eye",
  "download",
  "upload",
  "check",
  "times",
  "plus",
  "minus",
  "arrow-up",
  "arrow-down",
  "arrow-left",
  "arrow-right",
  "comment",
  "comments",
  "paperclip",
  "image",
  "video",
  "lightbulb",
  "pencil-alt",
  "question-circle",
  "exclamation-circle",
  "car",
  "bicycle",
  "truck",
  "plane",
  "ship",
  "anchor",
  "wifi",
  "battery-full",
  "battery-half",
  "battery-empty",
  "headphones",
  "briefcase",
  "hospital",
  "university",
  "industry",
  "key",
  "link",
  "sun",
  "moon",
  "clock",
  "shield",
  "gift",
  "coffee",
  "utensils",
  "medkit",
  "balance-scale",
  "hammer",
  "gavel",
  "flag",
  "trophy",
  "fire",
  "leaf",
  "road",
  "tv",
  "laptop",
  "tablet",
  "mobile",
  "microphone",
  "printer",
  "barcode",
  "qrcode",
  "shopping-bag",
  "handshake",
  "money-bill",
  "credit-card",
  "wallet",
  "piggy-bank"
]


def seed(quantity=10):
    fake = Faker()
    with connection.cursor() as cursor:
        cursor.execute("SELECT id_certificate_type FROM certificate_types ORDER BY RANDOM();")
        certificate_types = [row[0] for row in cursor.fetchall()]

        if not certificate_types:
            for _ in range(quantity):
                name = fake.word()
                description = fake.text()
                icon = fake.random_element(fontAwesomeIcons)
                hex_color = fake.hex_color()
                cursor.execute(
                    """
                    INSERT INTO certificate_types (name, description, icon, hex_color)
                    VALUES (%s, %s, %s, %s);
                    """,
                    [name, description, icon, hex_color]
                )
                if (quantity >= 4) and ((_ + 1) % (quantity // 4) == 0):  # 25% checkpoints
                    print(f"Progress: {((_ + 1) / quantity) * 100:.0f}% completed.")
        else:
            print("Certificate types already seeded.")

def delete(quantity=None):
    with connection.cursor() as cursor:
        if quantity is not None and quantity > 0:
            cursor.execute(
                f"""
                DELETE FROM certificate_types 
                WHERE id_certificate_type IN (
                    SELECT id_certificate_type FROM certificate_types 
                    ORDER BY id_certificate_type ASC 
                    LIMIT %s
                );
                """,
                [quantity]
            )
        else:
            cursor.execute("DELETE FROM certificate_types;")

