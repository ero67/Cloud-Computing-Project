from google.cloud import storage
from google.cloud import bigquery
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_gcs_access():
    """Test GCS bucket access"""
    try:
        # Initialize storage client
        storage_client = storage.Client()
        
        # Get the bucket
        bucket_name = "data-pipeline-parquet-teak-gamma-442315-f8"
        bucket = storage_client.get_bucket(bucket_name)
        
        # Create a test file
        blob = bucket.blob('test.txt')
        blob.upload_from_string('Hello, World!')
        
        logger.info(f"Successfully wrote to bucket: {bucket.name}")
        return True
    except Exception as e:
        logger.error(f"Failed to access GCS: {e}")
        return False

def test_bigquery_access():
    """Test BigQuery dataset access"""
    try:
        # Initialize BigQuery client
        client = bigquery.Client()
        
        # Get the dataset
        dataset_id = "teak-gamma-442315-f8.data_pipeline"
        dataset = client.get_dataset(dataset_id)
        
        logger.info(f"Successfully accessed dataset: {dataset.dataset_id}")
        return True
    except Exception as e:
        logger.error(f"Failed to access BigQuery: {e}")
        return False

if __name__ == "__main__":
    logger.info("Starting storage access tests...")
    gcs_result = test_gcs_access()
    bq_result = test_bigquery_access()
    
    logger.info("\nTest Results:")
    logger.info(f"GCS Access: {'✓' if gcs_result else '✗'}")
    logger.info(f"BigQuery Access: {'✓' if bq_result else '✗'}")