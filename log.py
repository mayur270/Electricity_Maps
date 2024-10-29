"""Log settings for reviewing or debugging purposes."""

import logging

from config import config

logger = logging.getLogger(__name__)
logging.basicConfig(
    level=config.LOGGING_LEVEL,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
)
