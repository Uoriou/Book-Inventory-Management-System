# Use official Python image
FROM python:3.11

# Set working directory in container
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the project files
COPY . .

# Make entrypoint script executable
RUN chmod +x ./entrypoint.sh

# Use entrypoint script to run migrations and start server
ENTRYPOINT ["./entrypoint.sh"]

