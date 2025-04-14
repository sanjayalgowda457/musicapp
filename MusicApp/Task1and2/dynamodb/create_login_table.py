import boto3
from botocore.exceptions import ClientError

# Connect to DynamoDB (update region if needed)
dynamodb = boto3.resource('dynamodb', region_name='us-east-1')  # or us-west-2

# Create table
def create_login_table():
    try:
        # Create 'login' table with 'email' as the primary key
        table = dynamodb.create_table(
            TableName='login',
            KeySchema=[{'AttributeName': 'email', 'KeyType': 'HASH'}],  # Partition key (HASH key)
            AttributeDefinitions=[{'AttributeName': 'email', 'AttributeType': 'S'}],  # Define 'email' as string type
            ProvisionedThroughput={'ReadCapacityUnits': 5, 'WriteCapacityUnits': 5}  # Set read/write capacity units
        )
        table.wait_until_exists()  # Wait until the table creation is complete
        print(" Login table created successfully.")
    except ClientError as e:
        # Handle the exception if the table already exists
        if e.response['Error']['Code'] == 'ResourceInUseException':
            print("Table already exists.")
        else:
            print(f" Error: {e}")

# Populate users
def populate_users(student_id, first_name, last_name):
    # Access the 'login' table
    table = dynamodb.Table('login')

    # Insert 10 sample users with incremental email and username
    for i in range(10):
        email = f"{student_id}{i}@student.rmit.edu.au"  # Generate email based on student ID
        username = f"{first_name}{last_name}{i}"  # Generate username based on first and last name
        password = str(i).zfill(6)  # Set a 6-digit password (zero-padded)

        # Put the user data into the table
        table.put_item(
            Item={
                'email': email,
                'user_name': username,
                'password': password
            }
        )

    print("****10 users inserted into 'login' table.****")

# Run this script directly
if __name__ == "__main__":
    # Create the login table and populate with sample users
    create_login_table()
    populate_users("s1234567", "Sanjay", "Lucifer")
