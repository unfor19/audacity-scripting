# audacity-scripting

> **IMPORTANT**: This is still a Work In Progress (WIP), some features might not be stable.

[![PyPI](https://img.shields.io/pypi/v/audacity-scripting?label=PyPi)](https://pypi.org/project/audacity-scripting)

A Python package for automating Audacity tasks based on [Audacity's Scripting Reference](https://manual.audacityteam.org/man/scripting_reference.html).

https://github.com/unfor19/audacity-scripting/assets/15122452/080e772c-3e40-424b-87ce-c2ac0dd75570

> Music by Sergio Prosvirini from Pixabay

## Requirements

- Install [Python 3.9+](https://www.python.org/downloads/)
- Install [Audacity 3.4.2+](https://www.audacityteam.org/download/)
- Audacity - Enable [mod-script-pipe](https://manual.audacityteam.org/man/scripting.html)
  - Run Audacity
  - Go into Edit > Preferences > Modules
  - Choose mod-script-pipe (which should show New) and change that to Enabled.
  - Restart Audacity
  - Check that it now does show Enabled.
  - This establishes that Audacity is finding mod-script pipe and that the version is compatible.

## Installation

Supported OS: Windows, Linux, and macOS

```
python -m pip install audacity-scripting
```

## Features

- [x] Remove spaces between clips - Removes spaces in all tracks for a given project absolute path `/path/to/my_project.aup3`
- [x] Add labels to clips
- [ ] Clean silence
- [ ] Normalize audio
- [ ] End Goal - Prepare videos for voice-clone-finetuning-vits

<!-- available_commands_end -->

## Getting Started

All the commands assume that the _Audacity_ application is up and running; That is mandatory as we communicate with [_Audacity_'s pipe](https://manual.audacityteam.org/man/scripting.html) to execute all the commands.

> **NOTE**: See the [GitHub Actions Tests Workflow](https://github.com/unfor19/audacity-scripting/actions/workflows/test.yml) to check it in action.

### Available Commands

Auto-generated by [unfor19/replacer-action](https://github.com/marketplace/actions/replacer-action); see [readme.yml](https://github.com/unfor19/audacity-scripting/blob/master/.github/workflows/readme.yml)

<!-- available_commands_start -->

```
Usage: audacity-scripting [OPTIONS] COMMAND [ARGS]...

  No confirmation prompts

Options:
  -ci, --ci  Use this flag to avoid confirmation prompts
  --help     Show this message and exit.

Commands:
  add-labels     Alias: al Add labels to clips in a given project
  clean-spaces   Alias: cs Clean spaces between clips in a given project
  do-command     Alias: dc - Execute a raw command in Audacity
  testing        This is for testing purposes only
  version-print  Get the version from the version file.
```

### Remove spaces between clips

This command copies the original file and removes spaces (gaps) between audio clips from the copied file.

```bash
audacity_scripting clean-spaces --file_path "/path/to/my_project.aup3"
```

### Send a command to Audacity

Send a command to Audacity according to [Audacity's Scripting Reference](https://manual.audacityteam.org/man/scripting_reference.html).

```bash
audacity_scripting do-command --command "Select: Tracks=0.0 Start=0.0 End=0.0"
```

## Known Issues

- macOS prints Audacity's server logs (`Server sending`, `Read failed on fifo, quitting`, etc.) - documented in [JOURNEY.md](./JOURNEY.md)

## References

- [GitHub Issue - Audacity Remove spaces between clips](https://github.com/audacity/audacity/issues/3924)
- [SourceForge Issue - Audacity pipes](https://sourceforge.net/p/audacity/mailman/audacity-devel/thread/CAJhgUZ1DOvHMie7KHJ45EuDztw-8WJM8Qd0d%2BNfkQaEje%3D-7Lg%40mail.gmail.com/)
- [GitHub Actions Windows Pipes Discussion](https://github.com/orgs/community/discussions/40540)
- [Audacity pipes issue on Windows](https://forum.audacityteam.org/t/different-errors-running-pipe-test/65305/40)
- [Python and Windows named pipes on Stackoverflow](https://stackoverflow.com/questions/48542644/python-and-windows-named-pipes)

## Authors

Created and maintained by [Meir Gabay](https://github.com/unfor19)

## License

This project is licensed under the MIT License - see the [LICENSE](https://github.com/unfor19/audacity-scripting/blob/main/LICENSE) file for details
