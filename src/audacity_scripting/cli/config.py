import click


class Config(object):
    def __init__(self):
        self.verbose = False
        self.errors = 0
        self.errors_msg = ""
        self.ci = False


pass_config = click.make_pass_decorator(Config, ensure=True)
