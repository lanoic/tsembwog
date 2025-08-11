import os, io, boto3
from botocore.exceptions import BotoCoreError, NoCredentialsError

MODEL_DIR = os.environ.get("MODEL_DIR", "/app/models")
USE_S3 = os.environ.get("USE_S3", "false").lower() == "true"
S3_BUCKET = os.environ.get("S3_BUCKET", "")
S3_PREFIX = os.environ.get("S3_PREFIX", "models/")

def local_path(name: str) -> str:
    os.makedirs(MODEL_DIR, exist_ok=True)
    return os.path.join(MODEL_DIR, name)

def save_bytes(name: str, data: bytes):
    if USE_S3 and S3_BUCKET:
        s3 = boto3.client("s3")
        s3.put_object(Bucket=S3_BUCKET, Key=S3_PREFIX + name, Body=data)
    else:
        p = local_path(name)
        with open(p, "wb") as f:
            f.write(data)

def load_bytes(name: str) -> bytes | None:
    if USE_S3 and S3_BUCKET:
        s3 = boto3.client("s3")
        try:
            obj = s3.get_object(Bucket=S3_BUCKET, Key=S3_PREFIX + name)
            return obj["Body"].read()
        except Exception:
            return None
    else:
        p = local_path(name)
        if not os.path.exists(p): return None
        with open(p, "rb") as f:
            return f.read()
