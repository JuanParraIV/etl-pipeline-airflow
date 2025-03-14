# libraries for etl
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.providers.http.operators.http import SimpleHttpOperator
from airflow.decorators import dag, task
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.utils.dates import days_ago
import os

## Upload the NASA_API_KEY to the Airflow Connection
NASA_API_KEY = os.getenv("NASA_API_KEY")

## Define the DAG

with DAG(
    "nasa_apod_postgress",
    start_date=days_ago(1),
    schedule_interval="@daily",
    catchup=False,
    tags=["nasa", "apod", "postgress"],
) as dag:
    ## step 1: create the table if doesn't exist
    @task
    def create_table():
        ## initialize the postgres hook with ORM Object relation mapping
        postgres_hook = PostgresHook(postgres_conn_id="postgres_connection")

        ## SQL query to create the table
        create_table_query = """
      CREATE TABLE IF NOT EXISTS apod_data(
        id SERIAL PRIMARY KEY,
        title VARCHAR(255),
        explanation TEXT,
        url TEXT,
        date DATE,
        media_type VARCHAR(50)
      );
      """
        postgres_hook.run(create_table_query)

    ## step 2: Extract the NASA API Data(APOD)- Astronomy Picture of the Day [Extract pipeline]

    extract_nasa_apod = SimpleHttpOperator(
        task_id="extract_nasa_apod",
        http_conn_id="nasa_apod_api",  # connection id define in airflow to the NASA API
        method="GET",
        endpoint="planetary/apod",  # endpoint to get the APOD data
        data={
            "api_key": "{{ conn.nasa_apod_api.extra_dejson.api_key}}"
        },  # data to pass to the endpoint
        headers={"Content-Type": "application/json"},
        response_filter=lambda response: response.json(),  # Convert the response to json
        # response_check=lambda response: response.json()['json']['priority'] == 5,
        # extra_options: Optional[Dict[str, Any]] = None,
        # log_response: bool = False,
        # auth_type: Type[AuthBase] = HTTPBasicAuth,
    )

    ## step 3: Transform the data [Transform pipeline]
    @task
    def transform_apod_data(response):
        apod_data = {
            "title": response.get("title", ""),
            "explanation": response.get("explanation", ""),
            "url": response.get("url", ""),
            "date": response.get("date", ""),
            "media_type": response.get("media_type", ""),
        }

        return apod_data

    ## step 4: Load the data into Postgres [Load pipeline]

    @task
    def load_apod_data(apod_data):
        ## Initialize the postgres hook
        postgres_hook = PostgresHook(postgres_conn_id="postgres_connection")

        ## Define the query to insert the data into the table
        insert_query = """
            INSERT INTO apod_data(title, explanation, url, date, media_type)
            VALUES(%s, %s, %s, %s, %s)
            """
        ## Execute the query
        postgres_hook.run(
            insert_query,
            parameters=(
                apod_data["title"],
                apod_data["explanation"],
                apod_data["url"],
                apod_data["date"],
                apod_data["media_type"],
            ),
        )

    ## step 5: Data Quality Check [Data Quality pipeline]

    ## step 6: define the tasks dependencies

    ## Extract
    create_table() >> extract_nasa_apod  ## ensure the table before extraction
    api_response = extract_nasa_apod.output

    ## Transform
    transformed_data = transform_apod_data(api_response)

    ## Load
    load_apod_data(transformed_data)
