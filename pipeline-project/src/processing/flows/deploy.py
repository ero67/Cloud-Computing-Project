import os
from prefect import flow
from prefect_kubernetes.jobs import KubernetesJob
from taxi_data_flow import NY_Taxi_Data_Flow

# Set environment variable for deployment creation
os.environ["PREFECT_API_URL"] = "http://prefect-server:4200/api"

# Create deployment
deployment = NY_Taxi_Data_Flow.to_deployment(
    name="taxi-data-flow",
    work_pool_name="k8s-pool",
    work_queue_name="default",
    path="/taxi_data_flow.py"  # Add this line to specify the absolute path
)

if __name__ == "__main__":
    print("Registering flow deployment with Prefect server...")
    deployment.apply()
    print("Flow deployment registered successfully!")
# import os
# from prefect import serve
# from prefect_kubernetes.jobs import KubernetesJob
# from taxi_data_flow import NY_Taxi_Data_Flow

# # Set environment variable for deployment creation
# os.environ["PREFECT_API_URL"] = "http://prefect-server:4200/api"

# # Configure the Kubernetes job
# k8s_job = KubernetesJob(
#     v1_job={
#         "apiVersion": "batch/v1",
#         "kind": "Job",
#         "metadata": {
#             "namespace": "data-pipeline",
#             "generateName": "taxi-data-flow-"
#         },
#         "spec": {
#             "template": {
#                 "spec": {
#                     "containers": [{
#                         "name": "flow",
#                         "image": "gcr.io/teak-gamma-442315-f8/taxi-flow:latest",
#                         "imagePullPolicy": "Always",
#                         "env": [
#                             {"name": "PREFECT_API_URL", "value": "http://prefect-server:4200/api"},
#                             {"name": "DB_HOST", "value": "cloudsql-proxy"},
#                             {"name": "DB_PORT", "value": "5432"},
#                             {"name": "GCS_BUCKET", "value": "data-pipeline-parquet-teak-gamma-442315-f8"},
#                             {"name": "GOOGLE_APPLICATION_CREDENTIALS", "value": "/var/secrets/google/key.json"},
#                             {
#                                 "name": "DB_NAME",
#                                 "valueFrom": {
#                                     "secretKeyRef": {
#                                         "name": "cloudsql-credentials",
#                                         "key": "database"
#                                     }
#                                 }
#                             },
#                             {
#                                 "name": "DB_USER",
#                                 "valueFrom": {
#                                     "secretKeyRef": {
#                                         "name": "cloudsql-credentials",
#                                         "key": "username"
#                                     }
#                                 }
#                             },
#                             {
#                                 "name": "DB_PASSWORD",
#                                 "valueFrom": {
#                                     "secretKeyRef": {
#                                         "name": "cloudsql-credentials",
#                                         "key": "password"
#                                     }
#                                 }
#                             }
#                         ],
#                         "volumeMounts": [{
#                             "name": "gcp-key",
#                             "mountPath": "/var/secrets/google",
#                             "readOnly": True
#                         }]
#                     }],
#                     "volumes": [{
#                         "name": "gcp-key",
#                         "secret": {
#                             "secretName": "gcp-sa-key"
#                         }
#                     }],
#                     "serviceAccountName": "default",
#                     "restartPolicy": "Never"
#                 }
#             },
#             "backoffLimit": 0
#         }
#     }
# )

# # Create deployment with job configuration
# deployment = NY_Taxi_Data_Flow.to_deployment(
#     name="taxi-data-flow",
#     work_pool_name="k8s-pool",
#     work_queue_name="default"
# )

# if __name__ == "__main__":
#     serve(deployment)