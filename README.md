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

- Please install Docker 
- Clone this BIM repository

## Run the docker image

Once Docker is installed, build the docker image 
```bash
   docker build -t "your-image-name" .
 ```
Then, run the container
```bash
   docker run -p 8000:8000 "your-image-name"
```
Alternatively, if there is a docker-compose.yml file, 
you can build and start all services with a single command:
```bash
   docker compose up --build
 ```

Access the application at ``` `http://127.0.0.1:8000/` ```

To stop the continer press Ctrl+C
