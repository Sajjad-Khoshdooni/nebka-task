# Fund Core


## Install requirements
```
pip install -r requirements.txt
```

## Migratations
```
./manage.py migrate
```

## Run Server
Before  running server you need to set the environmental variables you can see the
`.env` file example in `.example.env` file.
```
./manage.py runserver
```

## Create Super User
```
./manage.py createsuperuser
```

## Run Celery Workers
```
celery -A _base beat -l info
celery -A _base worker -l info --queues=fund --concurrency=4
```

## Docs
```
http://127.0.0.1:8000/swagger/
http://127.0.0.1:8000/redoc/
```

## Recommendation

In order to improve the performance of the `FundListAPIView`, it is recommended to use Redis for caching the `FundsData`. By caching the data in Redis, you can reduce the number of database queries and speed up the response time for the API.
