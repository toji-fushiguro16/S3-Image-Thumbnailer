# S3 Image Thumbnailer

Upload a JPEG image to an Amazon S3 source bucket. An S3 event invokes a Python Lambda function, which creates a 640×640 max JPEG thumbnail in a separate private bucket.

## Architecture

```text
Private source bucket → S3 ObjectCreated event → Lambda + Pillow → private thumbnail bucket
```

## Deploy

Prerequisites: AWS CLI, Docker, and AWS SAM CLI. From this folder run:

```bash
sam build --use-container
sam deploy --guided
```

The stack outputs the source and thumbnail bucket names. Upload a `.jpg` file with:

```bash
aws s3 cp photo.jpg s3://SOURCE_BUCKET/photos/photo.jpg
aws s3 ls s3://THUMBNAIL_BUCKET/thumbnails/photos/
```

The sample event filter accepts `.jpg` files. Update the template filter and handler if you want `.jpeg` or `.png` inputs.

## Clean up

```bash
sam delete
```

Both buckets are private. Remove their objects before deleting the stack if the deployment tool reports that a bucket is not empty. S3 and Lambda usage may incur charges; remove the stack after the demo.
