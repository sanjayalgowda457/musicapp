import boto3
import requests
import os
import json

# Define S3 bucket name and region
BUCKET_NAME = 'a1-music-image'  # Update this to your actual bucket name
REGION = 'us-east-1'  # or us-west-2

# Initialize S3 client
s3 = boto3.client('s3', region_name=REGION)

# Function to download images from URLs in JSON and upload them to S3
def download_and_upload_images(json_path):
    with open(json_path) as f:
        data = json.load(f)  # Load JSON data

        # Create a local directory for storing images
        os.makedirs('assets/images', exist_ok=True)

        uploaded = set()  # Track already uploaded image URLs to avoid duplicates

        # Iterate over each song entry
        for song in data['songs']:
            artist = song['artist'].replace(" ", "_")  # Replace spaces in artist name
            image_url = song['img_url']  # Get image URL

            if image_url in uploaded:
                continue  # Skip if image has already been processed

            image_name = image_url.split("/")[-1]  # Extract image file name
            local_path = f'assets/images/{image_name}'  # Define local file path

            try:
                # Download the image from the URL
                response = requests.get(image_url)
                with open(local_path, 'wb') as img_file:
                    img_file.write(response.content)
                print(f"Downloaded: {image_name}")

                # Upload the image to S3 under 'images/' folder
                s3.upload_file(local_path, BUCKET_NAME, f'images/{image_name}')
                print(f"Uploaded to S3: images/{image_name}")

                uploaded.add(image_url)  # Mark the image URL as uploaded

            except Exception as e:
                # Handle any errors during download or upload
                print(f"Failed for {image_url}: {e}")

# Run the function when script is executed directly
if __name__ == "__main__":
    download_and_upload_images("/data/2025a1.json")
