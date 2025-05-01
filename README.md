# 🎵 Music Subscription Web Application (AWS Cloud-Based)

A modern, serverless music subscription platform built on AWS. This web application allows users to register, search music using natural queries, and manage their favorite tracks — all via a clean and responsive interface.

This project serves as a real-world demonstration of full-stack cloud engineering using serverless technologies, real-time data handling, and regex-powered search.

---

## 🚀 Features

### 🔐 Secure User Authentication
* Login and registration implemented with AWS Lambda, API Gateway, and DynamoDB.

### 🔍 Advanced Music Search with Regex (NLP-style)
* Search the music catalog with natural, human-readable queries like:
- `Find songs by Elton John released in 1973`
- `All versions of Rivers of Babylon`

### ❤️ Personalized Subscriptions
* Users can subscribe/unsubscribe to tracks. Each user's choices are stored and retrieved dynamically from DynamoDB.

### 🖼️ Artist Image Management with S3
* Artist images are securely served using Amazon S3 with presigned URLs.

### 💻 Clean, Responsive UI
* Frontend built with HTML, CSS, and JavaScript. Designed with a Spotify-inspired aesthetic.

### ☁️ Fully Serverless Architecture
* All backend logic is handled through AWS Lambda and exposed via API Gateway. Music metadata and subscriptions are stored in DynamoDB.

---

## 🧱 Tech Stack

| Layer         | Technology                         |
|---------------|-------------------------------------|
| Frontend      | HTML, CSS, JavaScript              |
| Backend       | AWS Lambda (Python)                |
| API           | AWS API Gateway (REST)             |
| Database      | DynamoDB                           |
| Storage       | Amazon S3 (Presigned URLs)         |
| Hosting       | EC2 (Ubuntu + Apache2)             |
| NLP Queries   | Regex                              |

---

## 🔧 Quick Start Guide

### 1. Clone the Repository


* git clone https://github.com/your-username/music-subscription-app.git
* cd music-subscription-app

### 2. Create DynamoDB Tables

* python create_music_table.py
* python create_subscription_table.py

### 3. Upload Music Data and Artist Images

* python load_music_data.py
* python upload_artist_images.py

### 4. Launch EC2 & Host Frontend
* Launch an Ubuntu EC2 instance

* Install Apache2:

 * sudo apt update
 * sudo apt install apache2
 * Copy frontend files to /var/www/html/

### 5. Deploy Lambda Functions and Set Up API Gateway
* Deploy Python Lambda functions for login, register, search, subscribe, remove subscriptions, NLP query.

### Create REST API endpoints in API Gateway and link them to Lambda functions

* Update your HTML/JS files with the correct API Gateway URLs

### 📁 Project Structure

musicapp/
* create_music_table.py
* create_subscription_table.py
* load_music_data.py
* upload_artist_images.py
* createbucket.py
* login.html
* register.html
* main.html


### 🌱 Future Enhancements
* 🎧 Add audio previews for tracks

* 📊 Build a user analytics dashboard

* 👤 Introduce user profile customization

* 🔐 Switch to JWT-based authentication

🎼 Integrate album metadata and lyrics

### 🙋‍♂️ About the Developer
* Sanjay Addihally Lakshmegowda
* Cloud & Python Developer 
* https://www.linkedin.com/in/sanjay-al47/

