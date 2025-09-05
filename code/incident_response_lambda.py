import boto3
import uuid
import datetime

# Initialize clients
ec2 = boto3.client('ec2')
s3 = boto3.client('s3')
dynamodb = boto3.resource('dynamodb')
sns = boto3.client('sns')

# Hardcoded configuration
LOG_BUCKET = "incident-response-logs-345483430467"   # Make sure this bucket exists in us-east-1
TABLE_NAME = "IncidentMetadata"                     # DynamoDB table name in us-east-1
SNS_TOPIC_ARN = "arn:aws:sns:us-east-1:345483430467:IR-Alerts"  # Your SNS topic in us-east-1

def lambda_handler(event, context):
    instance_ids = []

    # Case 1: Manual test input
    if "instance_ids" in event:
        instance_ids = event["instance_ids"]

    # Case 2: GuardDuty event
    elif "detail" in event and "resource" in event["detail"]:
        try:
            instance_id = event["detail"]["resource"]["instanceDetails"]["instanceId"]
            if instance_id:
                instance_ids = [instance_id]
        except Exception as e:
            print(f"Could not extract instance ID from GuardDuty event: {e}")

    if not instance_ids:
        print("No instances to stop")
        return {"status": "no instances found"}

    try:
        # Stop EC2 instance(s)
        ec2.stop_instances(InstanceIds=instance_ids)
        print(f"Stopped instances: {instance_ids}")

        # Generate IncidentId + timestamp
        incident_id = str(uuid.uuid4())
        timestamp = datetime.datetime.utcnow().isoformat()

        # Log to S3
        log_content = f"IncidentId: {incident_id}, InstanceId: {instance_ids}, Action: stopped, Time: {timestamp}"
        s3.put_object(
            Bucket=LOG_BUCKET,
            Key=f'incident-log-{instance_ids[0]}.txt',
            Body=log_content
        )

        # Write to DynamoDB (with debug logging)
        table = dynamodb.Table(TABLE_NAME)
        response = table.put_item(
            Item={
                'IncidentId': incident_id,
                'InstanceId': instance_ids[0],
                'Action': 'stopped',
                'Timestamp': timestamp
            }
        )
        print(f"DynamoDB response: {response}")

        # Publish SNS notification
        message = f"⚠️ Incident {incident_id}: EC2 instance {instance_ids[0]} was stopped at {timestamp}."
        sns.publish(
            TopicArn=SNS_TOPIC_ARN,
            Message=message,
            Subject="Incident Response Alert"
        )

        return {
            "status": "success",
            "incident_id": incident_id,
            "stopped_instances": instance_ids
        }

    except Exception as e:
        print(f"Error: {e}")
        return {"status": "error", "message": str(e)}
