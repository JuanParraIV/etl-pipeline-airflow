# Project Overview: Airflow ETL Pipeline with Postgres and API Integration
This project involves creating an ETL (Extract, Transform, Load) pipeline using Apache Airflow. The pipeline extracts data from an external API (in this case, NASA's Astronomy Picture of the Day (APOD) API), transforms the data, and loads it into a Postgres database. The entire workflow is orchestrated by Airflow, a platform that allows scheduling, monitoring, and managing workflows.

The project leverages Docker to run Airflow and Postgres as services, ensuring an isolated and reproducible environment. We also utilize Airflow hooks and operators to handle the ETL process efficiently.


## Key Components of the Project:
### Airflow for Orchestration:
Airflow is used to define, schedule, and monitor the entire ETL pipeline. It manages task dependencies, ensuring that the process runs sequentially and reliably.
The Airflow DAG (Directed Acyclic Graph) defines the workflow, which includes tasks like data extraction, transformation, and loading.

### Postgres Database:
A PostgreSQL database is used to store the extracted and transformed data.
Postgres is hosted in a Docker container, making it easy to manage and ensuring data persistence through Docker volumes.
We interact with Postgres using Airflow’s PostgresHook and PostgresOperator.

### NASA API (Astronomy Picture of the Day):
The external API used in this project is NASA’s APOD API, which provides data about the astronomy picture of the day, including metadata like the title, explanation, and the URL of the image.
We use Airflow’s SimpleHttpOperator to extract data from the API.
Objectives of the Project:
Extract Data:

The pipeline extracts astronomy-related data from NASA’s APOD API on a scheduled basis (daily, in this case).

### Transform Data:
Transformations such as filtering or processing the API response are performed to ensure that the data is in a suitable format before being inserted into the database.

### Load Data into Postgres:
The transformed data is loaded into a Postgres database. The data can be used for further analysis, reporting, or visualization.
Architecture and Workflow:
The ETL pipeline is orchestrated in Airflow using a DAG (Directed Acyclic Graph). The pipeline consists of the following stages:

1. Extract (E):
The SimpleHttpOperator is used to make HTTP GET requests to NASA’s APOD API.
The response is in JSON format, containing fields like the title of the picture, the explanation, and the URL to the image.
2. Transform (T):
The extracted JSON data is processed in the transform task using Airflow’s TaskFlow API (with the @task decorator).
This stage involves extracting relevant fields like title, explanation, url, and date and ensuring they are in the correct format for the database.
3. Load (L):
The transformed data is loaded into a Postgres table using PostgresHook.
If the target table doesn’t exist in the Postgres database, it is created automatically as part of the DAG using a create table task.



# Get Started with Airflow using the Astro CLI

With the Astro CLI, you can run Airflow on your local machine. Follow this quickstart to build an Airflow project from the Learning Airflow template and run it in a local Airflow environment with just a few commands. At the end of the tutorial, you'll have all of the files and components you need to develop and test Airflow DAGs locally.

## Step 1: Install the CLI

### Mac
```bash
brew install astro
```

### Windows with winget
```bash
winget install astro
```


## Step 2: Create an Astro Project

An Astro project contains the set of files necessary to run Airflow, including dedicated folders for your DAG files, plugins, and dependencies. This set of files builds an image that you can run both on your local machine with Airflow and deploy to Astro.

Use `astro dev init` with the `--from-template` flag to create the project based off of the Learning Airflow template.
```bash
astro dev init --from-template learning-airflow
```

This command generates all of the project files you need to run Airflow locally, including an example DAG that you can run out of the box. Different templates generate different example DAGs. See Create an Astro project for more information about the default project structure.

## Step 3: Run Airflow Locally

Running your project locally allows you to test your DAGs before you deploy them to a production environment. While this step is not required for deploying and running your code on Astro, Astronomer recommends always using the Astro CLI to test locally before deploying.

To start running your project in a local Airflow environment, run the following command from the `learning-airflow` project directory:
```bash
astro dev start
```

This command builds your project and spins up 4 Docker containers on your machine, each for a different Airflow component:
- **Postgres**: Airflow's metadata database
- **Webserver**: The Airflow component responsible for rendering the Airflow UI
- **Scheduler**: The Airflow component responsible for monitoring and triggering tasks
- **Triggerer**: The Airflow component responsible for running Triggers and signaling tasks to resume when their conditions have been met. The triggerer is used exclusively for tasks that are run with deferrable operators

After your project builds successfully, open the Airflow UI in your web browser at [https://localhost:8080/](https://localhost:8080/).

Find your DAGs in the `dags` directory in the Airflow UI.

In this directory, you can find an example DAG, `example-astronauts`, which was generated with your Astro project. To provide a basic demonstration of an ETL pipeline, this DAG shows a simple ETL pipeline example that queries the list of astronauts currently in space from the Open Notify API and prints a statement for each astronaut. The DAG uses the TaskFlow API to define tasks in Python, and dynamic task mapping to dynamically print a statement for each astronaut.

### Example DAG in the Airflow UI

The Astro CLI uses port 8080 for the Airflow webserver and port 5432 for the Airflow metadata database by default. If these ports are already in use on your local computer, an error message might appear. To resolve this error message, see Run Airflow locally.

## Step 4: Develop Locally with the CLI

Now that you have a locally running project, you can start to develop your Astro project by adding DAGs, dependencies, environment variables, and more. See Develop your project for more details on how to modify all aspects of your Astro project.

Most changes you make, including updates to your DAG code, are applied automatically to your running environment and don't require rebuilding your project. However, you must rebuild your project and restart your environment to apply changes from any of the following files in your Astro project:
- `packages.txt`
- `Dockerfile`
- `requirements.txt`
- `airflow_settings.yaml`

To restart your local Airflow environment, run:
```bash
astro dev restart
```

This command rebuilds your image and restarts the Docker containers running on your local machine with the new image. Alternatively, you can run `astro dev stop` to stop your Docker containers without restarting your environment, then run `astro dev start` when you want to restart.