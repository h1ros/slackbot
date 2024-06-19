import boto3
import logging
from botocore.exceptions import ClientError

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)



def get_secret():

    secret_name = "slackbot/prd"
    region_name = "us-west-2"

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
    except ClientError as e:
        # For a list of exceptions thrown, see
        # https://docs.aws.amazon.com/secretsmanager/latest/apireference/API_GetSecretValue.html
        raise e

    secret = get_secret_value_response['SecretString']
    print(f'secret: {secret}')

def secret_from_parameter_store(parameter_name, env):
    """
    Reads a secret from AWS SSM Parameter Store.

    Args:
        parameter_name (str): The name of the parameter.
        env (str): dev|prd.

    Returns:
        str: The value of the parameter.
    """
    ssm = boto3.client("ssm")
    parameter = ssm.get_parameter(
        Name=f"/slackbot/{env}/{parameter_name}", WithDecryption=True
    )
    return parameter["Parameter"]["Value"]
