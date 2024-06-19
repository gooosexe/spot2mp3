#!/usr/bin/env bash
rm -rf build dist spot2mp3.egg-info
python setup.py sdist bdist_wheel
pip install .