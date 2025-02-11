#
#! database.py

from django.core.management.base import BaseCommand
from django.core.management import call_command
from django.db import connection
import os
from pathlib import Path
from django.apps import apps
import io
from pymongo import MongoClient
from api.utils.mongo_client import get_mongo_db

collections = [
    {
        "name": "attendance",
        "validator": {
            "$jsonSchema": {
                "bsonType": "object",
                "required": ["id_employee", "date", "sessions"],
                "properties": {
                    "id_employee": {
                        "bsonType": "string",
                        "description": "ID do funcionário deve ser uma string representando um UUID válido."
                    },
                    "date": {
                        "bsonType": "string",
                        "pattern": "^(\\d{4})-(\\d{2})-(\\d{2})$",
                        "description": "Data deve estar no formato ISO (yyyy-MM-dd)."
                    },
                    "sessions": {
                        "bsonType": "array",
                        "items": {
                            "bsonType": "object",
                            "required": ["checkin"],
                            "properties": {
                                "checkin": {
                                    "bsonType": "string",
                                    "pattern": "^(\\d{2}):(\\d{2}):(\\d{2})$",
                                    "description": "Check-in deve ser uma string no formato ISO (HH:mm:ss)."
                                },
                                "checkout": {
                                    "bsonType": ["string", "null"],
                                    "pattern": "^(\\d{2}):(\\d{2}):(\\d{2})$",
                                    "description": "Check-out deve ser uma string no formato ISO (HH:mm:ss)."
                                }
                            }
                        }
                    }
                }
            }
        }
    },
    {
        "name": "extrahours",
        "validator": {
            "$jsonSchema": {
                "bsonType": "object",
                "required": ["id_employee", "date", "start", "end"],
                "properties": {
                    "id_employee": {
                        "bsonType": "string",
                        "description": "ID do funcionário deve ser uma string representando um UUID válido."
                    },
                    "date": {
                        "bsonType": "string",
                        "pattern": "^(\\d{4})-(\\d{2})-(\\d{2})$",
                        "description": "Data deve estar no formato ISO (yyyy-MM-dd)."
                    },
                    "start": {
                        "bsonType": "string",
                        "pattern": "(\\d{2}):(\\d{2}):(\\d{2})$",
                        "description": "Hora de início deve estar no formato ISO (HH:mm:ss)."
                    },
                    "end": {
                        "bsonType": "string",
                        "pattern": "(\\d{2}):(\\d{2}):(\\d{2})$",
                        "description": "Hora de término deve estar no formato ISO (HH:mm:ss)."
                    }
                }
            }
        }
    },
     {
        "name": "schedule",
        "validator": {
            "$jsonSchema": {
                "bsonType": "object",
                "required": ["id_employee", "workSchedule"],
                "properties": {
                    "id_employee": {
                        "bsonType": "string",
                        "description": "ID do funcionário deve ser uma string representando um UUID válido."
                    },
                    "workSchedule": {
                        "bsonType": "object",
                        "properties": {
                            "monday": {
                                "bsonType": "object",
                                "required": ["start", "end"],
                                "properties": {
                                    "start": {
                                        "bsonType": "string",
                                        "pattern": "^(\\d{2}):(\\d{2})$",
                                        "description": "Hora de início deve estar no formato HH:mm."
                                    },
                                    "end": {
                                        "bsonType": "string",
                                        "pattern": "^(\\d{2}):(\\d{2})$",
                                        "description": "Hora de término deve estar no formato HH:mm."
                                    }
                                }
                            },
                            "tuesday": {
                                "bsonType": "object",
                                "required": ["start", "end"],
                                "properties": {
                                    "start": {
                                        "bsonType": "string",
                                        "pattern": "^(\\d{2}):(\\d{2})$",
                                        "description": "Hora de início deve estar no formato HH:mm."
                                    },
                                    "end": {
                                        "bsonType": "string",
                                        "pattern": "^(\\d{2}):(\\d{2})$",
                                        "description": "Hora de término deve estar no formato HH:mm."
                                    }
                                }
                            },
                            "wednesday": {
                                "bsonType": "object",
                                "required": ["start", "end"],
                                "properties": {
                                    "start": {
                                        "bsonType": "string",
                                        "pattern": "^(\\d{2}):(\\d{2})$",
                                        "description": "Hora de início deve estar no formato HH:mm."
                                    },
                                    "end": {
                                        "bsonType": "string",
                                        "pattern": "^(\\d{2}):(\\d{2})$",
                                        "description": "Hora de término deve estar no formato HH:mm."
                                    }
                                }
                            },
                            "thursday": {
                                "bsonType": "object",
                                "required": ["start", "end"],
                                "properties": {
                                    "start": {
                                        "bsonType": "string",
                                        "pattern": "^(\\d{2}):(\\d{2})$",
                                        "description": "Hora de início deve estar no formato HH:mm."
                                    },
                                    "end": {
                                        "bsonType": "string",
                                        "pattern": "^(\\d{2}):(\\d{2})$",
                                        "description": "Hora de término deve estar no formato HH:mm."
                                    }
                                }
                            },
                            "friday": {
                                "bsonType": "object",
                                "required": ["start", "end"],
                                "properties": {
                                    "start": {
                                        "bsonType": "string",
                                        "pattern": "^(\\d{2}):(\\d{2})$",
                                        "description": "Hora de início deve estar no formato HH:mm."
                                    },
                                    "end": {
                                        "bsonType": "string",
                                        "pattern": "^(\\d{2}):(\\d{2})$",
                                        "description": "Hora de término deve estar no formato HH:mm."
                                    }
                                }
                            },
                            "saturday": {
                                "bsonType": "object",
                                "required": ["start", "end"],
                                "properties": {
                                    "start": {
                                        "bsonType": "string",
                                        "pattern": "^(\\d{2}):(\\d{2})$",
                                        "description": "Hora de início deve estar no formato HH:mm."
                                    },
                                    "end": {
                                        "bsonType": "string",
                                        "pattern": "^(\\d{2}):(\\d{2})$",
                                        "description": "Hora de término deve estar no formato HH:mm."
                                    }
                                }
                            },
                            "sunday": {
                                "bsonType": "object",
                                "required": ["start", "end"],
                                "properties": {
                                    "start": {
                                        "bsonType": "string",
                                        "pattern": "^(\\d{2}):(\\d{2})$",
                                        "description": "Hora de início deve estar no formato HH:mm."
                                    },
                                    "end": {
                                        "bsonType": "string",
                                        "pattern": "^(\\d{2}):(\\d{2})$",
                                        "description": "Hora de término deve estar no formato HH:mm."
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
    }
]

class Command(BaseCommand):
    help = 'Executa arquivos SQL específicos ou todos os arquivos SQL dentro dos diretórios database/ ou database/functions/'

    def add_arguments(self, parser):
        parser.add_argument('--file', type=str, help='Arquivo SQL específico para executar (ex: /functions/get_employees.sql)')
        parser.add_argument('--create', action='store_true', help='Criar somente os dados da base de dados postgres SQL (os procedimentos, funções e etc.. não serão criados. Caso queira execute \033[32mpython manage.py database\033[m`). (ex: --create)')
        parser.add_argument('--drop', action='store_true', help='Deletar somente os dados da base de dados postgres SQL (os procedimentos, funções e etc.. não serão influenciados). (ex: --drop)')

    def handle(self, *args, **kwargs):
        sql_file = kwargs['file']
        create_db = kwargs['create']
        drop_db = kwargs['drop']
    
        if sum([bool(sql_file), create_db, drop_db]) > 1:
            self.stdout.write(self.style.ERROR("Use apenas uma das opções: --file, --create ou --drop."))
            return
    
        base_dir = Path(__file__).resolve().parent / 'database'
        functions_dir = base_dir / 'functions'
        views_dir = base_dir / 'views'
        procedures_dir = base_dir / 'procedures'
        db_sql_path = base_dir / 'db.sql'
        db_sql_drop_path = base_dir / 'drop.sql'

        with connection.cursor() as cursor:
            try:

                # db.sql # Create
                if create_db:
                    self.stdout.write("Criando a base de dados...")
                    self.execute_sql_file(cursor, db_sql_path) 

                    self.create_migrations()
                    self.stdout.write(self.style.SUCCESS("Base de dados criada com sucesso."))
                    return
                
                # drop.sql # Drop
                if drop_db:
                    self.stdout.write("Deletando a base de dados...")
                    self.execute_sql_file(cursor, db_sql_drop_path) 
                    
                    self.drop_migrations()
                    self.stdout.write(self.style.SUCCESS("Base de dados PostgreSQL deletada com sucesso."))

                    db = get_mongo_db()
                    for collection_name in collections['name']:
                        if collection_name in db.list_collection_names():
                            db[collection_name].drop()
                            self.stdout.write(self.style.SUCCESS(f"Coleção '{collection_name}' deletada do MongoDB."))
                        else:
                            self.stdout.write(f"Coleção '{collection_name}' não encontrada no MongoDB.")
                    self.stdout.write(self.style.SUCCESS("Coleções MongoDB deletadas com sucesso."))
                    return
            
                # File
                if sql_file:
                    file_path = base_dir / sql_file
                    if os.path.isfile(file_path):
                        self.execute_sql_file(cursor, file_path)
                        self.stdout.write(self.style.SUCCESS(f"Executado o arquivo: {file_path}"))
                    else:
                        self.stdout.write(self.style.ERROR(f"Arquivo {sql_file} não encontrado."))
                # Default
                else:
                    self.create_migrations()
                    #db.sql
                    if db_sql_path.is_file():
                        self.execute_sql_file(cursor, db_sql_path)
                        self.stdout.write(self.style.SUCCESS("Executado o arquivo db.sql"))
                    #databese/*.sql
                    for sql_file in sorted(base_dir.glob("*.sql")):
                        if sql_file != db_sql_path and sql_file != db_sql_drop_path:
                            self.execute_sql_file(cursor, sql_file)
                            self.stdout.write(self.style.SUCCESS(f"Executado o arquivo: {sql_file}"))

                    #database/functions/*.sql
                    for sql_file in sorted(functions_dir.glob("*.sql")):
                        self.execute_sql_file(cursor, sql_file)
                        self.stdout.write(self.style.SUCCESS(f"Executado o arquivo: {sql_file}"))
                    
                    #database/materialized_views/*.sql
                    for sql_file in sorted((base_dir / 'materialized_views').glob("*.sql")):
                        self.execute_sql_file(cursor, sql_file)
                        self.stdout.write(self.style.SUCCESS(f"Executado o arquivo: {sql_file}"))
                    
                    #database/triggers/*.sql
                    for sql_file in sorted((base_dir / 'triggers').glob("*.sql")):
                        self.execute_sql_file(cursor, sql_file)
                        self.stdout.write(self.style.SUCCESS(f"Executado o arquivo: {sql_file}"))
                    
                    #database/views/*.sql
                    for sql_file in sorted(views_dir.glob("*.sql")):
                        self.execute_sql_file(cursor, sql_file)
                        self.stdout.write(self.style.SUCCESS(f"Executado o arquivo: {sql_file}"))
                    
                    #database/procedures/*.sql
                    for sql_file in sorted(procedures_dir.glob("*.sql")):
                        self.execute_sql_file(cursor, sql_file)
                        self.stdout.write(self.style.SUCCESS(f"Executado o arquivo: {sql_file}"))

                    db = get_mongo_db()

                    for collection in collections:
                        collection_name = collection["name"]
                        validator = collection["validator"]
                        
                        if collection_name not in db.list_collection_names():
                            db.create_collection(collection_name)
                            db.command({
                                "collMod": collection_name,
                                "validator": validator,
                                "validationLevel": "strict" 
                            })
                            self.stdout.write(self.style.SUCCESS(f"Coleção '{collection_name}' criada com sucesso com schema validator."))
                        else:
                            self.stdout.write(f"Coleção '{collection_name}' já existe.")

                    

                connection.commit()
                self.stdout.write(self.style.SUCCESS("Todos os scripts SQL executados com sucesso."))

            except Exception as e:
                self.stdout.write(self.style.ERROR(f"Ocorreu um erro: {e}"))
                connection.rollback()

    def execute_sql_file(self, cursor, file_path):
        """Lê e executa um arquivo SQL"""
        with open(file_path, 'r') as file:
            sql = file.read()
        cursor.execute(sql)

    def drop_migrations(self):
        """Deleta todas as migrações"""
        for app in apps.get_app_configs():
            try:
                call_command('migrate', app.label, 'zero', stdout=io.StringIO(), stderr=io.StringIO())
            except:
                pass
        self.stdout.write(self.style.SUCCESS("Migrações deletadas com sucesso."))
        
    def create_migrations(self):
        """Cria todas as migrações"""
        call_command('migrate', stdout=io.StringIO(), stderr=io.StringIO())
        self.stdout.write(self.style.SUCCESS("Migrações criadas com sucesso."))
        

