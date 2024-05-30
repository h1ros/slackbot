from slack_bolt.async_app import AsyncApp
from slack_bolt.adapter.fastapi.async_handler import AsyncSlackRequestHandler
from fastapi import FastAPI
from mangum import Mangum
import asyncio
from config import SLACK_BOT_TOKEN, SLACK_SIGNING_SECRET

# Initialize your Slack app
app = AsyncApp(token=SLACK_BOT_TOKEN, signing_secret=SLACK_SIGNING_SECRET)

# FastAPI app
api = FastAPI()

# Slack request handler
slack_handler = AsyncSlackRequestHandler(app)

@api.post("/slack/messages")
async def slack_events(request: fastapi.Request):
    return await slack_handler.handle(request)

# Define lazy listener for handling messages
@app.event("message")
async def handle_message_events(event, say, logger):
    logger.info(f"Message event received: {event}")
    asyncio.create_task(process_message(event, say))

# Define lazy listener for handling mentions
@app.event("app_mention")
async def handle_mention_events(event, say, logger):
    logger.info(f"Mention event received: {event}")
    asyncio.create_task(process_mention(event, say))

# Asynchronous task processing
async def process_message(event, say):
    # Simulate a long-running process
    await asyncio.sleep(5)
    await say(f"Received your message: {event['text']}")

async def process_mention(event, say):
    # Simulate a long-running process
    await asyncio.sleep(5)
    await say(f"Hello <@{event['user']}>! How can I help you?")

# Lambda handler
handler = Mangum(api)
