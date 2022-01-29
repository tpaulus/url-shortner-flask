# Flask URL Shortener
Flask version of URL Shortener

# Running Locally

Initialize the DB Via
```commandline
docker-compose exec web python3 -c "from app import db; db.create_all(); print('DB Tables Created')"
```



# Requirements
A short URL:
-   Has one long URL
-   This URL shortener should have a well-defined API for URLs created, including analytics of usage.
-   No duplicate URLs are allowed to be created.
-   Short links can expire at a future time or can live forever.

Your solution must support:
-   Generating a short url from a long url
-   Redirecting a short url to a long url.
-   List the number of times a short url has been accessed in the last 24 hours, past week, and all time.
-   Data persistence ( must survive computer restarts)
-   Metrics and/or logging: Implement metrics or logging for the purposes of troubleshooting and alerting. This is optional.
-   Short links can be deleted

Project Requirements:
-   This project should be able to be runnable locally with some simple instructions
-   This project's documentation should include build and deploy instruction
-   Tests should be provided and able to be executed locally or within a test environment.