import os
import logging
from flask import Flask, request
import telebot
from telebot.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    CopyTextButton
)

# =========================
# CONFIG
# =========================

BOT_TOKEN = os.getenv("BOT_TOKEN")
RENDER_EXTERNAL_URL = os.getenv("RENDER_EXTERNAL_URL", "").rstrip("/")
PORT = int(os.getenv("PORT", "10000"))

if not BOT_TOKEN:
    raise RuntimeError("BOT_TOKEN environment variable is missing.")

bot = telebot.TeleBot(BOT_TOKEN, parse_mode="HTML")
app = Flask(__name__)

logging.basicConfig(level=logging.INFO)

# =========================
# BUTTON STYLE
# =========================

def copy_button(text):
    """
    Telegram CopyText button.
    User can copy the value with one tap.
    """
    return InlineKeyboardButton(
        text="📋 COPY",
        copy_text=CopyTextButton(text=text)
    )


def home_keyboard():
    kb = InlineKeyboardMarkup(row_width=2)

    kb.add(
        InlineKeyboardButton("🧩 Extract Emoji", callback_data="extract"),
        InlineKeyboardButton("ℹ️ Help", callback_data="help")
    )

    return kb


# =========================
# START
# =========================

@bot.message_handler(commands=["start"])
def start(message):
    text = (
        "👋 <b>Custom Emoji Extractor</b>\n\n"
        "Custom emoji wala message mujhe send/forward karo.\n\n"
        "Main uska:\n"
        "🆔 Custom Emoji ID\n"
        "😀 Emoji\n"
        "📋 One-Tap Copy Button\n\n"
        "de dunga."
    )

    bot.send_message(
        message.chat.id,
        text,
        reply_markup=home_keyboard()
    )


# =========================
# HELP
# =========================

@bot.message_handler(commands=["help"])
def help_command(message):
    text = (
        "🧩 <b>Custom Emoji Extractor Help</b>\n\n"
        "1️⃣ Telegram ka custom emoji message bhejo.\n"
        "2️⃣ Bot automatically ID detect karega.\n"
        "3️⃣ <b>📋 COPY</b> par tap karke ID copy karo.\n\n"
        "Agar multiple custom emojis hain, "
        "to bot sabhi IDs show karega."
    )

    bot.send_message(
        message.chat.id,
        text,
        reply_markup=home_keyboard()
    )


# =========================
# EXTRACT CUSTOM EMOJIS
# =========================

def extract_from_entities(text, entities):
    results = []

    if not text or not entities:
        return results

    for entity in entities:
        if entity.type == "custom_emoji":
            custom_id = entity.custom_emoji_id

            if custom_id:
                # Entity offset/length UTF-16 based hota hai.
                # Simple readable preview ke liye text return kar rahe hain.
                results.append({
                    "id": str(custom_id),
                    "offset": entity.offset,
                    "length": entity.length
                })

    return results


def send_results(message, results):
    if not results:
        bot.reply_to(
            message,
            "❌ <b>Custom Emoji nahi mila.</b>\n\n"
            "Telegram ka actual custom emoji message bhejo."
        )
        return

    # Duplicate IDs hatao, order preserve rahega
    unique_ids = list(dict.fromkeys(item["id"] for item in results))

    bot.send_message(
        message.chat.id,
        f"✅ <b>{len(unique_ids)} Custom Emoji ID found</b>"
    )

    for index, emoji_id in enumerate(unique_ids, 1):

        kb = InlineKeyboardMarkup()
        kb.add(copy_button(emoji_id))

        bot.send_message(
            message.chat.id,
            (
                f"🧩 <b>Custom Emoji #{index}</b>\n\n"
                f"🆔 <code>{emoji_id}</code>"
            ),
            reply_markup=kb
        )


# =========================
# MESSAGE HANDLER
# =========================

@bot.message_handler(
    content_types=[
        "text",
        "photo",
        "video",
        "animation",
        "document",
        "audio",
        "voice"
    ]
)
def handle_message(message):

    results = []

    # Normal text
    if message.text and message.entities:
        results.extend(
            extract_from_entities(
                message.text,
                message.entities
            )
        )

    # Caption
    if message.caption and message.caption_entities:
        results.extend(
            extract_from_entities(
                message.caption,
                message.caption_entities
            )
        )

    send_results(message, results)


# =========================
# STICKER HANDLER
# =========================

@bot.message_handler(content_types=["sticker"])
def handle_sticker(message):

    sticker = message.sticker

    # Telegram custom emoji sticker
    custom_id = getattr(sticker, "custom_emoji_id", None)

    if custom_id:
        kb = InlineKeyboardMarkup()
        kb.add(copy_button(str(custom_id)))

        bot.reply_to(
            message,
            (
                "🧩 <b>Custom Emoji Sticker</b>\n\n"
                f"🆔 <code>{custom_id}</code>"
            ),
            reply_markup=kb
        )
        return

    bot.reply_to(
        message,
        "❌ Is sticker mein Custom Emoji ID nahi mili."
    )


# =========================
# CALLBACK BUTTONS
# =========================

@bot.callback_query_handler(func=lambda call: call.data == "help")
def callback_help(call):

    bot.answer_callback_query(call.id)

    text = (
        "🧩 <b>Custom Emoji Extractor</b>\n\n"
        "Custom emoji ko directly bot ko send ya forward karo.\n"
        "Bot ID detect karega aur 📋 COPY button dega."
    )

    bot.send_message(
        call.message.chat.id,
        text
    )


@bot.callback_query_handler(func=lambda call: call.data == "extract")
def callback_extract(call):

    bot.answer_callback_query(call.id)

    bot.send_message(
        call.message.chat.id,
        "🧩 Ab custom emoji wala message mujhe bhejo."
    )


# =========================
# WEBHOOK
# =========================

@app.route("/", methods=["GET"])
def home():
    return "Custom Emoji Bot is running.", 200


@app.route("/health", methods=["GET"])
def health():
    return "OK", 200


@app.route("/telegram/webhook", methods=["POST"])
def telegram_webhook():

    try:
        json_string = request.get_data().decode("utf-8")
        update = telebot.types.Update.de_json(json_string)
        bot.process_new_updates([update])

        return "OK", 200

    except Exception as e:
        logging.exception("Webhook error: %s", e)
        return "ERROR", 500


# =========================
# SET WEBHOOK
# =========================

def setup_webhook():

    if not RENDER_EXTERNAL_URL:
        logging.warning(
            "RENDER_EXTERNAL_URL not found. "
            "Webhook was not automatically configured."
        )
        return

    webhook_url = (
        f"{RENDER_EXTERNAL_URL}/telegram/webhook"
    )

    try:
        bot.remove_webhook()
        bot.set_webhook(url=webhook_url)

        logging.info(
            "Webhook set successfully: %s",
            webhook_url
        )

    except Exception as e:
        logging.exception(
            "Webhook setup failed: %s",
            e
        )


# =========================
# RUN
# =========================

if __name__ == "__main__":

    setup_webhook()

    app.run(
        host="0.0.0.0",
        port=PORT
    )
