__all__ = ('send_welcome_email',
           )

import logging
import sys

from core.config import settings
from .welcome_email_notification import send_welcome_email

if sys.argv[0] == 'worker':
    logging.basicConfig(level=settings.logging_config.log_level_value,
                        format=settings.logging_config.log_format)