import boto3
from botocore.exceptions import ClientError

try:
    sts = boto3.client("sts", region_name="ap-south-1")
    identity = sts.get_caller_identity()
    print("SUCCESS — credentials are valid.")
    print("Account:", identity["Account"])
    print("User ARN:", identity["Arn"])
except ClientError as e:
    print("FAILED — credentials are invalid or missing permissions.")
    print("Error code:", e.response["Error"]["Code"])
    print("Error message:", e.response["Error"]["Message"])
except Exception as e:
    print("FAILED — unexpected error.")
    print(str(e))