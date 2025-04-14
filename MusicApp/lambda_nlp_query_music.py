import json
import boto3
import re
from decimal import Decimal
from boto3.dynamodb.conditions import Attr

# Connect to DynamoDB and reference the 'music' table
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('music')

# Custom function to handle Decimal types in DynamoDB responses when converting to JSON
def decimal_default(obj):
    if isinstance(obj, Decimal):
        return int(obj) if obj % 1 == 0 else float(obj)  # Convert to int if whole number, else float
    raise TypeError(f"Object of type {type(obj).__name__} is not JSON serializable")

# Function to extract filter values from natural language query
def extract_filters(query):
    query = query.lower()  # Convert query to lowercase for case-insensitive matching
    filters = {}

    # Extract 4-digit year (e.g., 1999, 2020)
    year_match = re.search(r"\b(19|20)\d{2}\b", query)
    if year_match:
        filters["year"] = int(year_match.group(0))

    # Extract artist name after "by" or "of"
    artist_match = re.search(r"(?:by|of)\s+([a-zA-Z\s]+?)(?:\s+(?:in|from|on|with|called|named)\s+|$)", query)
    if artist_match:
        filters["artist"] = artist_match.group(1).strip().title()

    # Extract album name after "called", "named", or "from"
    album_match = re.search(r"(?:album\s+)?(?:called|named|from)\s+\"?([a-zA-Z0-9\s]+)\"?", query)
    if album_match:
        filters["album"] = album_match.group(1).strip().title()

    # Extract song title after "track", "song", or "title"
    title_match = re.search(r"(?:track|song|title)\s+(?:called|named)?\s*\"?([a-zA-Z0-9\s]+)\"?", query)
    if title_match:
        filters["title"] = title_match.group(1).strip().title()

    return filters  # Return dictionary of extracted filters

# Lambda handler function
def lambda_handler(event, context):
    try:
        # Parse incoming event body as JSON
        body = json.loads(event.get('body', '{}'))
        query = body.get('query', '')  # Get natural language query from body
        print(f"Received query: {query}")

        filters = extract_filters(query)  # Extract filters from query
        print(f"Extracted filters: {filters}")

        # Construct DynamoDB filter expression based on extracted filters
        filter_expression = None
        for key, value in filters.items():
            if key == 'year':
                condition = Attr(key).eq(value)  # Exact match for year
            else:
                condition = Attr(key).contains(value)  # Partial match for title, artist, album
            filter_expression = condition if not filter_expression else filter_expression & condition

        # Perform DynamoDB scan with or without filters
        if filter_expression:
            response = table.scan(FilterExpression=filter_expression)
            print(f"Final Scan Filter Expression: {filter_expression}")
        else:
            response = table.scan()  # No filters, return all items
            print("No filters provided. Returning full scan.")

        items = response.get('Items', [])  # Extract items from response
        print(f"Found {len(items)} items")

        # Return successful response with matching music records
        return {
            'statusCode': 200,
            'body': json.dumps({'results': items}, default=decimal_default),
            'headers': {
                'Access-Control-Allow-Origin': '*'  # Allow cross-origin requests
            }
        }

    except Exception as e:
        # Return error response if any exception occurs
        print(f"Error: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)}),
            'headers': {
                'Access-Control-Allow-Origin': '*'  # Allow cross-origin requests
            }
        }
