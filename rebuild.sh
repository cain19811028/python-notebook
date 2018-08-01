#!/bin/sh
git pull
python build.py
git commit -m "rebuild framework.md" -a
git push
