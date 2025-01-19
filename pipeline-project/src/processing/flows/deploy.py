from prefect import serve
from taxi_data_flow import NY_Taxi_Data_Flow

if __name__ == "__main__":
    deployment = NY_Taxi_Data_Flow.to_deployment(
        name="taxi-data-flow",
        work_pool_name="k8s-pool",
        work_queue_name="default"
    )
    
    # Deploy the flow
    deployment.apply()
    print("Flow deployment registered successfully!")
    
    # Optionally serve the deployment
    # serve(deployment)