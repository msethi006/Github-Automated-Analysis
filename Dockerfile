# Base image
FROM ubuntu:20.04
FROM python:3.8

# Set the working directory
WORKDIR /app

# Install Python and required dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends 



# Install Python packages
RUN pip3 install GitPython langchain gpt-index python-git streamlit transformers



COPY app.py getRepos.py model.py repoPreprocessing.py /app/

# Expose the port your Streamlit app will run on (8501 by default)
EXPOSE 8501

# Command to run the Streamlit app
CMD ["streamlit", "run", "app.py"]

