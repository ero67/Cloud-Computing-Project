from prefect import serve
from prefect.deployments import Deployment
from taxi_data_flow import NY_Taxi_Data_Flow

# Create deployment
deployment = Deployment.build_from_flow(
    flow=NY_Taxi_Data_Flow,
    name="taxi-data-flow",
    work_pool_name="k8s-pool",
    work_queue_name="default"
)

if __name__ == "__main__":
    deployment.apply()
    print("Deployment registered successfully!")