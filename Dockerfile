# Use an official Python runtime as a parent image
FROM python:3.12

LABEL maintainer="Franco Piergallini Guida <francopierguida@gmail.com>"

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    DEBIAN_FRONTEND=noninteractive

# Install system dependencies and clean up in a single layer
RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get -qq install -y --no-install-recommends \
    libgeos-dev \
    libgl1 \
    libglib2.0-0 \
    supervisor && \
    apt-get clean && \
    rm -rf /tmp/* /var/tmp/* /var/lib/apt/lists/*

# Set the working directory
RUN mkdir /app/

WORKDIR /app/


# Copy the current directory contents into the container
COPY . .


# Install required Python packages
COPY ./requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir pip -U && \
    pip install --no-cache-dir -r requirements.txt


# Expose port 8000 for FastAPI
EXPOSE 8000

# Command to run the FastAPI application
CMD ["fastapi", "run", "app/main.py", "--port", "80"]
