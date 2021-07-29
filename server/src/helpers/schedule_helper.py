import os
import boto3
from botocore.config import Config
import random
import json


aws_config = Config(
    region_name = 'us-east-1',
    signature_version = 'v4',
    retries = {
        'max_attempts': 10,
        'mode': 'standard'
    }
)

def create_schedule(hour, event_guid, payload):

    #hard coded for everyday
    schedule = "cron(0 {} * * ? *)".format(str(hour))

    event_client = boto3.client('events',
                                aws_access_key_id=os.environ.get("AWS_ACCESS_KEY"),
                                aws_secret_access_key=os.environ.get("AWS_SECRET_KEY"),
                                config=aws_config)

    lambda_clnt = boto3.client('lambda',
                                aws_access_key_id=os.environ.get("AWS_ACCESS_KEY"),
                                aws_secret_access_key=os.environ.get("AWS_SECRET_KEY"),
                                config=aws_config
                                )

    # Create a rule that's scheduled to run every day minutes
    rslt = event_client.put_rule(Name=str(event_guid),
                                ScheduleExpression=schedule,                                                                            
                                State='ENABLED')

    rslt = lambda_clnt.add_permission(FunctionName=os.environ.get('LAMBDA_ARN'),
                                  StatementId=str(random.randint(0, 100000000)),
                                  Action='lambda:InvokeFunction',
                                  Principal='events.amazonaws.com',
                                  SourceArn=rslt['RuleArn'])

    rslt = event_client.put_targets(Rule=str(event_guid),
                                    Targets=[
                                        {
                                            'Arn': os.environ.get('LAMBDA_ARN'),
                                            'Id': os.environ.get('LAMBDA_ID'),
                                            'Input':str(json.dumps(payload))
                                        }   
                                        ])

    return event_guid