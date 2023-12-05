#!/bin/bash
git pull
docker stop perfect_north_emailer
docker container rm perfect_north_emailer
docker build -t perfect_north_emailer .
