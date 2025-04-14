import boto3
from botocore.exceptions import ClientError

# Connect to DynamoDB
dynamodb = boto3.resource('dynamodb', region_name='us-east-1')  # Change region if needed

def create_music_table():
    try:
        # Create 'music' table with 'title' as partition key and 'artist' as sort key
        table = dynamodb.create_table(
            TableName='music',
            KeySchema=[
                {'AttributeName': 'title', 'KeyType': 'HASH'},   # Partition key
                {'AttributeName': 'artist', 'KeyType': 'RANGE'}  # Sort key
            ],
            AttributeDefinitions=[
                {'AttributeName': 'title', 'AttributeType': 'S'},   # Define 'title' as string
                {'AttributeName': 'artist', 'AttributeType': 'S'}   # Define 'artist' as string
            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 5,   # Read capacity
                'WriteCapacityUnits': 5   # Write capacity
            }
        )
        table.wait_until_exists()  # Wait until table is created
        print("✅ Music table created with title + artist keys.")
    except ClientError as e:
        # Handle the case where the table already exists
        if e.response['Error']['Code'] == 'ResourceInUseException':
            print(" Music table already exists.")
        else:
            print(f" Error: {e}")

# Run the function when script is executed directly
if __name__ == "__main__":
    create_music_table()
