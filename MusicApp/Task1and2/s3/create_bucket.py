import boto3
from botocore.exceptions import ClientError

# Function to create an S3 bucket
def create_bucket(bucket_name, region='us-east-1'):
    s3 = boto3.client('s3', region_name=region)  # Initialize S3 client

    try:
        # Bucket creation logic varies slightly for the 'us-east-1' region
        if region == 'us-east-1':
            s3.create_bucket(Bucket=bucket_name)  # No LocationConstraint needed
        else:
            s3.create_bucket(
                Bucket=bucket_name,
                CreateBucketConfiguration={'LocationConstraint': region}  # Specify region for other locations
            )
        print(f" Bucket '{bucket_name}' created successfully.")  # Success message

    except ClientError as e:
        # Handle case where the bucket already exists and is owned by the user
        if e.response['Error']['Code'] == 'BucketAlreadyOwnedByYou':
            print(f"Bucket '{bucket_name}' already exists and is owned by you.")
        # Handle case where the bucket name is taken globally
        elif e.response['Error']['Code'] == 'BucketAlreadyExists':
            print(f" Bucket name '{bucket_name}' is already taken globally.")
        # Handle any other errors
        else:
            print(f" Error: {e}")

# Run the function if the script is executed directly
if __name__ == "__main__":
    bucket_name = 'a1-music-image'  # Define your bucket name (must be globally unique)
    create_bucket(bucket_name, region='us-east-1')  # Create bucket in specified region
