import boto3
from cryptography.fernet import Fernet

from rns_task import settings

s3_client = boto3.client(
    's3',
    aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
    aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
)

def encrypt_file(file_content, key):
    """
    encrypting the file using fernet
    """
    fernet = Fernet(key)
    return fernet.encrypt(file_content)

def upload_to_s3(file_content, filename):
    """
    uploading the file to s3
    """
    s3_client.put_object(
        Bucket=settings.AWS_STORAGE_BUCKET_NAME,
        Key=filename,
        Body=file_content
    )
    file_url = f"https://{settings.AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com/{filename}"
    return file_url
