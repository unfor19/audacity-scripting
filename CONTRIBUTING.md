## Contributing

This section assumes you've completed the [Requirements](https://github.com/unfor19/audacity-scripting?tab=readme-ov-file#requirements) section on the front page.

### Development Requirements

- macOS

  - Install [HomeBrew Package Manager](https://brew.sh/)
    ```bash
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
    ```
  - Install required packages with HomeBrew
    ```bash
    brew install make
    ```

- Windows

  - Install [Chocolatey Package Manager](https://chocolatey.org/install)
  - Install required packages with Choco

    **IMPORTANT:** Open a PowerShell window with elevated permissions (As Administrator)

    ```bash
    choco install -y make
    ```

From now on, we'll use `make` commands to develop and build this Python package locally.

1. [Fork](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/working-with-forks/fork-a-repo) this repository on GitHub
1. [Git clone](https://docs.github.com/en/repositories/creating-and-managing-repositories/cloning-a-repository) your forked repository
1. Prepare `.VENV` directory - This step also installs the latest version of `pip` and `wheel`
   ```bash
   make venv-prepare
   ```
1. **IMPORTANT**: The [Makefile](./Makefile) activates `.VENV` for any `venv-` target.
1. Install this package's development `requirements.txt` in `.VENV`
   ```bash
   make venv-install
   ```
1. Install this package in [edit mode](https://packaging.python.org/en/latest/guides/distributing-packages-using-setuptools/#working-in-development-mode)

   **IMPORTANT**: For any change in [./src/audacity_scripting/cli/](./src/audacity_scripting/cli/), it's best to re-run this command to update the CLI commands; see [Click Framework](https://click.palletsprojects.com/en/8.1.x/).

   ```bash
   make venv-install-edit
   ```

You can now start the development process!

### Development Process

1. Checkout to a new branch `feature/my-awesome-feature`
1. (Optional) Add a new Python package and update [./requirements.txt](./requirements.txt) accordingly
   ```bash
   make venv-install PACKAGE_NAME=click==8.1.7
   ```
   ```bash
   make venv-requirements-update
   ```
1. Add tests on your feature in [./tests](./tests); all tests are based on the [Python's unittest framework](https://docs.python.org/3/library/unittest.html)
1. Run tests - This wrapper command kills existing Audacity instances, cleans up test outputs, starts Audacity, and then starts the tests.
   ```bash
   make wrapper-run-test
   ```
1. Commit changes to your cloned fork
   ```bash
   git commit -am "added an awesome feature"
   ```
1. Create a GitHub Pull Request from your fork to the source repository.

#### Syncing with the "source" code

3. Add this repository as a "source" remote
   ```bash
   cd audacity-scripting
   ```

   ```bash
   git remote add source https://github.com/unfor19/audacity-scripting.git
   ```
1. Check git remotes
   ```bash
   git remote -v
   ```
   Assuming you are `willywonka`, here's the desired output:
   ```
   origin https://github.com/willywonka/audacity-scripting.git (fetch)
   origin https://github.com/willywonka/audacity-scripting.git (push)
   source https://github.com/unfor19/audacity-scripting.git (fetch)
   source https://github.com/unfor19/audacity-scripting.git (push)
   ```
1. To sync from `source` (this project's source repo) to your current branch, execute this command:
   ```bash
   git pull source main
   ```

> **NOTE**: Following that, you might need to handle some merge conflicts, but that's it; you're up-to-date with the latest version of the source code.
