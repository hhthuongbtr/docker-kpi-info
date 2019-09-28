## How to deploy

Build the containers

`$ docker-compose up --build`

The database may fail to connect, restart the containers to fix it.

Show list of containers

`$ docker ps`

Log directory is `kpi_info/data`

Connect to the python container to migrate and update database

`$ docker exec -it <container> bash`

`# python manage.py makemigrations`

`# python manage.py migrate`

`# python manage.py updatedb`

## Todo

Need clean up
