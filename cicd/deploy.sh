#!/bin/bash
docker tag diabetes-classifier-streamlit-app:latest registry.digitalocean.com/streamlit-apps/diabetes-classifier-streamlit-app:latest

docker push registry.digitalocean.com/streamlit-apps/diabetes-classifier-streamlit-app:latest 