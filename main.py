import dotenv
from src.logging_setup import setup_logging


if __name__ == '__main__':
    dotenv.load_dotenv()
    setup_logging()
