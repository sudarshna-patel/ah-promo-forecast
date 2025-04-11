#!/bin/bash

# Build the image
docker build -t promo-forecast-app .

# Run the container with memory limit and volume mount
docker run --rm --memory="5g" --name promo-forecast-app-container -p 8080:8080 -p 8000:8000 promo-forecast-app

