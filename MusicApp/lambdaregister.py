import boto3
import json
import re

# Initialize DynamoDB resource and reference the 'login' table
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('login')

# Lambda function handler for user registration
def lambda_handler(event, context):
    try:
        # Parse request body
        body = json.loads(event['body'])
        email = body.get('email')
        user_name = body.get('user_name')
        password = body.get('password')

        # Ensure all fields are provided
        if not email or not user_name or not password:
            return _response(400, {"error": "All fields are required."})

        # Validate email format using regular expression
        email_regex = r"^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,6}$"
        if not re.match(email_regex, email):
            return _response(400, {"error": "Invalid email format."})

        # Check if the email already exists in the table
        response = table.get_item(Key={'email': email})
        if 'Item' in response:
            return _response(409, {"error": "The email already exists"})

        # Save new user record to DynamoDB
        table.put_item(Item={
            'email': email,
            'user_name': user_name,
            'password': password  # Note: For production, store hashed password instead
        })

        # Return success message
        return _response(200, {"message": "Registration successful"})

    except Exception as e:
        # Return error response if exception occurs
        return _response(500, {"error": str(e)})

# Helper function to format HTTP responses
def _response(status_code, body):
    return {
        "statusCode": status_code,
        "headers": {
            "Access-Control-Allow-Origin": "*",  # Allow all origins (CORS)
            "Access-Control-Allow-Headers": "*",  # Allow all headers
            "Access-Control-Allow-Methods": "*"   # Allow all HTTP methods
        },
        "body": json.dumps(body)  # Convert response body to JSON string
    }
