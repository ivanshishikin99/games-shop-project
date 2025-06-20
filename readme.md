#Alembic autorevision

alembic revision --autogenerate

#Initializing postgres, maildev and rabbitmq

docker compose up -d pg maildev rabbitmq

#Initializing taskiq workers.

taskiq worker core:broker --fs-discover --tasks-pattern "**/tasks"

#If poetry stops working

python -m pip install requests-toolbelt 

