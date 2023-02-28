# Contributing Guidelines
The general workflow for contributing to this project is as follows:
1. Create a new branch for your contribution.
2. Make sure to `git pull upstream main`
2. Make your changes.
3. Update the documentation if necessary.
4. Push your changes to your fork.
5. Submit a pull request through [GitHub](https://github.com/ufosc/manim-data-structures/pulls).

## Setup
To interact with the project, you will need to install some dependencies and configure git.

1. [Install git](https://git-scm.com/)
2. [Install manim](https://docs.manim.community/en/stable/installation.html)
3. [Install Poetry](https://python-poetry.org/docs/master/#installing-with-the-official-installer)
4. Fork the [project](https://github.com/ufosc/manim-data-structures).
5. Clone your fork `git clone <my-fork-url>.
6. Add the upstream repository. `git remote add upstream https://github.com/ufosc/manim-data-structures/`
7. Install Pre-Commit:
`poetry run pre-commit install`

### Install git
For instructions see https://git-scm.com/.

### Fork the project
Go to https://github.com/ufosc/manim-data-structures and click the "fork" button.

### Clone your fork
```bash
git clone https://github.com/<your-username>/manim-data-structures.git
```
Once your fork is cloned, change the directory to enter the project folder:
```bash
cd manim-data-structures
```

### Add upstream repository
```bash
git remote add upstream https://github.com/ufosc/manim-data-structures.git
```
Now, `git remote -v` should show two remotes:
- `origin`: Your forked repository.
- `upstream`: The Manim Data Structures repository

### Package Install Dependencies
- Install [Poetry](https://python-poetry.org/) by following the instructions on this [link](https://python-poetry.org/docs/master/#installing-with-the-official-installer).
- Run `poetry install` inside the fork directory to install all dependencies. This command also creates a virtual environment which you can later enter by running `poetry shell` from within the forked directory.
- Install pre-commit by running `poetry run pre-commit install`. This ensures that each commit is properly formatted against the linters `black`, `flake8` and `isort`.

## Development

### Fetch the latest code from upstream
```bash
git checkout dev
git pull upstream dev
git push origin dev
```

### Initiate a PR
Once you have finalized your contribution, navigate to this [link](https://github.com/ufosc/manim-data-structures/pulls) to create a new pull request and submit it.

### Closing note
Once your PR is approved, it will be merged into the `dev` branch and we are looking at eventually merging upstream.

Thanks for contributing 😁!
