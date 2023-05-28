#!/bin/sh

docker-compose -f docker-compose.prod.yml down -v
docker-compose -f docker-compose.prod.yml up -d --build
docker-compose -f docker-compose.prod.yml exec web python manage.py makemigrations
docker-compose -f docker-compose.prod.yml exec web python manage.py migrate --noinput
docker-compose -f docker-compose.prod.yml exec web python manage.py collectstatic --no-input --clear
docker-compose -f docker-compose.prod.yml exec web python manage.py load_locations
docker-compose -f docker-compose.prod.yml exec web python manage.py create_cars
docker-compose -f docker-compose.prod.yml exec web python manage.py update_car_locations
