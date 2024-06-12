from slack_bolt.async_app import AsyncApp
from slack_bolt.adapter.fastapi.async_handler import AsyncSlackRequestHandler
from fastapi import FastAPI, Request
from mangum import Mangum
import asyncio
from config import SLACK_BOT_TOKEN, SLACK_SIGNING_SECRET

# Initialize your Slack app
app = AsyncApp(token=SLACK_BOT_TOKEN, signing_secret=SLACK_SIGNING_SECRET)

# FastAPI app
api = FastAPI()

# Slack request handler
slack_handler = AsyncSlackRequestHandler(app)

# @api.post("/slack/messages")
# async def slack_events(request: Request):
#     return {'status': 200}
#     # return await slack_handler.handle(request)
@api.post("/slack/messages")
async def slack_events(request: Request):
    # logger.info('call /slack/messages')
    print('call /slack/messages')
    body = await request.json()
    print(f'body: {body}')
    if "challenge" in body:
        return {"challenge": body["challenge"]}
    return await slack_handler.handle(request)

# Define lazy listener for handling messages
@app.event("message")
async def handle_message_events(event, say, logger):
    logger.info(f"Message event received: {event}")
    print(f"Message event received: {event}")
    asyncio.create_task(process_message(event, say))

# Define lazy listener for handling mentions
@app.event("app_mention")
async def handle_mention_events(event, say, logger):
    logger.info(f"Mention event received: {event}")
    print(f"Mention event received:{event}")

    asyncio.create_task(process_mention(event, say))

# Asynchronous task processing
async def process_message(event, say):
    print(f"process_message started")

    # Simulate a long-running process
    await asyncio.sleep(5)
    await say(f"Received your message: {event['text']}")

async def process_mention(event, say):
    # Simulate a long-running process
    print(f"process_mention started")

    await asyncio.sleep(5)
    await say(f"Hello <@{event['user']}>! How can I help you?")

async def test_slack_message():
    from slack_sdk.web.async_client import AsyncWebClient
    client = AsyncWebClient(token=SLACK_BOT_TOKEN)
    response = await client.chat_postMessage(
        channel='#general', 
        text="Test message from bot"
    )
    logger.info(f"Test message response: {response}")

@api.get("/test")
async def test(request: Request):
    await test_slack_message()
    return {"status": "Test message sent"}

def respond_to_slack_within_3_seconds(body, ack):
    text = body.get("text")
    if text is None or len(text) == 0:
        ack(f":x: Usage: /start-process (description here)")
    else:
        ack(f"Accepted! (task: {body['text']})")

import time
def run_long_process(respond, body):
    time.sleep(5)  # longer than 3 seconds
    respond(f"Completed! (task: {body['text']})")

app.command("/start-process")(
    # ack() is still called within 3 seconds
    ack=respond_to_slack_within_3_seconds,
    # Lazy function is responsible for processing the event
    lazy=[run_long_process]
)
# Lambda handler
print('Starting up')
handler = Mangum(api)
