import click

from ..bridge.pipe import do_command as _do_command
from .config import pass_config
from ..bridge.wrappers import remove_spaces_between_clips, open_project_copy
from ..utils.logger import logger
from ..utils.version import get_version


class AliasedGroup(click.Group):
    def get_command(self, ctx, cmd_name):
        app_aliases = {
            "c": "clean",
            "t": "testing",
            "r": "raw",
            "d": "do",
            "v": "version"
        }
        action_aliases = {
            "s": "spaces",
            "c": "command",
            "p": "print"
        }
        if len(cmd_name) == 2:
            words = []
            if cmd_name[0] in app_aliases:
                words.append(app_aliases[cmd_name[0]])
            if cmd_name[1] in action_aliases:
                words.append(action_aliases[cmd_name[1]])
            if len(words) == 2:
                cmd_name = "-".join(words)

        rv = click.Group.get_command(self, ctx, cmd_name)
        if rv is not None:
            return rv
        matches = [x for x in self.list_commands(ctx)
                   if x.startswith(cmd_name)]
        if not matches:
            return None
        elif len(matches) == 1:
            return click.Group.get_command(self, ctx, matches[0])
        ctx.fail(f"Too many matches: {', '.join(sorted(matches))}")


@click.command(cls=AliasedGroup)
@pass_config
@click.option(
    '--ci', '-ci',
    is_flag=True, help="Use this flag to avoid confirmation prompts"
)
def cli(config, ci):
    """No confirmation prompts"""
    config.ci = ci


@cli.command()
@click.option(
    '--file_path', '-p', required=True, show_default=False, type=str
)
def clean_spaces(file_path):
    """Alias: cs\n
    Clean spaces between clips in a given project\n
    File Path must be absolute
    """
    new_file_path = open_project_copy(file_path)
    logger.debug(new_file_path)
    result = remove_spaces_between_clips()
    if result:
        print(new_file_path)
    else:
        raise Exception("Failed to remove spaces between clips")


@cli.command()
@click.option(
    '--command', '-c', required=True, show_default=False, type=str
)
def do_command(command):
    """Alias: dc - Execute a raw command in Audacity\n
    Use this for reference - https://manual.audacityteam.org/man/scripting_reference.html\n
    Example:\n
    audacity_scripting do-command --command "Select: Track=0 Track=1"
    """
    response = _do_command(command)
    print(response)


@cli.command()
def version_print():
    """Get the version from the version file."""
    logger.info(get_version())


@cli.command()
def testing():
    """This is for testing purposes only"""
    logger.info("Testing")
