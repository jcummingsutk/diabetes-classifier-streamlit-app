FROM continuumio/miniconda3
WORKDIR /app
COPY ./conda.yaml ./
RUN conda env create -f conda.yaml
COPY st_app st_app
COPY config.yaml .
COPY config_secret.yaml .
SHELL ["conda", "run", "-n", "streamlit-review-chatter", "/bin/bash", "-c"]
CMD ["conda", "run", "-n", "streamlit-review-chatter", "python", "-m", "streamlit", "run", "st_app/app.py", "--server.port", "8000", "--server.address", "0.0.0.0"]