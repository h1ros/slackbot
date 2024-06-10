import os
from utils import secret_from_parameter_store
from pathlib import Path

ENVIRONMENT = os.environ.get("ENVIRONMENT", "prd")


def read_env_or_load(env_name, parameter_name):
    """
    Reads an environment variable or loads it from AWS SSM Parameter Store.

    Args:
        env_name (str): The name of the environment variable.
        parameter_name (str): The name of the parameter in AWS SSM Parameter Store.

    Returns:
        str: The value of the environment variable.
    """
    env_val = os.environ.get(env_name, "")

    if env_val == "":
        val = secret_from_parameter_store(parameter_name, ENVIRONMENT)
        os.environ[env_name] = val
        env_val = val
    return env_val


# Load .env if not running in AWS Lambda
if "AWS_EXECUTION_ENV" not in os.environ:
    from dotenv import load_dotenv

    # Get the folder this file is in:
    this_file_folder = os.path.dirname(os.path.realpath(__file__))
    load_dotenv(Path(this_file_folder) / ".env")


# secrets
SLACK_BOT_TOKEN = read_env_or_load("SLACK_BOT_TOKEN", "slack_bot_token")
SLACK_SIGNING_SECRET = read_env_or_load("SLACK_SIGNING_SECRET", "slack_signing_secret")
