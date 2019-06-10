# Mock API Gateway

[![Build Status](https://dev.azure.com/d-risk/api-gateway/_apis/build/status/d-risk.mock-api-gateway?branchName=master)](https://dev.azure.com/d-risk/api-gateway/_build/latest?definitionId=16&branchName=master)

This project is a microservice that provides credit reports on companies through [GraphQL].
You can learn more about GraphQL by following the given link.

## Getting Started

These instructions should get you started on this service.

### Prerequisites

Here are the requirements that you need to have before starting on this project.

* [Git]
* [Docker]
* [Python] 3.7 or higher

### Installing

First, we need to clone this project on your local machine.
Below is a commandline to clone this project to your local machine.

```commandline
git clone https://github.com/d-risk/credit-report-service.git
```

After cloning this project, it is time to create and populate a database for this service to use.
The database should be created and populated before continuing further.
In development mode, this service uses a file-based database Sqlite named `db.sqlite3`.
Below is the commandline to create and populate the database with randomly generated data.

```commandline
python manage.py populatedb --companies 100 --singtel
```

The first argument `--companies` specifies how many companies to be generated.
The above example `--companies 100` will create 100 companies.
The `--singtel` will add a credit report for the company Singapore Telecommunication Limited.

There are two ways to start this service: as a Docker container or using Python.

### Using Docker

If you would like to run this service as a Docker container, there is a `Dockerfile` to create a Docker image.
Below is the commandline to build a Docker image.

```commandline
docker build -t d-risk/credit-report-service .
```

Once the Docker image is built, it is time to run the image.
Below is the commandline to run the image.

```commandline
docker run --name credit-report-service -p 8000:8080 --rm -it d-risk/credit-report-service
```

When the Docker container is initialized, you can interact with this service using a browser through the given URL.
For example, using the above example, it would be `localhost:8000`.
The port is the port that is mapped to the Docker container.

### Using Python

The Python approach is meant for you to run this service on your local machine.
It is recommended to create a virtual environment to install the required packages.
Create a virtual environment as indicated below.

```commandline
python -m venv .venv
```

This will create the `.venv` directory for the virtual environment.
To switch to the virtual environment, follow the commandline below.

On Windows:
```commandline
.venv\Scripts\activate
```
On Unix or MacOS:
```commandline
source .venv/bin/activate
```

Once in the virtual environment, install the dependencies as indicated below.

```commandline
pip install -r requirements.freeze.txt
```

Once the dependencies are installed, you can start this service using the commandline given below.

```commandline
python manage.py runserver
```

Once the service is started, use a browser and go to the given URL.
Usually, it is `localhost:8000`.

### Deploying

The Docker image is the recommended way to deploy this service.
Once the Docker image is created, it can be uploaded to a repository of your choice and deployed on your preferred cloud platform.


[GraphQL]: https://graphql.org/
[Git]: https://git-scm.com/
[Docker]: https://www.docker.com/
[Python]: https://www.python.org/
