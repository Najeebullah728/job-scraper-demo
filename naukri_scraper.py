import requests
from bs4 import BeautifulSoup
import boto3
import json

# Initialize AWS SQS client
sqs = boto3.client('sqs', region_name='us-east-1')  # Use your region here
queue_url = 'YOUR_SQS_QUEUE_URL'  # Replace with your actual SQS URL

def get_job_links(url):
    """Scrape job links from the given URL."""
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Example: Find job links from a sitemap or job listing page
    job_links = []
    for job in soup.find_all('a', class_='job-link'):
        job_links.append(job.get('href'))
    
    return job_links

def send_to_sqs(job_links):
    """Send extracted job links to AWS SQS."""
    for link in job_links:
        message_body = json.dumps({'job_url': link})
        sqs.send_message(
            QueueUrl=queue_url,
            MessageBody=message_body
        )
        print(f"Job link sent to SQS: {link}")

if __name__ == "__main__":
    job_urls = ['https://www.naukri.com/jobs']  # Replace with sitemap URL or job listing page URLs
    for url in job_urls:
        links = get_job_links(url)
        send_to_sqs(links)
