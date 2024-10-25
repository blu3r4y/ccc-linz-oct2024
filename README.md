# 40th Classic Cloudflight Coding Contest

My solutions for the [40th Classic Cloudflight Coding Contest](https://codingcontest.org/) in October 2024, written in Python.

:goat: :goat: :goat:

## Challenges

- :heavy_check_mark: **[Level 1](data/Level%201.pdf)** - [Solution](/../level1/ccc/contest.py)
- :heavy_check_mark: **[Level 2](data/Level%202.pdf)** - [Solution](/../level2/ccc/contest.py)
- :heavy_check_mark: **[Level 3](data/Level%203.pdf)** - [Solution](/../level3/ccc/contest.py)
- :heavy_check_mark: **[Level 4](data/Level%204.pdf)** - [Solution](/../level4/ccc/contest.py)
- :x: **[Level 5](data/Level%205.pdf)** - *unfinished*

## Requirements

### Python >= 3.13

Package requirements are specified in the [pyproject.toml](pyproject.toml) file.

```sh
poetry install
```

Lint and format before commits.

```sh
ruff format
ruff check --select I --fix
```

## Snippets

Run code as a module

```sh
python -m ccc
```

Quickly archive the last commit

```sh
git archive --format zip -o code.zip HEAD
```
