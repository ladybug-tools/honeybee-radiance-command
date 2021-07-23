[![Build Status](https://travis-ci.com/ladybug-tools/honeybee-radiance-command.svg?branch=master)](https://travis-ci.com/ladybug-tools/honeybee-radiance-command)
[![Coverage Status](https://coveralls.io/repos/github/ladybug-tools/honeybee-radiance-command/badge.svg?branch=master)](https://coveralls.io/github/ladybug-tools/honeybee-radiance-command)

[![Python 3.7](https://img.shields.io/badge/python-3.7-blue.svg)](https://www.python.org/downloads/release/python-370/) [![Python 2.7](https://img.shields.io/badge/python-2.7-green.svg)](https://www.python.org/downloads/release/python-270/) [![IronPython](https://img.shields.io/badge/ironpython-2.7-red.svg)](https://github.com/IronLanguages/ironpython2/releases/tag/ipy-2.7.8/)

# honeybee-radiance-command

Python wrapper around Radiance commands, used by [honeybee-radiance](https://www.ladybug.tools/honeybee-radiance/docs/).

## Installation

```console
pip install -U honeybee-radiance-command
```

## QuickStart

```python
import honeybee_radiance_command

```

## [API Documentation](http://ladybug-tools.github.io/honeybee-radiance-command/docs)

## Local Development

1. Clone this repo locally
```console
git clone git@github.com:ladybug-tools/honeybee-radiance-command

# or

git clone https://github.com/ladybug-tools/honeybee-radiance-command
```
2. Install dependencies:
```console
cd honeybee-radiance-command
pip install -r dev-requirements.txt
```

3. Run Tests:
```console
python -m pytests tests/
```

4. Generate Documentation:
```console
sphinx-apidoc -f -e -d 4 -o ./docs ./honeybee_radiance_command
sphinx-build -b html ./docs ./docs/_build/docs
```