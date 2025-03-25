# Use the official Python 3.11.9 image as base
FROM python:3.11.9

# Set the working directory inside the container
WORKDIR /app

# Copy the necessary files
COPY app.py /app/app.py
COPY Python_3.11.9_requirements.txt /app/requirements.txt

# Install dependencies
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port Flask runs on
EXPOSE 5000

# Define environment variables
ENV CSV_DATABASE_PATH=/mnt/database/final_product_database_with_unique_names.csv

# Run the application
CMD ["python", "app.py"]
