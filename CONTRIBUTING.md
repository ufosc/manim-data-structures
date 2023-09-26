# Contributing Guidelines
The general workflow for contributing to this project is as follows:
1. Create a new branch for your contribution.
2. Make sure your branch is up-to-date `git pull upstream main`
3. Make your changes.
4. Update the documentation, tests, and changelog if necessary.
5. Push your changes to your fork.
6. Submit a pull request through [GitHub](https://github.com/ufosc/manim-data-structures/pulls).

## Setup
To interact with the project, you will need to install some dependencies and configure git.

1. [Install git](https://git-scm.com/)
2. [Install Manim dependencies](https://docs.manim.community/en/stable/installation.html#installing-manim-locally)
   - Note: You do not need to install Manim itself (Poetry will handle that).
3. [Install Poetry](https://python-poetry.org/docs/master/#installing-with-the-official-installer)
4. Fork the [project](https://github.com/ufosc/manim-data-structures).
5. Clone your fork `git clone <my-fork-url>`.
6. Add the upstream repository. `git remote add upstream https://github.com/ufosc/manim-data-structures/`
7. Install project dependencies. `poetry install`
8. Install Pre-Commit. `poetry run pre-commit install`
9. Ensure that the poetry virutal environment is loaded by running `poetry shell` (some IDEs have a setting to do so automatically).

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
