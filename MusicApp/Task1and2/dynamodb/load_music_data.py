import boto3
import json

# Connect to DynamoDB
dynamodb = boto3.resource('dynamodb', region_name='us-east-1')  # Specify region
table = dynamodb.Table('music')  # Reference the 'music' table

# Function to load music data from a JSON file into DynamoDB
def load_music_data(json_path):
    with open(json_path) as f:
        data = json.load(f)  # Load JSON data from file

        # Iterate through each song in the JSON
        for song in data['songs']:
            # Insert song record into the 'music' table
            table.put_item(
                Item={
                    'title': song['title'],               # Song title (partition key)
                    'artist': song['artist'],             # Artist name (sort key)
                    'year': int(song['year']),            # Year of release (convert to int)
                    'album': song['album'],               # Album name
                    'image_url': song['img_url']          # URL of album cover or image
                }
            )

    print("Music data loaded into DynamoDB.")  # Success message

# Run the data loading function when script is executed directly
if __name__ == "__main__":
    load_music_data("/data/2025a1.json")
