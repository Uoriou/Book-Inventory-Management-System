# Book Inventory Management System (BIM)

A platform for managing your book inventory (Backend API only)

## Technical Requirements:
To run the BIM system, please ensure that your system meets the following requirements:

- Operating System: Windows, macOS, or Linux
- Docker

## Library / Technologies Used:

- Python Django
- Docker

   [![My Skills](https://skillicons.dev/icons?i=py,django,docker&perline=3)](https://skillicons.dev)


## API Integration:

- Google Book API 

## Installation Guidline

- Please install Docker desktop: https://www.docker.com/products/docker-desktop/
- Make sure to clone this project

## Run the docker image

Once Docker is installed, it is possible to use the .yml file of this project to build the docker image to run the project using this command: 
```bash 
    docker compose up -d --build 
```

Make sure to run the project container. 

Once the container is up and running, create a superuser:

```bash
   docker-compose exec web python manage.py createsuperuser
```
The command will ask for your username and password, which will allow you to access the Django admin panel.

To stop the container and the application run:
```bash
    docker compose down
```
