import boto3  

def scale_servers(cpu_usage):  
    ec2 = boto3.client('ec2')  
    if cpu_usage > 80:  
        ec2.start_instances(InstanceIds=['i-123456'])  
        print("Starting new server... 🚀")  
    elif cpu_usage < 20:  
        ec2.stop_instances(InstanceIds=['i-123456'])  
        print("Stopping server... 🛑")  
