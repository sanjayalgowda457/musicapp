import boto3
import json

# Initialize DynamoDB resource and access the 'login' table
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('login')

# Lambda function handler for user login
def lambda_handler(event, context):
    try:
        # Parse the request body from the event
        body = json.loads(event['body'])

        # Extract email and password from the body
        email = body.get('email')
        password = body.get('password')

        # Check if both email and password are provided
        if not email or not password:
            return _response(400, {"error": "Email and password required"})

        # Retrieve user data from DynamoDB based on the provided email
        response = table.get_item(Key={'email': email})
        user = response.get('Item')

        # If user exists and password matches, login is successful
        if user and user['password'] == password:
            return _response(200, {
                "message": "Login successful",
                "user_name": user['user_name'],
                "email": user['email']
            })
        else:
            # If email or password is incorrect, return an error response
            return _response(401, {"error": "email or password is invalid"})

    except Exception as e:
        # If an error occurs, return an error response
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
