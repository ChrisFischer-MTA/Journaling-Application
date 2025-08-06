LABEL unstable
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

# Journal App requires cron support. Instlal cron and create cron script.
RUN apt-get update
RUN apt-get install cron curl -y 
RUN echo "*/5 * * * * root /usr/local/bin/python /app/get-blurbs.py\n" > /etc/cron.d/django-support-scripts
RUN echo "25 * * * * root /usr/bin/flock -w 10 /tmp/ai-lockfile timeout -s SIGKILL 45m /usr/local/bin/python /app/get-ai-summaries.py" >> /etc/cron.d/django-support-scripts
RUN echo '\n' >> /etc/cron.d/django-support-scripts
RUN chmod 0644 /etc/cron.d/django-support-scripts

# Copy the Django project to the container
COPY ./journal_project/ /app/
 
# Expose the Django port
EXPOSE 8000

# Create our initial database
RUN python manage.py makemigrations
RUN python manage.py migrate
RUN python create-test-data.py
RUN cp db.sqlite3 db.sqlite3_initial

# We can't use a simple command entry point, because cron can't inference env variables
# My workaround for this is create a script, save a env file to root, then reference the variables
# in our cron script. 
RUN echo 'printenv >> /etc/enviroment' > /app/start.sh
RUN echo 'cron && python manage.py runserver 0.0.0.0:8000' >> /app/start.sh
RUN chmod +x /app/start.sh

# TODO: Working in a check to see if db.sqlite3 is a folder (docker by default will make this a folder if the file doesn't exist.
# We take advantage of this logic by detecting it being a folder, then overwriting with our test database!
# RUN echo 'if [ -d /app/db.sqlite3 ]; then rm -r /app/db.sqlite3; cp /app/db.sqlite3_initial db.sqlite3; fi'


# Run Django’s development server
CMD /app/start.sh
#cron && python manage.py runserver 0.0.0.0:8000
#["python", "manage.py", "runserver", "0.0.0.0:8000"]
