import json
import boto3
from boto3.dynamodb.conditions import Attr
from decimal import Decimal

# Initialize DynamoDB resource and reference the 'music' table
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('music')

# Custom JSON encoder to convert Decimal values from DynamoDB to int or float
class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return int(obj) if obj % 1 == 0 else float(obj)  # Convert to int if whole number, else float
        return super(DecimalEncoder, self).default(obj)

# Lambda function handler
def lambda_handler(event, context):
    print("Received event:", event)

    # Set CORS headers
    headers = {
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Headers": "Content-Type",
        "Access-Control-Allow-Methods": "*"
    }

    # Handle CORS preflight requests
    if event.get("httpMethod") == "OPTIONS":
        return {
            "statusCode": 200,
            "headers": headers,
            "body": json.dumps("CORS preflight OK")
        }

    try:
        # Support both test events and real API Gateway events
        if isinstance(event, dict) and "body" in event:
            body = json.loads(event.get("body", '{}'))  # Parse JSON body
        else:
            body = event  # Handle direct test events

        # Get query parameters from request body
        title = body.get('title', "").strip()
        artist = body.get('artist', "").strip()
        album = body.get('album', "").strip()
        year = body.get('year', "").strip()

        filters = []  # List to store filter conditions

        # Add filter for title (case-insensitive)
        if title:
            filters.append(
                Attr('title').contains(title) |
                Attr('title').contains(title.lower()) |
                Attr('title').contains(title.upper())
            )

        # Add filter for artist (case-insensitive)
        if artist:
            filters.append(
                Attr('artist').contains(artist) |
                Attr('artist').contains(artist.lower()) |
                Attr('artist').contains(artist.upper())
            )

        # Add filter for album (case-insensitive)
        if album:
            filters.append(
                Attr('album').contains(album) |
                Attr('album').contains(album.lower()) |
                Attr('album').contains(album.upper())
            )

        # Add filter for year (handle both string and int types)
        if year:
            try:
                filters.append(
                    Attr('year').eq(year) |
                    Attr('year').eq(int(year))
                )
            except Exception as e:
                print("Year parsing failed:", str(e))
                filters.append(Attr('year').eq(year))  # Fallback if conversion fails

        # If no filters provided, return 400 Bad Request
        if not filters:
            return {
                "statusCode": 400,
                "headers": headers,
                "body": json.dumps({"error": "At least one field must be provided."})
            }

        # Combine all filter conditions using logical AND
        filter_expr = filters[0]
        for f in filters[1:]:
            filter_expr = filter_expr & f

        print("Using filter expression:", str(filter_expr))

        # Scan DynamoDB table with combined filter expression
        response = table.scan(FilterExpression=filter_expr)

        # Return results in response
        return {
            "statusCode": 200,
            "headers": headers,
            "body": json.dumps({"results": response.get("Items", [])}, cls=DecimalEncoder)
        }

    except Exception as e:
        # Handle any unexpected errors
        print("Error occurred:", str(e))
        return {
            "statusCode": 500,
            "headers": headers,
            "body": json.dumps({"error": "Something went wrong. " + str(e)})
        }
