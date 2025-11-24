########### BACK-END
# Use the official Python runtime image
FROM python:3.13
# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
   PYTHONUNBUFFERED=1
# Set the working directory inside the container
WORKDIR /app
# Install system dependencies
RUN apt-get update && apt-get install -y \
   libpq-dev gcc --no-install-recommends && \
   apt-get clean && rm -rf /var/lib/apt/lists/*
# Upgrade pip and install dependencies
COPY backend/requirements.txt /app/
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt
# Copy project files into the container
COPY backend /app/
# Expose the port Django will run on
EXPOSE 8000
# Run the Django development server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]


########### FRONT-END
# Use the latest LTS version of Node.js
#FROM node:20-alpine
# Set the working directory inside the container
#WORKDIR /app
# Copy package.json and package-lock.json
#COPY package*.json ./
# Install dependencies
#RUN npm install
# Copy the rest of your application files
#COPY . .
# Expose the port your app runs on
#EXPOSE 3000
# Define the command to run your app
# CMD ["npm", "start"]