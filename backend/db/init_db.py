import os
import logging

from alembic.config import Config, main
from alembic import command

from ..core.config import settings


def migrate() -> None:
    logging.info('Auto Migrate Head Start!')
    alembic_conf = Config(os.path.join(settings.ROOT_DIR), 'alembic.ini')
    command.upgrade(alembic_conf, 'head')
    logging.info('Auto Migrate Completed!')
