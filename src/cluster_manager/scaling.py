import os
import logging
import boto3
from botocore.exceptions import ClientError, NoCredentialsError

# Configure logging
logging.basicConfig(
    filename='cluster.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def get_aws_client():
    """Initialize AWS EC2 client with secure credentials"""
    try:
        aws_access_key = os.getenv("AWS_ACCESS_KEY_ID")
        aws_secret_key = os.getenv("AWS_SECRET_ACCESS_KEY")

        if not aws_access_key or not aws_secret_key:
            raise ValueError("AWS credentials missing in environment")

        return boto3.client(
            'ec2',
            aws_access_key_id=aws_access_key,
            aws_secret_access_key=aws_secret_key,
            region_name='us-east-1'
        )

    except (NoCredentialsError, ValueError) as e:
        logger.error(f"AWS Credential Error: {str(e)}")
        raise

def scale_servers(cpu_usage: float) -> str:
    """Auto-scale EC2 instances based on CPU usage"""
    try:
        ec2 = get_aws_client()

        if cpu_usage > 80:
            response = ec2.start_instances(
                InstanceIds=['i-123456'],
                DryRun=False
            )
            logger.info(f"Started instances: {response}")
            return "Scaling out - New instance launched 🚀"

        elif cpu_usage < 20:
            response = ec2.stop_instances(
                InstanceIds=['i-123456'],
                DryRun=False
            )
            logger.info(f"Stopped instances: {response}")
            return "Scaling in - Instance stopped 🛑"

        else:
            logger.info(f"CPU at {cpu_usage}% - No action needed")
            return "No scaling required ⚖️"

    except ClientError as e:
        error_msg = f"AWS API Error: {e.response['Error']['Message']}"
        logger.error(error_msg)
        return error_msg

    except Exception as e:
        error_msg = f"Unexpected Error: {str(e)}"
        logger.error(error_msg)
        return error_msg
