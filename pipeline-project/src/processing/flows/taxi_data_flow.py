from prefect import task, flow
import pandas as pd
import os
import requests
import time
from datetime import datetime, timedelta
from google.cloud import storage, bigquery
from sqlalchemy import create_engine
from google.api_core.exceptions import GoogleAPICallError, RetryError
from requests.exceptions import SSLError
import pyarrow as pa
import pyarrow.parquet as pq
from google.cloud.sql.connector import Connector, IPTypes
import sqlalchemy

@task(name="download_parquet")
def download_parquet(url, file_path):
    response = requests.get(url)
    if response.status_code == 200:
        with open(file_path, 'wb') as f:
            f.write(response.content)
        print(f"Parquet file downloaded to {file_path}")
    else:
        print(f"Failed to download the file from {url}")
    return file_path

@task(name="extract_parquet")
def extract_parquet(file_path):
    df = pd.read_parquet(file_path)
    return df

@task(name="process_dataframe")
def process_dataframe(df):
    df = df.assign(Load_dt=pd.to_datetime(datetime.now()))
    df = df.assign(Total_squared=[x**2 for x in df['total_amount']])
    return df

@task(name="convert_to_parquet")
def convert_to_parquet(df, file_path):
    """Converts DataFrame to Parquet file and saves it to the given file path."""
    # Convert DataFrame to Parquet using pyarrow
    table = pa.Table.from_pandas(df)
    pq.write_table(table, file_path)
    print(f"DataFrame converted to Parquet and saved to {file_path}.")
    return file_path

@task(name="upload_to_gcs")
def upload_to_gcs(bucket_name, source_file_path, destination_blob_name):
    """Uploads a Parquet file to Google Cloud Storage."""
    # Initialize the GCS client
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    # Upload the Parquet file
    blob.upload_from_filename(source_file_path)
    print(f"Parquet file uploaded to GCS: {destination_blob_name}")
    return f"gs://{bucket_name}/{destination_blob_name}"

@task(name="insert_into_cloud_sql")
def insert_into_cloud_sql(df, table_name):
    instance_name = os.getenv("CLOUDSQL_CONNECTION_NAME")
    db_user = os.getenv("DB_USER")
    db_pass = os.getenv("DB_PASSWORD")
    db_name = os.getenv("DB_NAME")

    connector = Connector()

    def getconn():
        return connector.connect(
            instance_name,
            "pg8000",
            user=db_user,
            password=db_pass,
            db=db_name,
        )

    engine = sqlalchemy.create_engine(
        "postgresql+pg8000://",
        creator=getconn,
    )

    try:
        df.to_sql(table_name, engine, if_exists='replace', index=False, chunksize=2000)
        print(f"Data inserted into Cloud SQL table {table_name}.")
    except Exception as e:
        print(f"Error inserting data into Cloud SQL: {e}")
    \
    return table_name

@task(name="load_parquet_to_bigquery")
def load_parquet_to_bigquery(gcs_uri, project_id, dataset_id, table_id):
    """Loads Parquet file from GCS into BigQuery."""
    client = bigquery.Client(project=project_id)

    # Define the BigQuery dataset and table references
    dataset_ref = client.dataset(dataset_id)
    table_ref = dataset_ref.table(table_id)

    # Create job config for Parquet
    job_config = bigquery.LoadJobConfig(
        source_format=bigquery.SourceFormat.PARQUET,
        write_disposition="WRITE_TRUNCATE",  # Replace the table if it exists
    )

    # Start the load job from GCS to BigQuery
    load_job = client.load_table_from_uri(gcs_uri, table_ref, job_config=job_config)
    load_job.result()  # Wait for the job to complete

    print(f"Data from Parquet file loaded into BigQuery table {table_id}.")

@flow(name="NY_Taxi_Data_Flow")
def NY_Taxi_Data_Flow():
    # Parameters
    url = 'https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2021-01.parquet'
    now = datetime.now().strftime("%Y_%m_%d")

    file = 'yellow_tripdata'

    # Using current working directory (Windows compatible)
    base_path = os.getcwd()  # Get current working directory
    file_path = os.path.join(base_path, file + '_.parquet')
    file_path_processed = os.path.join(base_path, file + '_processed.parquet')

    new_path = os.path.join(base_path, 'Archive', file + '_' + str(now) + ".parquet")
    destination_blob_name = 'raw_data/yellow_taxi_data.parquet'  # GCS blob name
    destination_blob_name_processed = 'processed/yellow_taxi_data.parquet'  # GCS blob name

    bucket_name = 'data-pipeline-parquet-teak-gamma-442315-f8'
    project_id = 'teak-gamma-442315-f8'
    dataset_id = 'data_pipeline'  # BigQuery dataset name
    table_id = 'yellow_taxi_trips'  # BigQuery table name
    target_table = 'yellow_taxi_trips'

    # Download the Parquet file from the URL
    download_parquet(url, file_path)

    # upload bronze data to gcs
    upload_to_gcs(bucket_name, file_path, destination_blob_name)

    # extract parquet into df
    df = extract_parquet(file_path)
    
    # apply basic transformations
    df_transformed = process_dataframe(df)

    # Step 3: Save transformed data to Google Cloud Storage)
    parquet_file = convert_to_parquet(df_transformed, file_path_processed)
    
    gcs_uri = upload_to_gcs(bucket_name, parquet_file, destination_blob_name_processed)

    # insert_into_cloud_sql(df_transformed, target_table)

    load_parquet_to_bigquery(gcs_uri, project_id, dataset_id, table_id)

if __name__ == '__main__':
    NY_Taxi_Data_Flow()