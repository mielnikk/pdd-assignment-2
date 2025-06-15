1. Export environment variables
   ```
   GCP_userID=
   PROJECT_ID=
   SERVICE_NAME=
   deployKeyName=".secrets/$SERVICE_NAME.json"
   privateKeyFile=
   
   export PROJECT_ID=$PROJECT_ID
   export SERVICE_NAME=$SERVICE_NAME
   export GCP_userID=$GCP_userID
   export GCP_privateKeyFile=$privateKeyFile
   
   ### Terrform setup variables
   # Name of your GCP project
   export TF_VAR_project_id=$PROJECT_ID
   # Name of your selected GCP region
   export TF_VAR_region=europe-central2
   # Name of your selected GCP zone
   export TF_VAR_zone=europe-central2-a
   
   ### Other variables used by Terrform
   # VM type
   export TF_VAR_instance_type=e2-medium
   
   export TF_VAR_spark_worker_count=1
   export TF_VAR_kafka_broker_count=1
   export TF_VAR_zookeeper_count=1
   # Prefix of your GCP deployment key
   export TF_VAR_deploy_key_name=$deployKeyName
   export TF_VAR_gcp_user=$GCP_userID

   ```
2. Init GCloud
    ```
    gcloud init
    gcloud config set project $PROJECT_ID
    gcloud services enable iam.googleapis.com
    gcloud services enable compute.googleapis.com
    
    gcloud iam service-accounts create $SERVICE_NAME
    gcloud projects add-iam-policy-binding $PROJECT_ID --member serviceAccount:$SERVICE_NAME@$PROJECT_ID.iam.gserviceaccount.com --role roles/editor
    gcloud iam service-accounts keys create ./$SERVICE_NAME.json --iam-account $SERVICE_NAME@$PROJECT_ID.iam.gserviceaccount.com
    ```
3. Add metadata SSH key on GCP
4. Run:
    ```
    terraform init
    terraform apply
    
    terraform output -json > terraform_output.json
    python3 scripts/generate_inventory.py
    ```
5. Ansible stuff
    ```
    ansible-playbook --key-file $GCP_privateKeyFile -i ansible/inventory.ini ansible/install-dependencies.yml
    ansible-playbook --key-file $GCP_privateKeyFile -i ansible/inventory.ini ansible/start-services.yml
    ```
   
In order to stop running clusters run `stop_services.yml`