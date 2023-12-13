# audacity-scripting

A Python wrapper for the [Audacity Scripting Reference](https://manual.audacityteam.org/man/scripting_reference.html).

📣 **IMPORTANT**: Currently tested only macOS

## Requirements

- Install [Python 3.6+](https://www.python.org/downloads/)
- Install [Audacity](https://www.audacityteam.org/download/)
- Audacity - Enable [mod-script-pipe](https://manual.audacityteam.org/man/scripting.html)
  - Run Audacity
  - Go into Edit > Preferences > Modules
  - Choose mod-script-pipe (which should show New) and change that to Enabled.
  - Restart Audacity
  - Check that it now does show Enabled.
  - This establishes that Audacity is finding mod-script pipe, and that the version is compatible.

## Installation

```
pip install audacity-scripting
```

## Features

- [x] Remove spaces between clips - Removes spaces in all tracks for a given project absolute path `/path/to/my_project.aup3`
- [ ] Clean silence
- [ ] Normalize audio

## Available Commands

Auto-generated by [unfor19/replacer-action](https://github.com/marketplace/actions/replacer-action), see [readme.yml](https://github.com/unfor19/frigga/blob/master/.github/workflows/readme.yml)

<!-- available_commands_start -->

```
Usage: audacity_scripting [OPTIONS] COMMAND [ARGS]...

  No confirmation prompts

Options:
  -ci, --ci  Use this flag to avoid confirmation prompts
  --help     Show this message and exit.

Commands:
  clean-spaces  Alias: cs
  do-command    Alias: dc - Execute a raw command in Audacity
  testing       This is for testing purposes only
```

<!-- available_commands_end -->

## Getting Started

All the commands assume that the _Audacity_ application is up and running; That is mandatory as we communicate with [_Audacity_'s pipe](https://manual.audacityteam.org/man/scripting.html) to execute all the commands.

### Remove spaces between clips

```bash
audacity_scripting clean-spaces --path "/path/to/my_project.aup3"
```

### Send a command to Audacity

```bash
audacity_scripting do-command --command "Select: Track=0 Track=1"
```

## References

- Audacity pipes - [https://sourceforge.net/p/audacity/mailman/audacity-devel/thread/CAJhgUZ1DOvHMie7KHJ45EuDztw-8WJM8Qd0d%2BNfkQaEje%3D-7Lg%40mail.gmail.com/](https://sourceforge.net/p/audacity/mailman/audacity-devel/thread/CAJhgUZ1DOvHMie7KHJ45EuDztw-8WJM8Qd0d%2BNfkQaEje%3D-7Lg%40mail.gmail.com/)
- GitHub Actions Windows Pipes Discussion - [https://github.com/orgs/community/discussions/40540](https://github.com/orgs/community/discussions/40540)
- Audacity pipes issue on Windows - [https://forum.audacityteam.org/t/different-errors-running-pipe-test/65305/40](https://forum.audacityteam.org/t/different-errors-running-pipe-test/65305/40)

## Authors

Created and maintained by [Meir Gabay](https://github.com/unfor19)

## License

This project is licensed under the MIT License - see the [LICENSE](https://github.com/unfor19/audacity-scripting/blob/master/LICENSE) file for details
