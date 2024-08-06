# Streamlit and DynamoDB Local Setup on Kubernetes

## Description

This project demonstrates how to deploy a Streamlit application connected to a local instance of DynamoDB running on a Kubernetes cluster. This setup is beneficial for developers who want to test their applications in a local environment that simulates a cloud-based architecture. By using Kubernetes, Docker, and Minikube, we create a development environment that is both scalable and consistent with production deployments. This allows developers to experiment and develop with minimal costs while ensuring their applications work as expected when deployed to cloud environments.

## Prerequisites

Before you begin, ensure you have the following installed on your system:

1. **Docker**: Required for building and running containers.
   - [Install Docker](https://docs.docker.com/get-docker/)
   - Verify installation: `docker --version`
   - Try running `docker run hello-world` or 'docker run -it ubuntu bash'

2. **Minikube**: A tool to run Kubernetes locally.
   - [Install Minikube](https://minikube.sigs.k8s.io/docs/start/)
   - Verify installation: `minikube version`

3. **kubectl**: Kubernetes command-line tool to interact with your cluster.
   - [Install kubectl](https://kubernetes.io/docs/tasks/tools/install-kubectl/)
   - Verify installation: `kubectl version --client`

4. **AWS CLI**: Command-line tool for interacting with AWS services.
   - [Install AWS CLI](https://aws.amazon.com/cli/)
   - Verify installation: `aws --version`

5. **Python 3.x**: Required to run Streamlit locally for development purposes.
   - [Install Python](https://www.python.org/downloads/)
   - Verify installation: `python --version`

6. **Streamlit**: Install Streamlit for running the application.
   - Install via pip: `pip install streamlit`

### Setting Up the Project

1. **Clone the Repository**

   Clone this repository to your local machine:

   ```bash
   git clone https://github.com/waughb/dynamodb-streamlit.git
   cd dynamodb-streamlit
   ```

2. **Build the Docker Image**

    Build the Docker image for the Streamlit application:

    ```bash
    docker build -t streamlit-dynamodb-app .
    ```

3. **Start Minikube**

    Start your local Kubernetes cluster using Minikube:

    ```bash
    minikube start
    ```

4. **Deploy DynamoDB Local to Kubernetes**

    Apply the Kubernetes manifests to deploy DynamoDB Local:

    ```bash
    kubectl apply -f dynamodb-local-deployment.yaml
    kubectl apply -f dynamodb-local-service.yaml
    ```

5. **Deploy the Streamlit Application**

    Apply the Kubernetes manifests to deploy the Streamlit application:

    ```bash
    kubectl apply -f deployment.yaml
    kubectl apply -f service.yaml
    ```

6. **Port forwarding**

    ```bash
    kubectl port-forward --address 0.0.0.0 -n default service/streamlit-dynamodb-app 30001:8501
    ```    

### Alternate Setup: Docker-Compose

1. **Build the Docker compose project**
    Build the Docker Compose image for the Streamlit application:

    ```bash
    docker-compose build
    ```

## **How to Run**

1. Access the Streamlit Application

    Use Minikube to access the Streamlit application:

    ```bash
    minikube service streamlit-dynamodb-app
    ```

    This command will open your default web browser and navigate to the Streamlit application.

### **Alternate Run: Docker-Compose**

1. Access the Streamlit Application

    Use Docker Compose to access the Streamlit application:

    ```bash
    docker-compose up -d
    ```

    This command will open your default web browser and navigate to the Streamlit application.


## How to Shutdown

1. Stop the Streamlit Application

    Delete the Streamlit application deployment and service:

    ```bash
    kubectl delete -f deployment.yaml
    kubectl delete -f service.yaml
    ```

2. Stop DynamoDB Local

    Delete the DynamoDB Local deployment and service:

    ```bash
    kubectl delete -f dynamodb-local-deployment.yaml
    kubectl delete -f dynamodb-local-service.yaml
    ```

3. Stop Minikube

    Stop the Minikube cluster:

    ```bash
    minikube stop
    ```

4. Optionally, delete the Minikube cluster to free up resources:

    ```bash
    minikube delete
    ```

### Alternative Shutdown: Docker-Compose

1. **How to shutdown Docker Compose**

    Use
    ```bash
    docker-compose down

    ```

### Test Cases
To verify the setup and functionality of your project, run the following test cases:

1. Check Pod Status

    Ensure all pods are running:

    ```bash
    kubectl get pods
    ```

Expected output: Pods with names dynamodb-local and streamlit-dynamodb should be in Running status.

2. Check Streamlit Application Access

    Use the following curl command to ensure the Streamlit application is accessible:

    ```bash
    curl $(minikube service streamlit-dynamodb-service --url)
    ```

Expected output: HTML content indicating the Streamlit application is running.

3. Interact with the Application

* Open the Streamlit application in your web browser.
* Verify you can view and add products through the application's interface.

## Troubleshooting

I have lots of difficulties updating minikube to the latest version. First stop the pods from running. Then I ended up using `minikube image rm streamlit-dynamodb-app` to fully remove the image. Then re-add the image `minikube image load streamlit-dynamodb-app:latest`. You can verify this by checking `minikube image ls --format table ` before and after and confirming the ID in Docker Desktop. 