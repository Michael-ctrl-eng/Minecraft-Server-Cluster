import logging  
import boto3  

# Set up logging (like a diary for your code)  
logging.basicConfig(  
    filename='cluster.log',  
    level=logging.INFO,  
    format='%(asctime)s - %(message)s'  
)  
logger = logging.getLogger(__name__)  

def scale_servers(cpu_usage):  
    try:  
        ec2 = boto3.client('ec2')  
        if cpu_usage > 80:  
            ec2.start_instances(InstanceIds=['i-123456'])  
            logger.info("Started new server! 🚀")  
        elif cpu_usage < 20:  
            ec2.stop_instances(InstanceIds=['i-123456'])  
            logger.info("Stopped server. 🛑")  
    except Exception as e:  
        logger.error(f"ERROR: {str(e)}")  
