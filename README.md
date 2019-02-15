# smile

## Local project setup

Start a local Redis server.

### Backend
```
python3 -m venv smile-env
source smile-env/bin/activate
pip install -r requirements-normal.txt
python manage.py migrate
python manage.py runserver
```

### Frontend
```
yarn install
yarn run serve
```

## Local project setup with Docker

```
docker-compose -f docker-compose.dev.yml up
```

## Deployment to Heroku

Add PostgreSQL-Addon and Redis-Addon.

```
git push heroku master
heroku config:set DEBUG=0
heroku config:set SECRET_KEY=<long securely random string>
heroku run python manage.py migrate
heroku restart
```

## Deployment with Docker

Copy `env.example` to `.env` and adjust values.

```
docker-compose up --build
```

The server will listen by default on port 8000.


## Admin interface

There's an admin interface at `/admin/`. You can create admin users like this:

```
python manage.py createsuperuser
```

## Delete messages older than 24h

Messages older than 24h are not visible, but are still in the database.
To delete them, either click the button in the message admin interface or periodically run this command (e.g. with a cron job):

```
python manage.py delete_old_messages
```
