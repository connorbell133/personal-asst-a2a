"""
This module contains the logger for the project.

Args:
    None

Returns:
    logger: The logger for the project.
"""

import logging

logging.basicConfig(
    level=logging.DEBUG, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)
