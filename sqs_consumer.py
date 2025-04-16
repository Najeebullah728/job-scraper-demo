import boto3
import json

# Initialize AWS SQS client
sqs = boto3.client('sqs', region_name='us-east-1')  # Use your region here
queue_url = 'YOUR_SQS_QUEUE_URL'  # Replace with your actual SQS URL

def process_job_link(job_link):
    """Process each job link - for example, saving it to a database."""
    print(f"Processing job link: {job_link}")
    # Here, you can insert the job data into a database or save it to a file

def consume_from_sqs():
    """Consume messages from SQS and process them."""
    while True:
        response = sqs.receive_message(
            QueueUrl=queue_url,
            AttributeNames=['All'],
            MaxNumberOfMessages=10,
            WaitTimeSeconds=20
        )
        
        messages = response.get('Messages', [])
        if not messages:
            print("No messages in the queue.")
            continue
        
        for message in messages:
            job_data = json.loads(message['Body'])
            job_link = job_data['job_url']
            process_job_link(job_link)

            # Delete message after processing
            sqs.delete_message(
                QueueUrl=queue_url,
                ReceiptHandle=message['ReceiptHandle']
            )

if __name__ == "__main__":
    consume_from_sqs()
