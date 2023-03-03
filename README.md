# Tensorflow Certificate

This repo contains a core preparation of relevant components for the tensorflow certificate. This repo is based on https://github.com/https-deeplearning-ai/tensorflow-1-public.

## Local Setup

The dependencies are managed with poetry. An installation can be done as follows:

```bash
# installing pyenv if needed
brew install pyenv

# installing Python 3.8.0
pyenv install -s 3.8.0

# install poetry if needed
brew install poetry

# ensure .venv will be created within project dir
poetry config virtualenvs.in-project true

# using Python 3.8.0 for poetry
poetry env use 3.8.0

# install all dependencies based on poetry.lock
poetry install
```


## Conventional Commits

`commit -m  "Tag MESSAGE"`

`commit -m "feat added linear regression to toolstack"`

| Type              | Content                         |
| ----------------- | ---------------------------- |
| fix               | Patches a bug in the codebase. |
| feat              | Introduces a new feature to the codebase.  |
| test              | Adding missing tests or correcting existing tests. |
| docs              | Adds, updates or revises documentation that is stored in the repository. |
| ops               | Changes that affect operational components, like infrastructure, deployment, backup,  |
| refactor          | Refactoring existing code in the product, but without altering or changing existing behaviour in the product.  |
| build             | Changes that affect build components or external dependencies, like build tool, ci pipeline, project version. |
| perf              | Code changes that improves the performance or general execution time of the product but does not fundamentally change an existing feature.  |
| chore             | Includes a technical or preventative maintenance task that is necessary for managing the product or the repository, but it is not tied to any specific feature or user story e.g., modifying gitignore. |
| style             | Changes, that do not affect the meaning of the code (white-spaces, formatting, missing semi-colons etc.)  |
| revert            | Reverts one or more commits that were previously included in the product, but accidentally merged or serious issues were discovered that required their removal. |
