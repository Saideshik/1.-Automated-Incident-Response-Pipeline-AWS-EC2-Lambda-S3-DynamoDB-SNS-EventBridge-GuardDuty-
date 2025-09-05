# AWS Automated Incident Response Pipeline

This project demonstrates a serverless **Incident Response Automation Pipeline** built on AWS.
It integrates **Amazon GuardDuty**, **EventBridge**, and **AWS Lambda** to automatically respond
to suspicious activity.

## 🚀 Features
- Detects threats via **GuardDuty**.
- Automates response with **Lambda**:
  - Stops/quarantines suspicious EC2 instances.
  - Logs incidents to **Amazon S3**.
  - Stores structured records in **DynamoDB**.
  - Sends real-time alerts via **SNS** (email/SMS).
- Fully serverless design, low maintenance.

## 🛠️ Architecture

Example: attack → detection → response → notification

GuardDuty → EventBridge → Lambda → EC2/S3/DynamoDB/SNS

## 📂 Project Structure

incident_response_pipeline/
1. code/incident_response_lambda.py   # AWS Lambda function
2. policies/incident_response_policy.json   # IAM policy
3 diagrams/Visual_pipeline_diagram.png     # Visual pipeline diagram
4 tests/stop_ec2_test.json               # Sample test event for Lambda
5 README.md

## 🧑‍💻 Skills Demonstrated
- AWS Lambda development (Python + boto3)
- Event-driven architecture with GuardDuty + EventBridge
- Incident automation (EC2 quarantine, forensic logging)
- Cloud security design with least privilege IAM policies
- Monitoring and alerting (S3, DynamoDB, SNS)


## ⚙️ Setup
1. Enable GuardDuty in your AWS account.
2. Create resources:
   - S3 bucket for logs
   - DynamoDB table (`IncidentMetadata`)
   - SNS topic for alerts
3. Deploy Lambda with the provided Python code.
4. Attach IAM role with least privilege permissions.

## ✅ Example Output
When triggered, the Lambda:
- Stops the suspicious EC2 instance
- Logs to S3
- Adds entry in DynamoDB
- Sends SNS alert email

Example record in DynamoDB:

IncidentId: 847328b4-4372-414c-92cb-4f78432f011b
InstanceId: i-0b89df24188ae6aeb
Action: stopped
Timestamp: 2025-09-04T19:12:47Z

