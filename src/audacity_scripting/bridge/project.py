from .pipe import do_command
import time
from ..utils.logger import logger


def open_project(file_path):
    return do_command(f'OpenProject2: Filename={file_path}')


def save_project():
    return do_command(f'SaveProject2:')


def save_project_as(file_path):
    return do_command(f'SaveProject2: Filename={file_path}')


def save_project_changes(new_file_path, sleep_seconds=0.01):
    logger.info("Saving project ...")
    if new_file_path:
        save_project_as(new_file_path)
    else:
        save_project()
    time.sleep(sleep_seconds)
    logger.info("Completed saving project")
