1. Export environment variables
2. 
    ```
    gcloud init
    gcloud config set project $PROJECT_ID
    gcloud services enable iam.googleapis.com
    gcloud services enable compute.googleapis.com
    
    gcloud iam service-accounts create $SERVICE_NAME
    gcloud projects add-iam-policy-binding $PROJECT_ID --member serviceAccount:$SERVICE_NAME@$PROJECT_ID.iam.gserviceaccount.com --role roles/editor
    gcloud iam service-accounts keys create ./$SERVICE_NAME.json --iam-account $SERVICE_NAME@$PROJECT_ID.iam.gserviceaccount.com
    ```
3. Add metadata ssh key on gcp
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