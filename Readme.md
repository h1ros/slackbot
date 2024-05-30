# Slack Bot with Python, FastAPI, and AWS Lambda

This repository contains a Slack bot built using Python, FastAPI, Slack Bolt, and AWS Lambda. The bot handles Slack events such as mentions and messages, and it is designed to handle processes that take more than 3 seconds using lazy listening.

## Features

- Handles Slack mentions and messages.
- Uses FastAPI for handling requests.
- Deployed on AWS Lambda using Docker.
- Automatic deployment via GitHub Actions.

## Prerequisites

- Python 3.8+
- Docker
- AWS account with permissions to create Lambda functions and API Gateway
- Slack App with necessary permissions

## Setup

### Step 1: Clone the Repository

```bash
git clone https://github.com/yourusername/slackbot.git
cd slackbot
```

### Step 2: Create a Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Set Up Your Slack App

1. Go to the [Slack API](https://api.slack.com/apps) and create a new app.
2. Enable "Event Subscriptions" and set the Request URL to your API Gateway endpoint (details below).
3. Subscribe to the `message.channels` and `app_mention` events.
4. Install the app to your workspace and obtain the OAuth token and signing secret.

### Step 5: Update `app.py` with Slack Credentials

Replace the placeholders with your actual Slack credentials in `app.py`:

```python
app = AsyncApp(token="xoxb-your-slack-bot-token", signing_secret="your-signing-secret")
```

### Step 6: Create Dockerfile

A `Dockerfile` is already provided in the repository.

### Step 7: Deploy to AWS Lambda

#### Build and Push Docker Image

1. Build your Docker image:

```bash
docker build -t your-slackbot-image .
```

2. Push your Docker image to AWS ECR:

- Follow the steps to create a repository and push your image to [AWS ECR](https://docs.aws.amazon.com/AmazonECR/latest/userguide/getting-started-cli.html).

#### Update Lambda Function

1. Create a new Lambda function in the AWS Lambda console.
2. Choose the "Container image" option.
3. Select your pushed Docker image from ECR.

### Step 8: Set Up API Gateway

1. Go to the AWS Management Console and navigate to the API Gateway service.
2. Create a new HTTP API.
3. Add a route with the path `/slack/messages` and method `POST`.
4. Integrate the route with your Lambda function.
5. Deploy the API and note the "Invoke URL".

### Step 9: Configure Slack

1. Go to the Slack API and navigate to your app.
2. Enable "Event Subscriptions".
3. Set the Request URL to `https://<your-api-id>.execute-api.<your-region>.amazonaws.com/slack/messages`.
4. Subscribe to `message.channels` and `app_mention` events.
5. Save changes.

## GitHub Actions for Automatic Deployment

This repository is configured with GitHub Actions to automatically build and deploy your Docker image to AWS Lambda whenever you push a new commit to the `main` branch.

### Setup GitHub Secrets

1. Go to your GitHub repository settings.
2. Navigate to "Secrets" and then "Actions".
3. Add the following secrets:
   - `AWS_ACCESS_KEY_ID`
   - `AWS_SECRET_ACCESS_KEY`
   - `ECR_REPOSITORY_URI` (your ECR repository URI)

### GitHub Actions Workflow

The `.github/workflows/deploy.yml` file is configured to build your Docker image, push it to ECR, and update your Lambda function.

## Testing

1. Mention your bot or send a message in a channel where the bot is present.
2. Check CloudWatch logs for your Lambda function to see if the events are processed correctly.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
