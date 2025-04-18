import os

from dotenv import load_dotenv

load_dotenv()
print(f"Loaded DB Host: {os.getenv('REST_API_DB_HOST')}")

__DB_BASE_HOST = f"{os.getenv('REST_API_DB_HOST')}:{os.getenv('REST_API_DB_PORT')}"
__DB_CREDENTIALS = f"{os.getenv('REST_API_DB_LOGIN')}:{os.getenv('REST_API_DB_PASSWORD')}"
SQLALCHEMY_DATABASE_URI = f'postgresql://{__DB_CREDENTIALS}@{__DB_BASE_HOST}/{os.getenv("REST_API_DB_NAME")}'
SECRET_KEY = os.getenv("REST_API_SECRET_KEY")
LOCAL_TOKEN = os.getenv("REST_API_LOCAL_TOKEN")