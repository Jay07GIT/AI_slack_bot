#!/usr/bin/env bash
cd ~//Documents/Projects/demo/AI_slack_bot/aislackbot
docker-compose down
/Users/jvelku299/miniconda3/envs/aislackbot/bin/python /Users/jvelku299/Documents/Projects/demo/AI_slack_bot/aislackbot/model/model.py
docker-compose build --no-cache
docker-compose up -d