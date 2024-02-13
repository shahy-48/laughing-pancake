# Data Engineering Project

## Steps:
1. Identify the dataset which in this case is the NY taxi data available freely on their website. The data is a parquet file.
2. Use Jupyter notebook to process and clean the data
3. Use docker-compose.yaml file to run postgres & pgadmin in a single container (avoids creating a network if they are run in teo different containers)
4. Use sqlalchemy to create an engine and then use that to dump taxi data from our dataframe into postgres db
5. Create a dockerfile which installs python in the container shell and then installs necessary libraries for the ingestion script to run
6. Install Terraform
7. Create a main.tf file with provider details and other setup related to provisioning resources in the cloud platform (Google in our case)
8. Create a GCP account
    a. Create a new project
    b. Create a service account
    c. Generate a new key as json
    d. Store these as a json file "my-creds.json"
    e. set the environment variable GOOGLE_APPLICATION_CREDENTIALS to this josn file's path
    f. Give the following access to this service account
        i. Bigquery admin
        ii. Storage admin
        iii. Storage object admin
    c. Give the following api access to this service account, enabling the iam service
        i. de-yash@de-zc-ny-taxi.iam.gserviceaccount.com
        ii. resource: //cloudresourcemanager.googleapis.com/projects/de-zc-ny-taxi
9. Install the gcloud sdk to be able to access it using cli, preferrably in the root folder
10. Authenticate using the following "gcloud auth application-default login". Once authenticated, you can use cli to talk to GCP