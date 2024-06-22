# Development

Make sure development happens in the `dev` branch, keeping the `main` branch for stable releases.

For git workflow, make linear commits on a seperate branch based off of `dev`. Before pushing changes, make sure to pull changes with

```bash
git stash # stash away current changes
git pull origin dev -r
git stash apply # un-stash changes
```

Then, push the commits with:

```bash
git push origin [branch] --force-with-lease
```

If a PR is waiting and got out of date, repeat the same steps above, or simply select "Rebase branch" on the Github website.

For PR merging, we use the "Squash and merge" option.

## Setup

Ask @menamerai for the environment secrets, then create a file on root called `.env` and write the secrets in.

Either use the provided devcontainer, or make sure that you have virtual environment installed with Python >=3.10 and Poetry.

To install dependencies:

```bash
poetry install
```

To set up pre-commit hooks and make sure the syntaxes are consistent:

```bash
poetry run pre-commit install
```

It might take a while for black and isort to be installed on your first commit.

Remember to execute all code-related commands with `poetry run [command]`, or spawn a poetry shell with:

```bash
poetry shell
```

Make sure the database is initialized with:

```bash
python init_database.py
```

The bot can be executed with:

```bash
python run_bot.py
```

## Structure

For every functionality that is added in the `hazel` directory, make sure to create corresponding tests in `tests`. To check if the test passed, we can run

```bash
poetry run pytest
```