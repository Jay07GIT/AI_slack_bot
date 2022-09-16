#!/usr/bin/env bash
cd ~/aislackbot
docker-compose down
/Users/ar051/miniconda3/envs/aislackbot/bin/python /Users/ar051/Documents/Work/AI_slack_bot/model/model.py
docker-compose build --no-cache
docker-compose up -d