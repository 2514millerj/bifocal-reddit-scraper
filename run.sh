#!/bin/bash

while read p; do
  export $p
done <.env

. venv/bin/activate
python app.py
