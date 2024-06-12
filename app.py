import json
import logging
from fastapi import FastAPI, Request
from slack_bolt.async_app import AsyncApp
from slack_bolt.adapter.fastapi.async_handler import AsyncSlackRequestHandler
from slack_sdk.web.async_client import AsyncWebClient
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
    logger.info('call /slack/messages')
    body = await request.json()
    logger.info(f'body: {body}')
    if "challenge" in body:
        return {"challenge": body["challenge"]}
    return await slack_handler.handle(request)

# Define lazy listener for handling messages
@app.event("message")
async def handle_message_events(event, say, ack, logger):
    await ack()  # Acknowledge the event immediately
    logger.info(f"Message event received: {event}")
    asyncio.create_task(process_message(event, say))

# Define lazy listener for handling mentions
@app.event("app_mention")
async def handle_mention_events(event, say, ack, logger):
    await ack()  # Acknowledge the event immediately
    logger.info(f"Mention event received: {event}")
    asyncio.create_task(process_mention(event, say))

# Asynchronous task processing
async def process_message(event, say):
    logger.info("process_message started")
    await asyncio.sleep(5)  # Simulate a long-running process
    await say(f"Received your message: {event['text']}")

async def process_mention(event, say):
    logger.info("process_mention started")
    await asyncio.sleep(5)  # Simulate a long-running process
    await say(f"Hello <@{event['user']}>! How can I help you?")

# Define a test endpoint
@api.get("/test")
async def test(request: Request):
    response = await client.chat_postMessage(
        channel='#general',  # Replace with your channel ID or name
        text="Test message from bot"
    )
    logger.info(f"Test message response: {response}")
    return {"status": "Test message sent"}

# Lambda handler
logger.info('Starting up')
handler = Mangum(api)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(api, host="0.0.0.0", port=8000)
