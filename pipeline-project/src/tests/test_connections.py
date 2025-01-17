from google.cloud import storage
from google.cloud import bigquery
from google.cloud.sql.connector import Connector
import logging
import os
import sqlalchemy

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_gcs_connection():
    """Test Google Cloud Storage connectivity"""
    try:
        storage_client = storage.Client()
        buckets = list(storage_client.list_buckets())
        logger.info(f"Successfully connected to GCS. Found {len(buckets)} buckets.")
        return True
    except Exception as e:
        logger.error(f"Failed to connect to GCS: {e}")
        return False

def test_bigquery_connection():
    """Test BigQuery connectivity"""
    try:
        client = bigquery.Client()
        datasets = list(client.list_datasets())
        logger.info(f"Successfully connected to BigQuery. Found {len(datasets)} datasets.")
        return True
    except Exception as e:
        logger.error(f"Failed to connect to BigQuery: {e}")
        return False

def test_cloudsql_connection():
    """Test Cloud SQL connectivity using the same method as processing code"""
    try:
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
                db=db_name
            )

        engine = sqlalchemy.create_engine(
            "postgresql+pg8000://",
            creator=getconn
        )

        # Test connection by executing a simple query
        with engine.connect() as conn:
            conn.execute(sqlalchemy.text("SELECT 1"))
        
        logger.info("Successfully connected to Cloud SQL")
        return True
    except Exception as e:
        logger.error(f"Failed to connect to Cloud SQL: {e}")
        return False

def main():
    """Run all connection tests"""
    logger.info("Starting connection tests...")
    
    gcs_result = test_gcs_connection()
    bq_result = test_bigquery_connection()
    sql_result = test_cloudsql_connection()
    
    logger.info("\nTest Results:")
    logger.info(f"GCS Connection: {'✓' if gcs_result else '✗'}")
    logger.info(f"BigQuery Connection: {'✓' if bq_result else '✗'}")
    logger.info(f"Cloud SQL Connection: {'✓' if sql_result else '✗'}")
    
    all_passed = all([gcs_result, bq_result, sql_result])
    logger.info(f"\nOverall Status: {'All tests passed!' if all_passed else 'Some tests failed.'}")
    
    return all_passed

if __name__ == "__main__":
    main()