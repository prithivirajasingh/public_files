#!/usr/bin/env python3

import logging
import requests
import os
import pickle
import asyncio
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters
import re

# Telegram Bot API Token
ALPHAVPSONE_TELEGRAM_BOT_TOKEN = os.getenv("ALPHAVPSONE_TELEGRAM_BOT_TOKEN")  # Refer python_confidential_environment/custom.env

# qBittorrent Configuration (VPS)
VPS_DOMAIN = "alphaone.prithivirajasingh.com"
VPS_QBIT_URL = f"http://{VPS_DOMAIN}:8080/api/v2"
VPS_QBIT_USERNAME = "admin"
VPS_QBIT_PASSWORD = os.getenv("VPS_QBIT_PASSWORD")  # Refer python_confidential_environment/custom.env
VPS_COOKIE_FILE = "vps_qbit_cookies.pkl"

# qBittorrent Configuration (RVS)
RVS_DOMAIN = "rpi.prithivirajasingh.com"
RVS_QBIT_URL = f"http://{RVS_DOMAIN}:8080/api/v2"
RVS_QBIT_USERNAME = "admin"
RVS_QBIT_PASSWORD = os.getenv("RVS_QBIT_PASSWORD")  # Refer python_confidential_environment/custom.env
RVS_COOKIE_FILE = "rvs_qbit_cookies.pkl"

# Configure Logging
logging.basicConfig(format="%(asctime)s - %(levelname)s - %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)

# qBittorrent Session Management
vps_session = requests.Session()
rvs_session = requests.Session()

def load_qb_cookies(cookie_file, session):
    """Load existing qBittorrent cookies from file if they exist."""
    if os.path.exists(cookie_file):
        try:
            with open(cookie_file, 'rb') as f:
                session.cookies.update(pickle.load(f))
            return True
        except (pickle.PicklingError, EOFError):
            logger.error(f"Failed to load cookies from {cookie_file}")
    return False

def save_qb_cookies(cookie_file, session):
    """Save qBittorrent session cookies to file."""
    try:
        with open(cookie_file, 'wb') as f:
            pickle.dump(session.cookies, f)
    except pickle.PicklingError:
        logger.error(f"Failed to save cookies to {cookie_file}")

def check_qb_session(qbit_url, session):
    """Check if the current qBittorrent session is active."""
    try:
        response = session.get(f"{qbit_url}/auth/login")
        if response.status_code == 200 and response.text == "Ok.":
            return True
        return False
    except requests.RequestException:
        return False

def qb_login(qbit_url, username, password, session):
    """Log in to qBittorrent Web UI and save cookies."""
    data = {"username": username, "password": password}
    response = session.post(f"{qbit_url}/auth/login", data=data, verify=False)
    if response.status_code == 200 and response.text == "Ok.":
        return True
    logger.error(f"Login failed for {qbit_url}: {response.text}")
    return False

def add_to_vps(magnet_link):
    """Add a magnet link to VPS qBittorrent with session management."""
    session_active = load_qb_cookies(VPS_COOKIE_FILE, vps_session) and check_qb_session(VPS_QBIT_URL, vps_session)
    if not session_active:
        if not qb_login(VPS_QBIT_URL, VPS_QBIT_USERNAME, VPS_QBIT_PASSWORD, vps_session):
            return "⚠️ VPS qBittorrent Login Failed!"
        save_qb_cookies(VPS_COOKIE_FILE, vps_session)
    data = {"urls": magnet_link}
    response = vps_session.post(f"{VPS_QBIT_URL}/torrents/add", data=data, verify=False)
    return "✅ Magnet link added to VPS qBittorrent!" if response.status_code == 200 else f"⚠️ VPS qBittorrent Error: {response.text}"

def add_to_rvs(magnet_link):
    """Add a magnet link to RVS qBittorrent with session management."""
    session_active = load_qb_cookies(RVS_COOKIE_FILE, rvs_session) and check_qb_session(RVS_QBIT_URL, rvs_session)
    if not session_active:
        if not qb_login(RVS_QBIT_URL, RVS_QBIT_USERNAME, RVS_QBIT_PASSWORD, rvs_session):
            return "⚠️ RVS qBittorrent Login Failed!"
        save_qb_cookies(RVS_COOKIE_FILE, rvs_session)
    data = {"urls": magnet_link}
    response = rvs_session.post(f"{RVS_QBIT_URL}/torrents/add", data=data, verify=False)
    return "✅ Magnet link added to RVS qBittorrent!" if response.status_code == 200 else f"⚠️ RVS qBittorrent Error: {response.text}"

# Function to remove emojis from a string
def remove_emojis(text):
    emoji_pattern = re.compile("[\U00010000-\U0010ffff\U0000FE00-\U0000FFFF]", flags=re.UNICODE)
    return emoji_pattern.sub("", text)

async def start(update: Update, context) -> None:
    """Send a welcome message when the bot is started."""
    await update.message.reply_text("Bot is running! Send me a magnet link or use other commands!")

async def handle_content(update: Update, context) -> None:
    """Handles text messages including magnet links and text processing."""
    content = update.message.text.strip()

    if content.startswith("magnet:?"):
        magnet_parts = content.split('&')
        vps_result = add_to_vps(magnet_parts[0])
        rvs_result = add_to_rvs(magnet_parts[0])
        await update.message.reply_text(f"VPS: {vps_result}\nRVS: {rvs_result}")
    elif "[" in content and "]" in content:
        output = []
        previous_value = ""

        for line in content.splitlines():
            line = line.strip()
            if not line:
                continue

            if "[" in line and "]" in line:
                value = line.rsplit(":", 1)[-1].strip()
            else:
                value = line

            value = remove_emojis(value).lower()

            if previous_value:
                value = previous_value + " " + value
                previous_value = ""
            elif len(value.split()) == 1:
                previous_value = value
                continue

            output.append(value)

        output = [item.strip() for item in output]
        output = list(set(output))
        output = sorted(output)
        send_text = '\n'.join(output)
        await update.message.reply_text(f"{send_text}")
    else:
        await update.message.reply_text(f"Echoing:\n{content}")

async def error_handler(update: Update, context) -> None:
    """Log any errors that occur."""
    logger.error(f"Exception occurred: {context.error}", exc_info=True)
    if update and update.message:
        await update.message.reply_text("An error occurred. Please try again.")

async def clear_old_updates(application):
    """Fetch and clear all old updates to start processing only new messages."""
    try:
        # Get all pending updates
        updates = await application.bot.get_updates(timeout=10)
        if updates:
            # Get the ID of the latest update and set offset to skip all prior updates
            latest_update_id = updates[-1].update_id
            await application.bot.get_updates(offset=latest_update_id + 1, timeout=10)
            logger.info(f"Cleared {len(updates)} old updates. Starting with update_id {latest_update_id + 1}")
        else:
            logger.info("No old updates to clear.")
    except Exception as e:
        logger.error(f"Failed to clear old updates: {e}")

async def main():
    """Initialize the bot and register handlers."""
    logger.info("Starting bot...")
    application = Application.builder().token(ALPHAVPSONE_TELEGRAM_BOT_TOKEN).build()

    # Register handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_content))
    application.add_error_handler(error_handler)

    # Initialize the application
    await application.initialize()

    # Clear old updates before starting polling
    await clear_old_updates(application)

    logger.info("Bot polling started")
    try:
        # Start the application and updater manually
        await application.start()
        await application.updater.start_polling(allowed_updates=Update.ALL_TYPES)
        # Keep the bot running until interrupted
        while True:
            await asyncio.sleep(3600)  # Sleep to keep the loop alive
    except KeyboardInterrupt:
        logger.info("Bot stopped by user")
    finally:
        # Stop polling and shut down
        await application.updater.stop()
        await application.stop()
        await application.shutdown()

if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        loop.run_until_complete(main())
    finally:
        loop.run_until_complete(loop.shutdown_asyncgens())
        loop.close()
