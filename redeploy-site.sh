#!/bin/bash

pkill -f tmux

cd mlh_portfolio_project
git fetch && git reset origin/main --hard
source python3-virtualenv/bin/activate
pip install -r requirements.txt

docker compose -f docker-compose.prod.yml down
docker compose -f docker-compose.prod.yml up -d --build
