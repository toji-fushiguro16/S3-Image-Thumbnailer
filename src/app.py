import io
import os
from urllib.parse import unquote_plus

import boto3
from PIL import Image, UnidentifiedImageError

s3 = boto3.client("s3")
OUTPUT_BUCKET = os.environ["OUTPUT_BUCKET"]
MAX_SIZE = (640, 640)


def handler(event, _context):
    for record in event.get("Records", []):
        source_bucket = record["s3"]["bucket"]["name"]
        key = unquote_plus(record["s3"]["object"]["key"])
        if not key.lower().endswith((".jpg", ".jpeg", ".png")):
            continue
        original = s3.get_object(Bucket=source_bucket, Key=key)["Body"].read()
        try:
            with Image.open(io.BytesIO(original)) as image:
                image.thumbnail(MAX_SIZE)
                if image.mode not in ("RGB", "L"):
                    image = image.convert("RGB")
                output = io.BytesIO()
                image.save(output, format="JPEG", quality=85, optimize=True)
        except (UnidentifiedImageError, OSError):
            print(f"Skipping invalid image: s3://{source_bucket}/{key}")
            continue
        target = f"thumbnails/{os.path.splitext(key)[0]}.jpg"
        s3.put_object(Bucket=OUTPUT_BUCKET, Key=target, Body=output.getvalue(), ContentType="image/jpeg")
        print(f"Created s3://{OUTPUT_BUCKET}/{target}")
    return {"statusCode": 200}
