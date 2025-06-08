# Weekend Project - Example Journaling App
## Introduction
This is a custom journaling app that I wrote in the span of a weekend. I did some basic scaffolding before my four-day Memorial Weekend, but the bulk of the work was done Friday and Saturday (with light commits Sunday and Monday during testing). This app was primarily written just to keep my python/django skills sharp while I'm not using them in my professional life - not neccessarily for the app's usefulness itself.

This app is trying to solve the following problems:
* Journals should always be private, and never sent off the computer this project runs on.
* Journals can benefit from AI analysis, and, that AI processessing should be done with local models on consumer-grade hardware  (I bought an Arc B280 for this project).
* Journals should be long-lasting

## Future Development
When I'm ready for the next iteration of this project, I'm hoping to incorporate the following:
* A goals journal. My hope is that the user should have monthly goals, yearly goals, and tri-yearly goals. If you write a journal, AI should scan the journal for references to goals and then link them.
* Feedback. I think it'd be interesting if after your journal is written, the AI gives you some suggestions for things to do the next day.
* Better sentiment analysis.
* Trends. It'd be interesting to see the AI sus out things that you journaled about and track how those topics either faded or didn't fade over time.

## Current Features
Right now, the journal app does a few things:
* You can create a journal
![image](https://github.com/user-attachments/assets/a7c55860-12fe-4b95-9d73-4abe3de6456a)
* You can view past journals
![image](https://github.com/user-attachments/assets/a03b01f2-51bb-497b-9b1e-db6083708c51)

_Note: These journals are example journals I had AI write with the prompt about being a drone operator in a bureaucratic organization._

* It has a Signal integration, meaning you can message the app things to journal about throughout the day and it'll display the messages when you sent them ("blurbs!")
![image](https://github.com/user-attachments/assets/4bcfda9b-b021-47f6-9cf5-b29a29dcbbe8)

* It sends your journals to a local LLM and automatically titles them. Also does mood extraction.
![image](https://github.com/user-attachments/assets/1125ad32-75e8-4ef6-ad44-16faed0e2844)
_Note: The Title and Mood tags are completely AI generated_

* Weekly Summaries - At the end of every week, AI reviews your journal and provides you a weekly summary.
![image](https://github.com/user-attachments/assets/6ddf8922-3c92-4f9c-b7ab-b71ac51638fa)

* You can even ask your journals a question using AI.
![image](https://github.com/user-attachments/assets/5d35288c-ffaf-4859-9447-5c80c5b73d8f)

* And it will give you a response formatted from Markdown!
![image](https://github.com/user-attachments/assets/27730138-17e4-4683-92a9-ac52eef60cef)


## Installation and Usage Instructions
### Getting the Ollama API running
#### If you have an Intel GPU
The docker compose incorporates an ollama-intel docker container. If you are using an Intel GPU, it should pretty much work out of the box.

#### If you have a Nvidia GPU
NVIDIA users have it the easiest, I recommend checking out [this article](https://gist.github.com/usrbinkat/de44facc683f954bf0cca6c87e2f9f88) as it should give you some helpful information on how to set up the compose.
The broad strokes: You'll need to get an ollama API endpoint listening with the container name ollama-api on the port xxxxx. From there, the application during initialization should do all of the heavy lifting for you. By default, it'll grab Deepseek's r1-14b.

### Setting your .env file
The docker compose references an env file. In the repository, the one that's included has all the ENV values you need, however, you'll need to set them yourself. The following values are required:
* `SECRET_KEY`: The value of the secret key for the Django webapp. Should be set to a random 64 hexadecimal value.
* `SIGNAL_NUMBER`: The value of the phone number (including area code) you intend to use for Signal (blurb integration). Example value: +12024566213
* `WEBAPP_USERNAME`: The value of the username you intend to use for your journaling. The blurb integration will attach your blurbs to this user.

### Provisioning the database
The database, by default, is created when the docker container is built and stored in the docker container. The database is initially populated with the username `joe` and password `testuser`. If you get an error similar to "Are you trying to mount a file on a folder or vice versa?" from docker, run the following commands:
```bash
docker compose down
rm -r .data/db.sqlite3
touch .data/db.dqlite3
docker compose up -d
docker cp django-docker:/app/sqlite3_init ./.data/db.sqlite3_init
docker compose down
mv ./.data/db.sqlite3_init ./.data/db.sqlite3
```
You should then be able to run the webapp, no problem. Note that the AI integration may not work for a little while - it'll automatically queue the downloading of the deepseek model after the first journal is written.
