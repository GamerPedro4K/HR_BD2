#
#! seed.py
#? python manage.py seed
#? python manage.py seed --quantity 1000 
#? python manage.py seed --seeder 1_employee

from django.core.management.base import BaseCommand
import importlib
import os
from pathlib import Path
import re

class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('--quantity', type=int, default=100, help='Number of records to create (min 10, max 10000)')
        parser.add_argument('--seeder', type=str, help='Specific seeder file to run (without the .py extension)')
    
    def handle(self, *args, **kwargs):
        quantity = kwargs['quantity']
        seeder_file_name = kwargs['seeder']

        if quantity < 10:
            quantity = 10
            print('The minimum quantity is 10. Defaulting to 10.')
        elif quantity > 10000:
            quantity = 10000
            print('The maximum quantity is 10000. Defaulting to 10000.')
        
        seeders_directory = Path(__file__).resolve().parent / 'seeders'

        if seeder_file_name:
            seeder_file_path = seeders_directory / f"{seeder_file_name}.py"
            if os.path.isfile(seeder_file_path):
                print(f"Seeder file found: {seeder_file_path}")
                seeder_module = importlib.import_module(f'api.management.commands.seeders.{seeder_file_name}')
                
                if hasattr(seeder_module, 'seed'):
                    self.stdout.write(self.style.SUCCESS(f'Seeding {seeder_file_name}...'))
                    seeder_module.seed(quantity)
                else:
                    self.stdout.write(self.style.ERROR(f'No seed method found in {seeder_file_name}.'))
            else:
                self.stdout.write(self.style.ERROR(f'Seeder file {seeder_file_name}.py not found.'))
        else:
            seeder_files = sorted(
                [f for f in os.listdir(seeders_directory) if f.endswith('.py') and f != '__init__.py'],
                key=lambda x: int(re.match(r'(\d+)_', x).group(1))
            )
            
            for seeder_file in seeder_files:
                seeder_name = seeder_file[:-3]  # Remove a extensão .py
                print(f"Seeder file: {seeder_name}")
                seeder_module = importlib.import_module(f'api.management.commands.seeders.{seeder_name}')
                
                if hasattr(seeder_module, 'seed'):
                    self.stdout.write(self.style.SUCCESS(f'Seeding {seeder_name}...'))
                    seeder_module.seed(quantity)
                    
        self.stdout.write(self.style.SUCCESS('Seeding completed!'))