import boto3
import json

# Initialize DynamoDB resource and access the 'subscription' table
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('subscription')

# Lambda function handler for subscribing to a song
def lambda_handler(event, context):
    try:
        # Parse the request body from the event
        body = json.loads(event['body'])

        # Extract fields from the request body
        email = body.get('email')
        title = body.get('title')
        artist = body.get('artist')
        album = body.get('album')
        year = body.get('year')
        image_url = body.get('image_url')

        # Validate that all required fields are provided
        if not all([email, title, artist, album, year, image_url]):
            return _response(400, {"error": "Missing required fields"})

        # Construct a unique song key using title and artist
        song_key = f"{title.strip()}#{artist.strip()}"

        # Check if the user is already subscribed to the song
        existing = table.get_item(Key={'email': email, 'song_key': song_key})
        if 'Item' in existing:
            return _response(409, {"error": "Already subscribed to this song"})

        # Insert the new subscription into DynamoDB
        table.put_item(Item={
            'email': email,
            'song_key': song_key,
            'title': title,
            'artist': artist,
            'album': album,
            'year': year,
            'image_url': image_url
        })

        # Return a success response
        return _response(200, {"message": "Subscribed successfully"})

    except Exception as e:
        # Return an error response if something goes wrong
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
