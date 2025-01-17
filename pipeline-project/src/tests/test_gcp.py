from google.cloud import storage
from google.cloud import bigquery
import os
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_gcs_connection():
    """Test Google Cloud Storage connectivity"""
    try:
        # Initialize the client
        storage_client = storage.Client()
        
        # List buckets to test connection
        buckets = list(storage_client.list_buckets())
        logger.info(f"Successfully connected to GCS. Found {len(buckets)} buckets.")
        
        return True
        
    except Exception as e:
        logger.error(f"Failed to connect to GCS: {e}")
        return False

def test_bigquery_connection():
    """Test BigQuery connectivity"""
    try:
        # Initialize the client
        client = bigquery.Client()
        
        # Try to list datasets
        datasets = list(client.list_datasets())
        logger.info(f"Successfully connected to BigQuery. Found {len(datasets)} datasets.")
        return True
        
    except Exception as e:
        logger.error(f"Failed to connect to BigQuery: {e}")
        return False

def main():
    """Run all connection tests"""
    logger.info("Starting GCP connection tests...")
    
    # Run tests
    gcs_result = test_gcs_connection()
    bq_result = test_bigquery_connection()
    
    # Summary
    logger.info("\nTest Results:")
    logger.info(f"GCS Connection: {'✓' if gcs_result else '✗'}")
    logger.info(f"BigQuery Connection: {'✓' if bq_result else '✗'}")
    
    # Overall status
    all_passed = all([gcs_result, bq_result])
    logger.info(f"\nOverall Status: {'All tests passed!' if all_passed else 'Some tests failed.'}")
    
    return all_passed

if __name__ == "__main__":
    main()