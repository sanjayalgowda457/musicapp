# Music Subscription Web Application (AWS Cloud-Based)
 * Duration: Mar 2025 – Apr 2025
 * Tech Stack: AWS EC2, S3, Lambda, API Gateway, DynamoDB, HTML, CSS, JavaScript, Python, Regex (NLP)

Designed and deployed a fully cloud-based music subscription web application hosted on an AWS EC2 instance. The platform allows users to register, search, and subscribe to music tracks, featuring secure login, personalized subscription management, and seamless image handling from S3.

Key Features:
* User Authentication: Secure login and registration using DynamoDB and API Gateway with Lambda.
* Music Management: Structured music metadata stored in DynamoDB; enabled user-specific subscriptions with real-time updates.
* Advanced Search with NLP: Integrated a natural language-based query system using regex to support complex and intuitive user queries like “Find all songs of Jimmy Buffett in 1974” or “All versions of Rivers of Babylon”.
* AWS Integration:
  * Artist images fetched and displayed using S3.
  * All backend operations (CRUD) managed via Lambda functions and API Gateway.
  * Responsive Frontend: Built with HTML, CSS, and JavaScript to deliver a user-friendly, Spotify-inspired interface.
  * Deployment: Deployed on an Ubuntu EC2 instance, accessible via public DNS using Apache2 and HTTPS/HTTP protocols.
