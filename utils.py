import boto3
import logging
from langchain.docstore.document import Document

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def extract_relevant_content(raw_documents):
    """
    Extracts relevant content from raw Notion documents.

    Args:
        raw_documents (list): A list of raw Notion documents.

    Returns:
        list: A list of refined documents containing relevant content.
    """
    refined_documents = []
    for doc in raw_documents:
        metadata = doc.metadata
        answer = metadata.get('answer', '')
        question = metadata.get('question', '')
        page = Document(page_content=f"Long answer: {doc.page_content}\n Short answer: {answer}\n Question: {question}", metadata={})
        refined_documents.append(page)
    return refined_documents


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
        Name=f"/chambers/{env}/{parameter_name}", WithDecryption=True
    )
    return parameter["Parameter"]["Value"]
