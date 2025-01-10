# test.py
#! python manage.py test

from django.core.management.base import BaseCommand
from django.db import connection
import os
from pathlib import Path
import re

class Command(BaseCommand):
    
    
    def handle(self, *args, **kwargs):
        test_directory = Path(__file__).resolve().parent / 'test'
        
        if os.path.isdir(test_directory):
            sql_files = sorted(
                [f for f in os.listdir(test_directory) if f.endswith('.sql')],
                key=lambda x: int(re.match(r'(\d+)_', x).group(1) if re.match(r'(\d+)_', x) else 0)
            )
            
            for sql_file in sql_files:
                sql_file_path = test_directory / sql_file
                print(f"Executing SQL file: {sql_file_path}")
                
                try:
                    with open(sql_file_path, 'r') as f:
                        sql_query = f.read()

                    with connection.cursor() as cursor:
                        cursor.execute(sql_query)
                        self.stdout.write(self.style.SUCCESS(f'Successfully executed {sql_file_path}'))
                
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f'Error executing {sql_file_path}: {e}'))
                    
        self.stdout.write(self.style.SUCCESS('Testing completed!'))
