# <i>Una Health API Test task</i>


## Description

Simple Django + DRF CRUD API, represented by an only data model, containing information on patients' blood measurements, taken with a special device.
The blood measurements data can be retrieved and exported into an Excel file as well us be uploaded from a csv file via a specific POST route of the API.

## Table of Contents

- [Key Features](#key-features)
- [Set up project](#set-up-project)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
- [Technologies Used](#technologies-used)

## Key Features

- Data upload from a csv file that will be parsed into a DB model
- Data download - export to an Excel file

## Set up project

### Prerequisites
Before running the application, make sure you have the following dependencies installed on your system:

- Docker: [Install Docker](https://docs.docker.com/get-docker/)
- Docker Compose: [Install Docker Compose](https://docs.docker.com/compose/install/)
- Makefile utility (optional)

### Installation

1. Clone the repository to your local machine and make it your current working directory:

```
git clone https://github.com/RogerRabbit32/UnaHealth---TestTask.git
cd GlukoseAPI
```

2. Build the Docker image. Run the command:


```
make build
```
or, alternatively
```
docker-compose build
```

3. Start the containers. Run the command:

```
make up
```
or

```
docker-compose up
```


If the installation is successful, your app should be available at [http://localhost:8000](http://localhost:8000),
all of the routes with example usages are given at <i><b>/api/docs/<b><i>

## Technologies used
<ul>
<li>Django: Python Web framework for building web apps</li>
<li>DRF: Python Web framework, Django extension for building APIs</li>
<li>pytest: Python framework for tests management</li>
<li>PostgreSQL: Database management system for storing application data</li>
<li>Docker + Docker Compose: Containerization for easy deployment</li>
</ul>
