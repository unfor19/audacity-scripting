# audacity-scripting

WIP: A Python package for managing Audacity programmatically with Python.

## Quick Start

To run the application, go ahead and use pip or Docker.

### pip

Requires Python v3.6 and above

```
$ pip install -U unfor19-appy

$ appy
Created the file: $HOME/python-project/meirg-ascii.txt
Insert your name: meir gabay

Hello Meir Gabay, here's the cat fact of the day:
Unlike humans, cats do not need to blink their eyes on a regular basis to keep their eyes lubricated.

$ cat $HOME/python-project/meirg-ascii.txt
```

### Docker

Requires [Docker](https://docs.docker.com/get-docker/)

```bash
$ docker run --rm -it unfor19/appy bash
$ (container) appy
Created the file: /app/meirg-ascii.txt
... # Same as above
$ (container) cat /app/meirg-ascii.txt
```

<details>

<summary>Expand/Collapse - contents of meirg-ascii.txt</summary>

```
........................................................................................................................
........................................................................................................................
........................................................................................................................
........................................................................................................................
........................................................................................................................
........................................................................................................................
........................................................................................................................
........................................................................................................................
........................................................................................................................
......................................................::!!!!!::::.......................................................
.................................................:!*$%@S#&$$$@@$%*%**!:.................................................
.............................................:!*@&&@$::::.........::!$@%!!:.............................................
...........................................!@&@%%:.....................::!*!:...........................................
.........................................*&#%:.............................::!!.........................................
.......................................!@&*:.................................:!::.......................................
.....................................:@$*.......................................:!:.....................................
....................................*#$:..........::::::........::::::.............:....................................
...................................$S*............!&&&&@:......:@&&&&*.............::...................................
..................................@#:.............!&&%&&$......%&&%@&*................:.................................
.................................$S!..............!&@%$&&!....!&&@%@&*................:.................................
................................%S!...............!&@$$@&@:...$&@$$@&*................:.................................
...............................!B&................!&@$&$&&*..*&&$&$@&*................::................................
...............................!&!................!&@$&@$&@::@&@$&$@&*.................:................................
...............................$&.................!&@$&&$@&%%&&$&&$@&*..................................................
...............................@#.................!&@$&&&$&&&&$@&&$@&*..................................................
...............................@@.................!&@$&&&$$&&@$&&&$@&*..................:...............................
...............................@&.................!&@$&@@&$@&$&@$&$@&*.................%!...............................
...............................%S:................!&@$&$!&@$$@&*%&$@&*................:S!...............................
...............................:B%................!&@$&$.%#$$#$.%&$@&*................%B:...............................
...............................:B#:...............!&@$&$.:$$$$!.%&$@&*................#@................................
................................&B$...............!&@$&$........%&$@&*...............$S:................................
................................:#S:..............!&@$&$........%&$@&*..............*B%.................................
.................................:S#:.............!&&$&$........%&$@&*.............!S@..................................
..................................!S&:............!&$%&$........%&%$&*............*S@...................................
...................................:&B$...........:!..:!........::..::..........:@B$....................................
.....................................%B@:......................................*#S*.....................................
......................................!##@!..................................!&S@:......................................
........................................*&S@*:.............................*@#$:........................................
..........................................!$SS&*:......................:!@&@%:..........................................
............................................:*@###$*!:...........:::!$&&@%:.............................................
................................................!%@$$@&&#&@@&@@$&##&$%!:................................................
......................................................:!!*%%%%*!!::.....................................................
........................................................................................................................
........................................................................................................................
........................................................................................................................
....................!!!!:.......!!!!:.....!!!!!!!!!!!!!.....:!!!!.....!!!!!!!!!!!:.........:!!!!!!!:....................
..................!&&$$%@!....!&$$$$$...*#@$@@@@@@@@@$&*..:$S$$$&:..!&&$$@@@@@@$%$%......!$$$$$$$$$$$:..................
.................:S#@*%%*@!..%B$*%%%@..!SB$%%*********@*..@BB*%*@!.:#B@*%%********$$...:$#%%%%%%%%%%%@:.................
.................!&@@%%%%*@:*B$*%%%%@..*#&$%%%SSSSSSS#$:..@##*%*@!.!@#@*%*SSSSS#*%!&:..&B@%%%SBSSS%%*@*.................
.................!&#@%%%%%*&B$*%%%%%@..*&@$%%%S&&&&&&%....@@&*%*@!.!&&@*%*#$$SBB*%!@!.!##$%%$&%@BBS##@:.................
.................!&@@%%%%%%%$*%%%%%%@..*&@$%%%$$$$$$$@*...@@&*%*@!.!&@@*%%@%%@#@%%!&:.*&&$%%$%:@####&$!.................
.................!&@@%%*&%*%%%!&$*%%@..*&&$%%*%%%%%%*@%...@@&*%*@!.!&@@*%%%%%%%%**$*..*&@$%%$#B#!%%%*$%.................
.................!&@@%%*BB$$$%&B@*%%@..*&@$%%%SBBBBB#%:...@@#*%*@!.!&@@*%*@&&%*%!&!...*&&$%%%BBS@@%%*$*.................
.................:#@@%%*BBBBS@#&@*%%@..*&&$%%%#####&$*%:..@@&*%*@!.!#@@*%*BBBB*%%%$...*#&$%%%SSSSS%%*$*.................
.................!&#@*%*&!!!::&@@*%%@..!S#$%%*******%*@*..@&S*%*@!.!&&@*%*@$BBS*%*$%..!BBS****%%%***%@:.................
.................:SB#@@@$....:S##$@@$..!BB&$@@@@@@@@@@&*..@BB$$$&:.:SB&$@@$.&BB&$@$&:..&BBB@$@$$@@@@%:..................
.................:SBBBS%:....:SBBBS%:..!BBBBBBBBBBBBB&*...@BBBB@!..:SBBBS%:.:SBBBB@!...:$#BBBBBBB#$!....................
..................:!!!:.......:!!!:.....:!!!!!!!!!!!!.....:!!!:.....:!!!:....:!!!:........:!!!!!:.......................
........................................................................................................................
........................................................................................................................
........................................................................................................................
........................................................................................................................
........................................................................................................................
........................................................................................................................
........................................................................................................................
........................................................................................................................
........................................................................................................................
```

</details>

## References

- [packaging python](https://packaging.python.org/tutorials/packaging-projects/)
- [python-packaging-tutorial](https://python-packaging-tutorial.readthedocs.io/en/latest/setup_py.html)
- [python sample project](https://github.com/pypa/sampleproject)
- [setuptools package discovery](https://setuptools.readthedocs.io/en/latest/userguide/package_discovery.html)

## Authors

Created and maintained by [Meir Gabay](https://github.com/unfor19)
