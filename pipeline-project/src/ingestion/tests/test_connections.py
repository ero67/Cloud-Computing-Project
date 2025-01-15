# test_connections.py
from google.cloud import storage
from google.cloud import bigquery
import psycopg2
import os
import logging

# Set up logging
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
    """Test Cloud SQL connectivity"""
    try:
        # Get connection details from environment variables
        db_host = os.getenv('DB_HOST', 'cloudsql-proxy')
        db_port = os.getenv('DB_PORT', '5432')
        db_name = os.getenv('DB_NAME')
        db_user = os.getenv('DB_USER')
        db_password = os.getenv('DB_PASSWORD')

        # Connect to database
        conn = psycopg2.connect(
            host=db_host,
            port=db_port,
            dbname=db_name,
            user=db_user,
            password=db_password
        )
        
        # Test connection by executing simple query
        with conn.cursor() as cur:
            cur.execute('SELECT version();')
            version = cur.fetchone()
            logger.info(f"Successfully connected to Cloud SQL. PostgreSQL version: {version[0]}")
        
        conn.close()
        return True

    except Exception as e:
        logger.error(f"Failed to connect to Cloud SQL: {e}")
        return False

def main():
    """Run all connection tests"""
    logger.info("Starting connection tests...")
    
    # Run tests
    gcs_result = test_gcs_connection()
    bq_result = test_bigquery_connection()
    sql_result = test_cloudsql_connection()
    
    # Summary
    logger.info("\nTest Results:")
    logger.info(f"GCS Connection: {'✓' if gcs_result else '✗'}")
    logger.info(f"BigQuery Connection: {'✓' if bq_result else '✗'}")
    logger.info(f"Cloud SQL Connection: {'✓' if sql_result else '✗'}")
    
    # Overall status
    all_passed = all([gcs_result, bq_result, sql_result])
    logger.info(f"\nOverall Status: {'All tests passed!' if all_passed else 'Some tests failed.'}")
    
    return all_passed

if __name__ == "__main__":
    main()