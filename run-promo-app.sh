#!/bin/bash

# Build the image
podman build -t promo-forecast-app .

# Run the container with memory limit and volume mount
podman run --rm --memory="5g" -p 5000:5000 -p 8000:8000 -v $(pwd):/app promo-forecast-app

# for windows
# podman run --rm -p 5000:5000 -p 8000:8000 -p 6379:6379 -v %cd%:/app promo-forecast-app
# podman run --rm --memory="5g" -p 5000:5000 -p 8000:8000 -v %cd%:/app promo-forecast-app

# set PYTHONPATH=%cd%

# podman build -t promo-forecast-app .
# podman run -p 8000:8000 -p 5000:5000 promo-forecast-app

# # dev
# podman run --rm -p 5000:5000 -p 8000:8000 -v %cd%:/app promo-forecast-app
# podman run --rm --memory="5g" -p 5000:5000 -p 8000:8000 -v %cd%:/app promo-forecast-app

