import boto3
import json

# Initialize DynamoDB resource and access the 'subscription' table
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('subscription')

# Lambda function handler for removing a subscription
def lambda_handler(event, context):
    try:
        # Parse the request body from the event
        body = json.loads(event['body'])
        email = body.get('email')
        title = body.get('title')
        artist = body.get('artist')

        # Validate required fields
        if not email or not title or not artist:
            return _response(400, {"error": "Missing email, title, or artist"})

        # Construct the composite key used in DynamoDB
        song_key = f"{title}#{artist}"

        # Delete the subscription item based on the primary key
        table.delete_item(
            Key={
                'email': email,
                'song_key': song_key
            }
        )

        # Return success response
        return _response(200, {"message": "Subscription removed"})

    except Exception as e:
        # Handle any exceptions and return error response
        return _response(500, {"error": str(e)})

# Helper function to format HTTP responses with headers
def _response(status_code, body):
    return {
        "statusCode": status_code,
        "headers": {
            "Access-Control-Allow-Origin": "*",   # Enable CORS
            "Access-Control-Allow-Headers": "*",  # Allow all headers
            "Access-Control-Allow-Methods": "*"   # Allow all HTTP methods
        },
        "body": json.dumps(body)  # Convert body to JSON string
    }
