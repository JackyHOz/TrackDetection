#!/bin/bash
. venv/bin/activate
venv/bin/pip3 install --upgrade pip
venv/bin/pip3 install -r requirements.txt
python3 stream.py