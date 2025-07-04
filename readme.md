#Alembic autorevision

alembic revision --autogenerate

#Initializing postgres, maildev and rabbitmq

docker compose up -d pg maildev rabbitmq

#Initializing taskiq workers

taskiq worker core:broker --fs-discover --tasks-pattern "**/tasks"

#Initializing celery worker

celery -A tasks.celery:celery worker --loglevel=INFO --pool=solo

#Initializing celery flower

celery -A tasks.celery:celery flower

#If poetry stops working

python -m pip install requests-toolbelt 

