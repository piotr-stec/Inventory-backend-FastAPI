import logging
from src.config import Settings
from src.database.core import create_db, check_all_tables

settings = Settings()

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG, format='%(message)s')



def _create_all_tables_if_needed():
    if not all(check_all_tables()):
        logger.info("Creating tables")
        create_db()
        logger.info("All tables created")
    else:
        logger.info("All tables exists. Nothing to do")