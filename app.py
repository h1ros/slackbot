import json
import logging
from fastapi import FastAPI, Request
from slack_bolt.async_app import AsyncApp
from slack_bolt.adapter.fastapi.async_handler import AsyncSlackRequestHandler
from slack_sdk.web.async_client import AsyncWebClient
from slack_sdk.errors import SlackApiError
from mangum import Mangum
import asyncio
from config import SLACK_BOT_TOKEN, SLACK_SIGNING_SECRET

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize your Slack app with increased timeout
app = AsyncApp(token=SLACK_BOT_TOKEN, signing_secret=SLACK_SIGNING_SECRET)
client = AsyncWebClient(token=SLACK_BOT_TOKEN, timeout=30)  # Increase timeout to 30 seconds

# FastAPI app
api = FastAPI()

# Slack request handler
slack_handler = AsyncSlackRequestHandler(app)

@api.post("/slack/messages")
async def slack_events(request: Request):
    print('call /slack/messages')
    body = await request.json()
    print(f'body: {body}')
    if "challenge" in body:
        return {"challenge": body["challenge"]}
    return await slack_handler.handle(request)

# Define lazy listener for handling messages
@app.event("message")
async def handle_message_events(event, say, ack, logger):
    await ack()  # Acknowledge the event immediately
    print(f"Message event received: {event}")
    asyncio.create_task(process_message(event, sa, ack))

# Define lazy listener for handling mentions
@app.event("app_mention")
async def handle_mention_events(event, say, ack, logger):
    await ack()  # Acknowledge the event immediately
    print(f"Mention event received: {event}")
    asyncio.create_task(process_mention(event, say, ack))

# Asynchronous task processing with retry mechanism
async def process_message(event, say):
    print("process_message started")
    await asyncio.sleep(5)  # Simulate a long-running process
    await send_message(say, f"Received your message: {event['text']}")

async def process_mention(event, say, ack):
    print("process_mention started")

    await ack()
    print("ack() called")

    await asyncio.sleep(5)  # Simulate a long-running process
    print("asyncio.sleep(5) ended")
    print(f"send message: Hello <@{event['user']}>! How can I help you?")

    await send_message(say, f"Hello <@{event['user']}>! How can I help you?")

# Function to send message with retry logic
async def send_message(say, text, retries=3):
    for attempt in range(retries):
        try:
            await say(text)
            print(f"Message sent: {text}")
            return
        except SlackApiError as e:
            logger.error(f"Error sending message: {e.response['error']}")
            if attempt < retries - 1:
                print("Retrying...")
                await asyncio.sleep(2 ** attempt)  # Exponential backoff
            else:
                logger.error("Max retries reached. Giving up.")

# Define a test endpoint
@api.get("/test")
async def test(request: Request):
    response = await client.chat_postMessage(
        channel='#general',  # Replace with your channel ID or name
        text="Test message from bot"
    )
    print(f"Test message response: {response}")
    return {"status": "Test message sent"}

# Slash command handler
@app.command("/start-process")
async def start_process_command(ack, body, say):
    await ack()
    print(f"Command received: {body}")
    await send_message(say, f"Starting process as requested by <@{body['user_id']}>")

# Lambda handler
print('Starting up')
handler = Mangum(api)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(api, host="0.0.0.0", port=8000)
