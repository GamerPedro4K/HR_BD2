import pymongo
from decouple import config

def get_mongo_connection_string():
    """
    Retorna a string de conexão do MongoDB usando as configurações do arquivo .env.
    """
    host = config('MONGO_HOST', default='localhost')
    port = config('MONGO_PORT', default='27017')
    username = config('MONGO_USER', default='')
    password = config('MONGO_PASSWORD', default='')
    db_name = config('MONGO_DATABASE_NAME', default='mongo')
    auth_source = config('MONGO_AUTH_SOURCE', default='admin')
    
    return f"mongodb://{username}:{password}@{host}:{port}/{db_name}?authSource={auth_source}"

def get_mongo_db():
    """
    Retorna a database do MongoDB usando a string de conexão.
    """
    connection_string = get_mongo_connection_string()
    try:
        client = pymongo.MongoClient(connection_string)
        return client[config('MONGO_DATABASE_NAME', default='mongo')]
    except Exception as e:
        print(f"Erro ao conectar ao MongoDB: {e}")
        return None
