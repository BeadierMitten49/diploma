import dotenv
dotenv.load_dotenv()
from src.logging_setup import setup_logging
from src.infrastructure.database.database_setup import init_db


if __name__ == '__main__':
    setup_logging()
    init_db()
