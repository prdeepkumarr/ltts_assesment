# LTTS(SKY) Assessment

This is to fetch the data from the api endpoints and display that in the form of json

## Table of Contents
	- Installation
	- Usage
	- API Endpoint

## Installation

To run this project, you will need:

- Docker
- Python 3
- Flask
- Swagger

To install these requirements, you can run the following command:

```
pip install -r requirements.txt
```
To build a Docker image from the Dockerfile, you can use the following command:

```
docker build -t project-name .
```
To run the Python script inside the Docker container, you can use the following command:

```
docker run project-name python run_file.py
```

## Usage

To access the Swagger documentation for the API, you can open a web browser and navigate to

``` 
localhost:5000/apidocs
```

## API Endpoint

Api endpoint to register the user 
```
localhost:5000/token/register
```
Api endpoint to login, this will generate the access token and refresh token 
```
localhost:5000/token/login
````
