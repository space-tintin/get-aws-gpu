import argparse
import boto3
import time
from botocore.exceptions import ClientError

boto3.setup_default_session(profile_name='default')

def start_ec2_instance(ec2, instance_id: str, max_retries: int = 5, backoff_factor: int = 2): 
    """ Restart an EC2 instance given its instance ID and region.
    """
    
    for attempt in range(max_retries + 1):
        try:
            ec2.start_instances(InstanceIds=[instance_id])
            print(f"Started instance {instance_id}")
            break
        except ClientError as error:
            if error.response['Error']['Code'] == 'IncorrectInstanceState':
                print(f"Instance {instance_id} is already running")
                break
            elif attempt < max_retries:
                print(f"Attempt {attempt + 1} of {max_retries + 1}: Instance {instance_id} not yet ready, waiting {backoff_factor ** attempt} seconds")
                time.sleep(backoff_factor ** attempt)
            else:
                raise error

def launch_instance(ec2, config: dict, max_retries: int = 5, backoff_factor: int = 2):
    """ Launch an EC2 instance given a config and region
    """
    
    for attempt in range(max_retries + 1):
        try:
            response = ec2.run_instances(**config)
            instance_id = response['Instances'][0]['InstanceId']
            print(f"Launched instance {instance_id}")
            return instance_id
        except ClientError as error:
            if error.response['Error']['Code'] == 'InsufficientInstanceCapacity':
                if attempt < max_retries:
                    wait_time = backoff_factor ** attempt
                    print(f"Attempt {attempt + 1} of {max_retries + 1}: Insufficient capacity for instance type, retrying in {wait_time} seconds...")
                    time.sleep(wait_time)
                else:
                    raise error
            else:
                raise error


def get_ec2_client(region):
    """Create an EC2 client for the specified region"""
    return boto3.client('ec2', region_name=region)

if __name__ == '__main__':
    # Parse the command line arguments
    parser = argparse.ArgumentParser(description="Manage AWS EC2 instances")
    parser.add_argument("action", choices=["launch", "start"], help="The action to perform: launch or start an instance")
    parser.add_argument("region", help="The AWS region")
    parser.add_argument("--instance_id", default=None, help="The id of the instance to start (required for 'start' action)")
    parser.add_argument("--ami", default=None, help="The AMI ID (required for 'launch' action)")
    parser.add_argument("--instance_type", default=None, help="The instance type (required for 'launch' action)")
    parser.add_argument("--subnet", default=None, help="The subnet ID (required for 'launch' action)")
    parser.add_argument("--security_group", default=None, help="The security group ID (required for 'launch' action)")
    args = parser.parse_args()
    
    ec2 = get_ec2_client(args.region)
    
    if args.action == "start":
        if args.instance_id is None:
            print("An instance id is required for 'start' action")
        else:
            start_ec2_instance(ec2, args.instance_id)
    else:
        # EC2 instance config. 
        if args.ami is None or args.instance_type is None or args.subnet is None or args.security_group is None:
            print("For 'launch' action, you need to specify --ami, --instance_type, --subnet, and --security_group")
        else:
            config = {
                "MaxCount": 1,
                "MinCount": 1,
                "ImageId": args.ami,
                "InstanceType": args.instance_type,
                "InstanceInitiatedShutdownBehavior": "stop",
                "DisableApiTermination": False,
                "EbsOptimized": True,
                "BlockDeviceMappings": [
                    {
                        "DeviceName": "/dev/sda1",
                        "Ebs": {
                            "DeleteOnTermination": True,
                            "VolumeSize": 100,
                            "VolumeType": "gp3",
                            "Encrypted": False,
                            "Iops": 3000,
                            "Throughput": 125
                        }
                    }
                ],
                "NetworkInterfaces": [
                    {
                        "DeviceIndex": 0,
                        "SubnetId": args.subnet,
                        "Groups": [args.security_group],
                        "AssociatePublicIpAddress": True
                    }
                ],
            }
            
            launch_instance(ec2, config)
