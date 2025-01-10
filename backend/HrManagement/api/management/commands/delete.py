#
#! delete.py
#? python manage.py delete 
#? python manage.py delete --quantity 1000 
#? python manage.py delete --seeder 1_employee

import re
from django.core.management.base import BaseCommand
import importlib
import os
from pathlib import Path
from django.contrib.auth.models import User

class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('--quantity', type=int, default=None, help='Number of records to delete (\033[31mdepricated\033[m)')
        parser.add_argument('--seeder', type=str, help='Specific seeder file to delete records from')
    
    def handle(self, *args, **kwargs):
        quantity = kwargs['quantity']
        seeder_name = kwargs['seeder']

        seeders_directory = Path(__file__).resolve().parent / 'seeders'
        if seeder_name:
            # Verifica se o arquivo do seeder existe
            seeder_file_path = seeders_directory / f"{seeder_name}.py"
            if os.path.isfile(seeder_file_path):
                print(f"Seeder file found: {seeder_file_path}")
                seeder_module = importlib.import_module(f'api.management.commands.seeders.{seeder_name}')

                if hasattr(seeder_module, 'delete'):
                    self.stdout.write(self.style.SUCCESS(f'Deleting from {seeder_name}...'))
                    seeder_module.delete(quantity)
                else:
                    self.stdout.write(self.style.ERROR(f'No delete method found in {seeder_name}.'))
            else:
                self.stdout.write(self.style.ERROR(f'Seeder file {seeder_name}.py not found.'))
        else:
            # Ordena os arquivos de seeders em ordem inversa para deletar na ordem correta
            seeder_files = sorted(
                [f for f in os.listdir(seeders_directory) if f.endswith('.py') and not f.startswith('__')],
                key=lambda x: int(re.match(r'(\d+)_', x).group(1)),
                reverse=True
            )

            for seeder_file in seeder_files:
                seeder_name = seeder_file[:-3]
                print(f"Seeder file: {seeder_name}")
                seeder_module = importlib.import_module(f'api.management.commands.seeders.{seeder_name}')
                
                if hasattr(seeder_module, 'delete'):
                    self.stdout.write(self.style.SUCCESS(f'Deleting {seeder_name}...'))
                    seeder_module.delete(quantity)
            User.objects.all().delete()
        self.stdout.write(self.style.SUCCESS('Deletion completed successfully'))
