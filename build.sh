#!/usr/bin/env bash
rm -rf build dist spot2mp3.egg-info
python3 setup.py sdist bdist_wheel
pip install .