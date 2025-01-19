# import os
# from prefect import flow
# from prefect_kubernetes.jobs import KubernetesJob
# from taxi_data_flow import NY_Taxi_Data_Flow

# # Set environment variable for deployment creation
# os.environ["PREFECT_API_URL"] = "http://prefect-server:4200/api"

# # Create deployment
# deployment = NY_Taxi_Data_Flow.to_deployment(
#     name="taxi-data-flow",
#     work_pool_name="k8s-pool",
#     work_queue_name="default"
# )

# if __name__ == "__main__":
#     print("Registering flow deployment with Prefect server...")
#     deployment.apply()  # Just register and exit
#     print("Flow deployment registered successfully!")
import os
from prefect import serve
from prefect_kubernetes.jobs import KubernetesJob
from taxi_data_flow import NY_Taxi_Data_Flow

# Set environment variable for deployment creation
os.environ["PREFECT_API_URL"] = "http://prefect-server:4200/api"

# Create deployment with job configuration
deployment = NY_Taxi_Data_Flow.to_deployment(
    name="taxi-data-flow",
    work_pool_name="k8s-pool",
    work_queue_name="default"
)

if __name__ == "__main__":
    serve(deployment)