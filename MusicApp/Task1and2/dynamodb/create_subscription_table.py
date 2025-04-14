import boto3

# Connect to DynamoDB
dynamodb = boto3.resource('dynamodb', region_name='us-east-1')  # change region if needed

# Define table name
table_name = 'subscription'

try:
    # Create 'subscription' table with 'email' as partition key and 'song_key' as sort key
    table = dynamodb.create_table(
        TableName=table_name,
        KeySchema=[
            {
                'AttributeName': 'email',
                'KeyType': 'HASH'  # Partition key
            },
            {
                'AttributeName': 'song_key',
                'KeyType': 'RANGE'  # Sort key
            }
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'email',
                'AttributeType': 'S'  # String type for email
            },
            {
                'AttributeName': 'song_key',
                'AttributeType': 'S'  # String type for song_key
            }
        ],
        BillingMode='PAY_PER_REQUEST'  # On-demand billing mode (no provisioned throughput)
    )

    # Notify that table creation has started
    print(f"Table creation initiated for '{table_name}'...")

    # Wait until the table is created and ready
    table.meta.client.get_waiter('table_exists').wait(TableName=table_name)
    print(f"Table '{table_name}' is ready!")

except Exception as e:
    # Handle any exceptions that occur during table creation
    print(f"Error creating table: {e}")
