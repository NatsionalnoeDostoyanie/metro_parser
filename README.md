# The Metro Parser
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Imports: isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336)](https://pycqa.github.io/isort/)
[![python](https://img.shields.io/badge/Python-3.12-3776AB.svg?style=flat&logo=python&logoColor=white)](https://www.python.org)

## Table of Contents
- [Set up and run](#set-up-and-run)

## Set up and run
**You must have `poetry` installed in your OS:**
```bash
make install-main
make run
```

**If you don't have `poetry`:**
```bash
python3 -m venv .venv

# Linux:
source .venv/bin/activate

# Windows:
.venv\Scripts\activate

pip install -r requirements/main.txt

python3 metro_parser/main.py
```