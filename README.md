# Cabinet 1c
Django

# Запуск
1. pipenv install
2. pipenv shell
3. python manage.py runserver 0.0.0.0:8000
4. python manage.py migrate

# Docker
- postgres
- docker run -p 5544:5432 -d --name django-postgres -e POSTGRES_PASSWORD=pass postgres:13.1-alpine
- docker run -p 27017:27017 -d --name django-mongodb -e MONGO_INITDB_ROOT_USERNAME=root -e MONGO_INITDB_ROOT_PASSWORD=pass mongo:4.4.3-bionic
- docker run -p 4321:4321 -d --name mongodb-web -e MONGO_URL=mongodb://root:pass@192.168.0.100:27017 ugleiton/mongo-gui