#!/bin/sh
git pull
python update.py
git commit -m "update framework.md" -a
git push
