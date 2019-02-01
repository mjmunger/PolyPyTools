#!/usr/bin/env bash
if [ $# -ne 1 ]; then
    echo "Usage: ./publish-update.sh <version>"
    exit 1
fi
python3 -m pip install --user --upgrade setuptools wheel
python3 setup.py sdist bdist_wheel
python3 -m pip install --user --upgrade twine
python3 -m twine upload dist/*$1*