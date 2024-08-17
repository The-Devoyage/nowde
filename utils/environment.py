import os
import sys
import logging

logger = logging.getLogger(__name__)

def check_env_vars():
    env_vars = [
        'GOOGLE_API_KEY',
    ]
    for var in env_vars:
        if var not in os.environ:
            logger.error(f"Environment variable not set: {var}")
            sys.exit(1)
