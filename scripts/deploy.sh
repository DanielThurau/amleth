#!/bin/bash

docker build -t amleth .

docker run -d \
  --name amleth \
  --env-file data/.env_prod \
  --restart always \
  -p 4000:80 \
  -v ~/code/amleth/data:/amleth/data \
  amleth
