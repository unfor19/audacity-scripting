from .pipe import do_command


def save_project():
    return do_command(f'SaveProject:')


def save_project_as(file_path):
    return do_command(f'SaveProject2: Filename={file_path}')


def open_project(file_path):
    return do_command(f'OpenProject2: Filename={file_path}')
