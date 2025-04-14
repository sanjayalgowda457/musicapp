import boto3
import json
from boto3.dynamodb.conditions import Key
from decimal import Decimal

# Initialize DynamoDB and S3 clients
dynamodb = boto3.resource('dynamodb')
s3 = boto3.client('s3')
table = dynamodb.Table('subscription')

# S3 bucket and image folder prefix
BUCKET_NAME = 'a1-music-image'  # your S3 bucket name
FOLDER_PREFIX = 'images/'       # your S3 folder for images

# Custom JSON encoder to convert Decimal to int/float
class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return int(obj) if obj % 1 == 0 else float(obj)
        return super(DecimalEncoder, self).default(obj)

# Generate a pre-signed S3 URL for an artist's image
def generate_presigned_url(artist_name):
    # Clean artist name to match image key format
    key = FOLDER_PREFIX + artist_name.replace(" ", "").replace("-", "").replace("'", "").replace("&", "") + ".jpg"
    try:
        # Create a pre-signed URL valid for 7 days (604800 seconds)
        return s3.generate_presigned_url(
            'get_object',
            Params={'Bucket': BUCKET_NAME, 'Key': key},
            ExpiresIn=604800
        )
    except Exception as e:
        print(f"Failed to generate pre-signed URL for {key}: {e}")
        return ""

# Lambda function handler to fetch a user's subscriptions
def lambda_handler(event, context):
    try:
        # Get email from query string parameters
        email = event.get("queryStringParameters", {}).get("email")

        if not email:
            return _response(400, {"error": "Email is required"})

        # Query the subscription table for the user's subscriptions
        response = table.query(KeyConditionExpression=Key('email').eq(email))
        items = response.get('Items', [])

        # Clean up items and add pre-signed image URLs
        for item in items:
            item.pop('song_key', None)  # Remove song_key from response
            item['image_url'] = generate_presigned_url(item.get('artist', 'Unknown'))

        # Return the subscription list with image URLs
        return {
            "statusCode": 200,
            "headers": {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Headers": "*",
                "Access-Control-Allow-Methods": "*"
            },
            "body": json.dumps({"subscriptions": items}, cls=DecimalEncoder)
        }

    except Exception as e:
        # Return error if something goes wrong
        return _response(500, {"error": str(e)})

# Helper function to return an HTTP response
def _response(status_code, body):
    return {
        "statusCode": status_code,
        "headers": {
            "Access-Control-Allow-Origin": "*",   # Allow all origins (CORS)
            "Access-Control-Allow-Headers": "*",  # Allow all headers
            "Access-Control-Allow-Methods": "*"   # Allow all HTTP methods
        },
        "body": json.dumps(body)  # Convert response body to JSON string
    }
