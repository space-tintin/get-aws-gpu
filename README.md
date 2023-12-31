# AWS EC2 Instance Launcher Script
This Python script provides a simple command-line interface to launch Amazon Web Services (AWS) EC2 instances. It can launch new EC2 instances or start existing ones.

The script uses AWS's Boto3, the Amazon Web Services (AWS) Software Development Kit (SDK) for Python, which allows Python developers to write software that makes use of services like Amazon S3, Amazon EC2, and others.

The main intent is to have a script to attempt to launch gpu instances over and over again when availability is low

**Requirements**

Python 3.6+  
AWS account with necessary permissions to launch/start EC2 instances  
Boto3 Python library  

**Installation**   
To install the necessary Python library, run:

```sh
pip install -r requirements.txt
```

### Usage
You will need to provide the necessary command-line arguments. There are two main actions: launch and start.

For launching a new instance:


```sh
python ec2_manager.py launch <region> --ami <ami_id> --instance_type <instance_type> --subnet <subnet_id> --security_group <security_group_id>
```

For starting an existing instance:

```sh
python ec2_manager.py start <region> --instance_id <instance_id>
```

Replace `<region>`, `<ami_id>`, `<instance_type>`, `<subnet_id>`, `<security_group_id>`, and `<instance_id>` with your actual values.

**Command Line Arguments**
- `action`: The action to perform - either 'launch' to launch a new instance, or 'start' to start an existing instance  
- `region`: The AWS region where the action will be performed  
- `--ami`: The AMI ID (required for 'launch' action)  
- `--instance_type`: The instance type (required for 'launch' action)  
- `--subnet`: The subnet ID (required for 'launch' action)  
- `--security_group`: The security group ID (required for 'launch' action)  
- `--instance_id`: The ID of the instance to start (required for 'start' action)  
  
Note: Make sure to setup AWS Credentials before using the script. Refer to AWS Documentation for setting up the credentials.

**License**
This project is licensed under the MIT License