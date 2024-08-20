#import logger
import logging
from dotenv import load_dotenv
from utils.environment import check_env_vars
from lib.generate import run
import click

load_dotenv()

logging.basicConfig(level=logging.INFO, format='%(levelname)s - %(asctime)s - %(name)s - %(message)s')
logger = logging.getLogger(__name__)

@click.command()
@click.option('--context', default='./', help='Context directory')
@click.help_option('--help', '-h')

def main(context):
    logger.info("Starting... 🚀")
    check_env_vars()
    run(context)

if __name__ == '__main__':
    main()
