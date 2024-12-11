# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Copy the env file to the container
COPY .env /app/.env

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Define a volume for persisting the database
VOLUME ["/app/instance"]

# Make port 5000 available to the world outside this container
EXPOSE 5000

# Run the entrypoint script when the container launches
CMD ["/app/entrypoint.sh"]