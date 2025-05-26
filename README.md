# Weekend Project
## Introduction
This is a custom journaling app that I wrote in the span of a weekend. I did some basic scaffolding before my four-day Memorial Weekend, but the bulk of the work was done Friday and Saturday (with light commits Sunday and Monday during testing). 

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
* You can view past journals
* It has a Signal integration, meaning you can message the app things to journal about throughout the day and it'll display the messages when you sent them ("blurbs!")
* It sends your journals to a local LLM and automatically titles them

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
