import os
import logging
from flask import Flask, request
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

BOT_TOKEN = os.getenv("BOT_TOKEN")
PORT = int(os.getenv("PORT", "10000"))
RENDER_EXTERNAL_URL = os.getenv("RENDER_EXTERNAL_URL", "").rstrip("/")

if not BOT_TOKEN:
    raise RuntimeError("BOT_TOKEN environment variable is missing")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

bot = telebot.TeleBot(BOT_TOKEN, parse_mode="HTML")
app = Flask(__name__)


# =========================
# BUTTONS
# =========================

def primary_button(text, callback_data):
    return InlineKeyboardButton(
        text=text,
        callback_data=callback_data,
        style="primary"
    )


def success_button(text, callback_data):
    return InlineKeyboardButton(
        text=text,
        callback_data=callback_data,
        style="success"
    )


def danger_button(text, callback_data):
    return InlineKeyboardButton(
        text=text,
        callback_data=callback_data,
        style="danger"
    )


def copy_button(emoji_id):
    try:
        from telebot.types import CopyTextButton

        return InlineKeyboardButton(
            text="📋 COPY ID",
            copy_text=CopyTextButton(text=str(emoji_id)),
            style="primary"
        )

    except Exception:
        return InlineKeyboardButton(
            text="📋 COPY ID",
            callback_data="copy_" + str(emoji_id),
            style="primary"
        )


def home_keyboard():
    kb = InlineKeyboardMarkup(row_width=2)

    kb.add(
        success_button(
            "🧩 EXTRACT EMOJI",
            "extract"
        ),
        primary_button(
            "ℹ️ HELP",
            "help"
        )
    )

    kb.add(
        danger_button(
            "✖ CLOSE",
            "close"
        )
    )

    return kb


# =========================
# START
# =========================

@bot.message_handler(commands=["start"])
def start_handler(message):

    text = (
        "👋 <b>Welcome to Custom Emoji Extractor</b>\n\n"
        "🧩 Send me any message containing Telegram "
        "custom emojis.\n\n"
        "I will extract the Custom Emoji ID for you.\n\n"
        "📋 You can copy each ID with one tap."
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
def help_handler(message):

    text = (
        "ℹ️ <b>HOW TO USE</b>\n\n"
        "1️⃣ Send a message containing custom emojis.\n"
        "2️⃣ I will detect all Custom Emoji IDs.\n"
        "3️⃣ Press 📋 COPY ID to copy an ID.\n\n"
        "✅ Multiple custom emojis are supported."
    )

    bot.send_message(
        message.chat.id,
        text,
        reply_markup=home_keyboard()
    )


# =========================
# EXTRACT CUSTOM EMOJIS
# =========================

def extract_custom_emojis(text, entities):

    emoji_ids = []

    if not entities:
        return emoji_ids

    for entity in entities:

        try:
            if (
                entity.type == "custom_emoji"
                and getattr(entity, "custom_emoji_id", None)
            ):
                emoji_ids.append(
                    str(entity.custom_emoji_id)
                )

        except Exception as e:
            logging.warning(
                "Entity error: %s",
                e
            )

    return emoji_ids


# =========================
# SEND RESULTS
# =========================

def send_results(chat_id, emoji_ids):

    unique_ids = list(dict.fromkeys(emoji_ids))

    # No emoji found
    if not unique_ids:

        bot.send_message(
            chat_id,
            "❌ <b>No Custom Emoji Found</b>\n\n"
            "Please send a message containing "
            "Telegram custom emojis.",
            reply_markup=home_keyboard()
        )

        return

    # IMPORTANT:
    # Fixed f-string
    bot.send_message(
        chat_id,
        f"✅ <b>{len(unique_ids)} Custom Emoji Found</b>",
        reply_markup=home_keyboard()
    )

    # Send each ID separately
    for emoji_id in unique_ids:

        text = (
            "🧩 <b>Custom Emoji ID</b>\n\n"
            f"<code>{emoji_id}</code>"
        )

        kb = InlineKeyboardMarkup()

        kb.add(
            copy_button(emoji_id)
        )

        bot.send_message(
            chat_id,
            text,
            reply_markup=kb
        )


# =========================
# TEXT MESSAGES
# =========================

@bot.message_handler(
    content_types=["text"]
)
def text_handler(message):

    emoji_ids = extract_custom_emojis(
        message.text or "",
        message.entities
    )

    send_results(
        message.chat.id,
        emoji_ids
    )


# =========================
# PHOTO
# =========================

@bot.message_handler(
    content_types=["photo"]
)
def photo_handler(message):

    emoji_ids = extract_custom_emojis(
        message.caption or "",
        message.caption_entities
    )

    send_results(
        message.chat.id,
        emoji_ids
    )


# =========================
# VIDEO
# =========================

@bot.message_handler(
    content_types=["video"]
)
def video_handler(message):

    emoji_ids = extract_custom_emojis(
        message.caption or "",
        message.caption_entities
    )

    send_results(
        message.chat.id,
        emoji_ids
    )


# =========================
# ANIMATION / GIF
# =========================

@bot.message_handler(
    content_types=["animation"]
)
def animation_handler(message):

    emoji_ids = extract_custom_emojis(
        message.caption or "",
        message.caption_entities
    )

    send_results(
        message.chat.id,
        emoji_ids
    )


# =========================
# DOCUMENT
# =========================

@bot.message_handler(
    content_types=["document"]
)
def document_handler(message):

    emoji_ids = extract_custom_emojis(
        message.caption or "",
        message.caption_entities
    )

    send_results(
        message.chat.id,
        emoji_ids
    )


# =========================
# AUDIO
# =========================

@bot.message_handler(
    content_types=["audio"]
)
def audio_handler(message):

    emoji_ids = extract_custom_emojis(
        message.caption or "",
        message.caption_entities
    )

    send_results(
        message.chat.id,
        emoji_ids
    )


# =========================
# VOICE
# =========================

@bot.message_handler(
    content_types=["voice"]
)
def voice_handler(message):

    emoji_ids = extract_custom_emojis(
        message.caption or "",
        message.caption_entities
    )

    send_results(
        message.chat.id,
        emoji_ids
    )


# =========================
# STICKER
# =========================

@bot.message_handler(
    content_types=["sticker"]
)
def sticker_handler(message):

    emoji_ids = []

    try:
        custom_id = getattr(
            message.sticker,
            "custom_emoji_id",
            None
        )

        if custom_id:
            emoji_ids.append(
                str(custom_id)
            )

    except Exception as e:
        logging.warning(
            "Sticker error: %s",
            e
        )

    send_results(
        message.chat.id,
        emoji_ids
    )


# =========================
# CALLBACKS
# =========================

@bot.callback_query_handler(
    func=lambda call: call.data == "extract"
)
def extract_callback(call):

    bot.answer_callback_query(
        call.id,
        "🧩 Send a message containing custom emojis."
    )


@bot.callback_query_handler(
    func=lambda call: call.data == "help"
)
def help_callback(call):

    text = (
        "ℹ️ <b>HELP</b>\n\n"
        "Send any Telegram message containing "
        "custom emojis.\n\n"
        "The bot will extract their IDs and give "
        "you a 📋 COPY ID button."
    )

    bot.answer_callback_query(call.id)

    bot.send_message(
        call.message.chat.id,
        text,
        reply_markup=home_keyboard()
    )


@bot.callback_query_handler(
    func=lambda call: call.data == "close"
)
def close_callback(call):

    bot.answer_callback_query(
        call.id,
        "Closed"
    )

    try:
        bot.delete_message(
            call.message.chat.id,
            call.message.message_id
        )
    except Exception:
        pass


# =========================
# COPY FALLBACK
# =========================

@bot.callback_query_handler(
    func=lambda call: call.data.startswith("copy_")
)
def copy_callback(call):

    emoji_id = call.data.replace(
        "copy_",
        "",
        1
    )

    bot.answer_callback_query(
        call.id,
        f"ID: {emoji_id}"
    )


# =========================
# FLASK
# =========================

@app.route("/")
def index():

    return "Custom Emoji Extractor Bot is running."


@app.route("/health")
def health():

    return {
        "status": "ok",
        "bot": "Custom Emoji Extractor"
    }


@app.route(
    "/telegram/webhook",
    methods=["POST"]
)
def telegram_webhook():

    try:

        json_string = request.get_data().decode(
            "utf-8"
        )

        update = telebot.types.Update.de_json(
            json_string
        )

        bot.process_new_updates(
            [update]
        )

        return "OK", 200

    except Exception as e:

        logging.exception(
            "Webhook error"
        )

        return "ERROR", 500


# =========================
# WEBHOOK SETUP
# =========================

def setup_webhook():

    if not RENDER_EXTERNAL_URL:
        logging.warning(
            "RENDER_EXTERNAL_URL is not set."
        )
        return

    webhook_url = (
        RENDER_EXTERNAL_URL
        + "/telegram/webhook"
    )

    try:

        bot.remove_webhook()

        bot.set_webhook(
            url=webhook_url
        )

        logging.info(
            "Webhook set: %s",
            webhook_url
        )

    except Exception as e:

        logging.exception(
            "Webhook setup failed: %s",
            e
        )


# =========================
# MAIN
# =========================

if __name__ == "__main__":

    setup_webhook()

    app.run(
        host="0.0.0.0",
        port=PORT
    )
