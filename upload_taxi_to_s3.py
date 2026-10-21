"""
Project : NYC Taxi Trip Data Analysis
Phase   : 1 - Data Ingestion
Purpose : Upload real NYC TLC Parquet trip files to AWS S3
Platform: Windows
"""

import boto3
import os
import logging
from pathlib import Path
from botocore.exceptions import ClientError, NoCredentialsError

# ---------------------------------------------------------
# CONFIGURATION
# ---------------------------------------------------------
LOCAL_DATA_DIR = r"E:\nyc-taxi"
BUCKET_NAME = "nyc-taxi-raw-machindra-2026"      # UPDATE to your actual bucket name
S3_PREFIX = "raw-trips/"
AWS_REGION = "ap-south-1"                       # match your aws configure region

logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)s | %(message)s")
logger = logging.getLogger(__name__)


def get_s3_client():
    try:
        return boto3.client("s3", region_name=AWS_REGION)
    except NoCredentialsError:
        logger.error("AWS credentials not found. Run `aws configure` first.")
        raise


def create_bucket_if_not_exists(s3_client, bucket_name):
    try:
        s3_client.head_bucket(Bucket=bucket_name)
        logger.info(f"Bucket '{bucket_name}' already exists.")
    except ClientError:
        logger.info(f"Creating bucket '{bucket_name}'...")
        if AWS_REGION == "us-east-1":
            s3_client.create_bucket(Bucket=bucket_name)
        else:
            s3_client.create_bucket(
                Bucket=bucket_name,
                CreateBucketConfiguration={"LocationConstraint": AWS_REGION},
            )
        logger.info(f"Bucket '{bucket_name}' created.")


def upload_file_to_s3(s3_client, file_path, bucket_name, s3_key):
    file_size_mb = os.path.getsize(file_path) / (1024 * 1024)
    logger.info(f"Uploading {file_path.name} ({file_size_mb:.1f} MB)...")
    try:
        s3_client.upload_file(
            Filename=str(file_path),
            Bucket=bucket_name,
            Key=s3_key,
            ExtraArgs={"ServerSideEncryption": "AES256"},
        )
        logger.info(f"✅ Uploaded: {file_path.name} -> s3://{bucket_name}/{s3_key}")
    except ClientError as e:
        logger.error(f"Failed to upload {file_path.name}: {e}")


def upload_dataset(s3_client):
    data_path = Path(LOCAL_DATA_DIR)
    if not data_path.exists():
        logger.error(f"Local data directory '{LOCAL_DATA_DIR}' not found.")
        return

    # ⬇️ Now looking for PARQUET files
    files = list(data_path.glob("*.parquet"))
    if not files:
        logger.warning("No Parquet files found to upload.")
        return

    logger.info(f"Found {len(files)} file(s) to upload.")
    for file_path in files:
        s3_key = f"{S3_PREFIX}{file_path.name}"
        upload_file_to_s3(s3_client, file_path, BUCKET_NAME, s3_key)


if __name__ == "__main__":
    logger.info("=== Starting NYC Taxi Data Ingestion Pipeline ===")
    client = get_s3_client()
    create_bucket_if_not_exists(client, BUCKET_NAME)
    upload_dataset(client)
    logger.info("=== Ingestion Complete ===")