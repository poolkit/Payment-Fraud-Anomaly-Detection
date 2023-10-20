# Payment Anomaly Detection 🚀

![Anomaly Detection](https://www.eway.com.au/wp-content/uploads/sites/12/2021/08/tools_for_card_not_present_fraud.jpg)

## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Getting Started](#getting-started)
  - [Dataset](#dataset)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Training](#training)
  - [Deployment](#deployment)
  - [Usage](#usage)
  - [Continuous Integration and Continuous Deployment (CI/CD)](#continuous-integration-and-continuous-deployment-cicd)
  - [Deploying on AWS](#deploying-on-aws)

## Introduction

📢 Welcome to the Payment Anomaly Detection project! This project leverages Isolation Forest to detect payment anomalies in your financial data. Anomalies can be a sign of fraud or unusual financial activity.

Detecting anomalies in your payment data is crucial for securing your financial transactions and identifying potential risks. This project provides an efficient solution for anomaly detection available in frontend and backend.

## Features

🌟 This project offers the following key features:

- **Unsupervised Learning**: The Isolation Forest algorithm for robust anomaly detection.

- **Web Application**: Fastapi backend to serve Streamlit frontend.

- **Docker Deployment**: Deploy the anomaly detection system using Docker containers in (AWS) ECR.

- **AWS EC2 Integration**: Deploy the Docker containers on Amazon Web Services (AWS) EC2 instances.

- **Continuous Integration and Continuous Deployment (CI/CD)**: GitHub Actions for automating the development workflow.

## Getting Started

### Dataset
📊 JP Morgan Chase has prepared a synthetic dataset, for research and development purposes. It can be found on [JP Morgan's Synthetic Data Webpage](https://www.jpmorgan.com/technology/artificial-intelligence/initiatives/synthetic-data/payments-data-for-fraud-detection). To access the dataset, send an email to the address provided on the given link.

### Prerequisites

Before getting started, make sure you have the following prerequisites:

- Python 3.x
- Docker
- An AWS Account
- GitHub account

### Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/poolkit/Payment-Fraud-Anomaly-Detection.git
   cd Payment-Fraud-Anomaly-Detection
   ```
2. Install the required Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Training

1. Change the data path in train_pipeline.py
2. Run the script to train and save the model in the artifacts folder.
   ```
   python train_pipeline.py
   ```

### Deployment

1. Build Docker images
   ```
   docker build -t frontend:latest -f web-app/frontend/Dockerfile.frontend .
   docker build -t backend:latest -f web-app/backend/Dockerfile.backend .
   ```
2. Use docker-compose.yml to build it together at once
   ```
   docker-compose build
   ```
3. To run the app
   ```
   docker-compose up
   ```

### Usage
🥳 Once the container is up and running on our local machine, we can access the web app using:<br>
   ```
   localhost:8000 #Backend
   localhost:5000 #Frontend
   ```

### Continuous Integration and Continuous Deployment (CI/CD)
🔄 Continuous Integration and Continuous Deployment (CI/CD) are set up using GitHub Actions. Every push to the main branch triggers an automated build and deployment process. You can view the GitHub Actions workflow in the .github/workflows/main.yaml directory.

### Deploying on AWS
🦞 Before running the CI/CD pipeline:

1. Create an IAM user with the following user roles
   ```
   AmazonEC2ContainerRegistryFullAccess
   AmazonEC2FullAccess
   ```

2. AWS ECR repository will be created on the fly while running the pipeline (steps included in main.yaml).

3. Create an EC2 instance and connect it. Run the following commands to set up EC2 correctly for Docker and GitHub Runner.
   ```
   sudo apt-get update -y
   sudo apt-get upgrade
   sudo apt install awscli -y
   curl -fsSL https://get.docker.com -o get-docker.sh
   sudo sh get-docker.sh
   sudo usermod -aG docker ubuntu
   newgrp docker
   sudo apt install docker-compose -y
   ```

4. Set up GitHub Actions runner
   - Go to Settings > Actions > Runners > New self-hosted runner
   - Select Linux OS and follow the download and configuration steps in EC2.
   - On ./run.sh the GitHub Runner should be connected and the status should be Idle.

5. Set the Secrets
   - Go to Secrets and variables > Actions > New repository secret
   - Add the following secrets and their values. We will use it in main.yaml
     ```
     AWS_ACCESS_KEY_ID
     AWS_SECRET_ACCESS_KEY
     AWS_REGION
     AWS_ECR_LOGIN_URI = <<your-aws-account-id>>.dkr.ecr.<<aws-region>>.amazonaws.com
     ```
6. Run the CI/CD pipeline and let it finish.
7. Go to EC2 inbound rules and add two custom TCP with ports 8000 and 5000.
8. Finally, check the app running on EC2 public ip.
