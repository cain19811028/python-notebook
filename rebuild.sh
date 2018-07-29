#!/bin/sh
git pull
python build.py
git commit -m "rebuild latest github repo info" -a
git push origin
