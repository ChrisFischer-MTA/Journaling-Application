# Use the official Python runtime image
FROM python:3.13-slim
 
# Create the app directory
RUN mkdir /app
 
# Set the working directory inside the container
WORKDIR /app
 
# Set environment variables 
# Prevents Python from writing pyc files to disk
ENV PYTHONDONTWRITEBYTECODE=1
#Prevents Python from buffering stdout and stderr
ENV PYTHONUNBUFFERED=1 
 
# Upgrade pip
RUN pip install --upgrade pip 
 
# Copy the Django project  and install dependencies
COPY requirements.txt  /app/
 
# run this command to install all dependencies 
RUN pip install --no-cache-dir -r requirements.txt
 
# Copy the Django project to the container
COPY ./journal_project/ /app/
 
# Expose the Django port
EXPOSE 8000

# Journal App requires docker support
RUN apt-get update
RUN apt-get install cron curl -y 
RUN echo "* * * * * root python /app/get-blurbs.py" > /etc/cron.d/django-support-scripts
RUN echo '\n' >> /etc/cron.d/django-support-scripts
RUN chmod 0644 /etc/cron.d/django-support-scripts


RUN python manage.py makemigrations
RUN python manage.py migrate
RUN python create-test-data.py
RUN cp db.sqlite3 db.sqlite3_initial
 
# Run Django’s development server
CMD cron && python manage.py runserver 0.0.0.0:8000
#["python", "manage.py", "runserver", "0.0.0.0:8000"]
