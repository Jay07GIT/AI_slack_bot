#!/usr/bin/env bash
cd ~/<>
docker-compose down
/Users/<>/miniconda3/envs/<>/bin/python /Users/<>/Documents/Projects/demo/<>/model/model.py
docker-compose build --no-cache
docker-compose up -d