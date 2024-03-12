# coding=utf-8
"""
Copyright © 2020 U.S. TECH SOLUTIONS LICENSE

@version 0.2.0
Searcher services
@author <anujy647@simplifyvms.com>
"""
import json
import boto3
from botocore.exceptions import ClientError


def get_secret(env: str, secret_aws: str):
    """ function help to get aws secret manager """
    secret_name = f"{env}/{secret_aws}"
    region_name = "us-east-1"

    # Create a Secrets Manager client
    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name
    )

    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name
        )
    except ClientError as err:
        if err.response['Error']['Code'] == 'ResourceNotFoundException':
            print("The requested secret " + secret_name + " was not found")
        elif err.response['Error']['Code'] == 'InvalidRequestException':
            print("The request was invalid due to:", err)
        elif err.response['Error']['Code'] == 'InvalidParameterException':
            print("The request had invalid params:", err)
    else:
        if 'SecretString' in get_secret_value_response:
            secret = json.loads(get_secret_value_response['SecretString'])
            return secret
