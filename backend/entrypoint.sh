#!/bin/bash
echo $ENV_CONFIG | base64 --decode - >> ./env/.env
python3 app/main.py