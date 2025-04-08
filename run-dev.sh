#!/bin/bash
# podman run --rm -p 5000:5000 -p 8000:8000 -v $(pwd)/:/app/ promo-forecast-app

podman run --rm -p 5000:5000 -p 8000:8000 -p 6379:6379 -v %cd%:/app promo-forecast-app
