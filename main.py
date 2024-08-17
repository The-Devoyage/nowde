#import logger
import logging
from dotenv import load_dotenv
from utils.environment import check_env_vars
from lib.generate import run

load_dotenv()

logging.basicConfig(level=logging.INFO, format='%(levelname)s - %(asctime)s - %(name)s - %(message)s')
logger = logging.getLogger(__name__)

def main():
    logger.info("Starting... 🚀")
    check_env_vars()
    run()

if __name__ == '__main__':
    main()
