import os
import logging
from flask import Flask, request
import telebot
from telebot.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton
)

BOT_TOKEN = os.getenv("BOT_TOKEN")
PORT = int(os.getenv("PORT", "10000"))
RENDER_EXTERNAL_URL = os.getenv(
    "RENDER_EXTERNAL_URL",
    ""
).rstrip("/")

if not BOT_TOKEN:
    raise RuntimeError(
        "BOT_TOKEN environment variable is missing"
    )

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

bot = telebot.TeleBot(
    BOT_TOKEN,
    parse_mode="HTML"
)

app = Flask(__name__)


# ==================================================
# BUTTON STYLES
# ==================================================

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


# ==================================================
# COPY BUTTON
# ==================================================

def copy_button(emoji_id):

    try:
        from telebot.types import CopyTextButton

        return InlineKeyboardButton(
            text="📋 COPY ID",
            copy_text=CopyTextButton(
                text=str(emoji_id)
            ),
            style="primary"
        )

    except Exception:

        # Fallback
        return InlineKeyboardButton(
            text="📋 COPY ID",
            callback_data="copy_" + str(emoji_id),
            style="primary"
        )


# ==================================================
# HOME KEYBOARD
# ==================================================

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


# ==================================================
# START
# ==================================================

@bot.message_handler(commands=["start"])
def start(message):

    text = (
        "👋 <b>Custom Emoji Extractor V4</b>\n\n"

        "🧩 Custom Emoji वाला message "
        "मुझे भेजो या forward करो।\n\n"

        "✨ मैं automatically Custom Emoji ID "
        "निकालूँगा।\n\n"

        "📋 हर ID के सामने अलग "
        "<b>📋 COPY ID</b> button मिलेगा।"
    )

    bot.send_message(
        message.chat.id,
        text,
        reply_markup=home_keyboard()
    )


# ==================================================
# HELP
# ==================================================

@bot.message_handler(commands=["help"])
def help_command(message):

    text = (
        "ℹ️ <b>HELP</b>\n\n"

        "1️⃣ Custom Emoji वाला message भेजो।\n"
        "2️⃣ Bot सभी Custom Emojis detect करेगा।\n"
        "3️⃣ हर Emoji की ID अलग दिखाई जाएगी।\n"
        "4️⃣ 📋 COPY ID दबाकर ID copy करो।\n\n"

        "🔵 PRIMARY = Copy / Main Action\n"
        "🟢 SUCCESS = Extract\n"
        "🔴 DANGER = Close"
    )

    bot.send_message(
        message.chat.id,
        text,
        reply_markup=home_keyboard()
    )


# ==================================================
# EXTRACT CUSTOM EMOJIS
# ==================================================

def extract_custom_emojis(text, entities):

    result = []

    if not text or not entities:
        return result

    for entity in entities:

        if entity.type == "custom_emoji":

            emoji_id = getattr(
                entity,
                "custom_emoji_id",
                None
            )

            if emoji_id:
                result.append(
                    str(emoji_id)
                )

    return result


# ==================================================
# SEND RESULTS
# ==================================================

def send_results(message, emoji_ids):

    if not emoji_ids:

        bot.reply_to(
            message,
            (
                "❌ <b>Custom Emoji नहीं मिला।</b>\n\n"

                "Telegram का actual Custom Emoji "
                "वाला message भेजकर फिर try करो।"
            )
        )

        return

    # Remove duplicates
    unique_ids = list(
        dict.fromkeys(emoji_ids)
    )

    bot.send_message(
        message.chat.id,
        (
            f"✅ <b>{len(unique_ids)} "
            f"Custom Emoji Found</b>"
        )
    )

    # Every emoji gets separate Copy button
    for index, emoji_id in enumerate(
        unique_ids,
        start=1
    ):

        kb = InlineKeyboardMarkup()

        kb.add(
            copy_button(
                emoji_id
            )
        )

        text = (
            f"🧩 <b>Custom Emoji #{index}</b>\n\n"
            f"🆔 <code>{emoji_id}</code>"
        )

        bot.send_message(
            message.chat.id,
            text,
            reply_markup=kb
        )


# ==================================================
# TEXT / MEDIA
# ==================================================

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

    emoji_ids = []

    # Text
    if message.text:

        emoji_ids.extend(
            extract_custom_emojis(
                message.text,
                message.entities
            )
        )

    # Caption
    if message.caption:

        emoji_ids.extend(
            extract_custom_emojis(
                message.caption,
                message.caption_entities
            )
        )

    send_results(
        message,
        emoji_ids
    )


# ==================================================
# STICKER
# ==================================================

@bot.message_handler(
    content_types=["sticker"]
)
def handle_sticker(message):

    sticker = message.sticker

    emoji_id = getattr(
        sticker,
        "custom_emoji_id",
        None
    )

    if not emoji_id:

        bot.reply_to(
            message,
            (
                "❌ इस sticker में "
                "Custom Emoji ID नहीं मिली।"
            )
        )

        return

    kb = InlineKeyboardMarkup()

    kb.add(
        copy_button(
            str(emoji_id)
        )
    )

    bot.reply_to(
        message,
        (
            "🧩 <b>Custom Emoji</b>\n\n"
            f"🆔 <code>{emoji_id}</code>"
        ),
        reply_markup=kb
    )


# ==================================================
# EXTRACT CALLBACK
# ==================================================

@bot.callback_query_handler(
    func=lambda call:
        call.data == "extract"
)
def callback_extract(call):

    bot.answer_callback_query(
        call.id
    )

    bot.send_message(
        call.message.chat.id,
        (
            "🧩 <b>Ready!</b>\n\n"
            "अब Custom Emoji वाला "
            "message भेजो।"
        )
    )


# ==================================================
# HELP CALLBACK
# ==================================================

@bot.callback_query_handler(
    func=lambda call:
        call.data == "help"
)
def callback_help(call):

    bot.answer_callback_query(
        call.id
    )

    bot.send_message(
        call.message.chat.id,
        (
            "ℹ️ <b>HELP</b>\n\n"
            "Custom Emoji वाला message भेजो।\n"
            "हर ID के सामने "
            "📋 COPY ID button मिलेगा।"
        )
    )


# ==================================================
# CLOSE CALLBACK
# ==================================================

@bot.callback_query_handler(
    func=lambda call:
        call.data == "close"
)
def callback_close(call):

    bot.answer_callback_query(
        call.id,
        "Closed"
    )

    try:

        bot.edit_message_reply_markup(
            call.message.chat.id,
            call.message.message_id,
            reply_markup=None
        )

    except Exception:

        pass


# ==================================================
# COPY CALLBACK FALLBACK
# ==================================================

@bot.callback_query_handler(
    func=lambda call:
        call.data.startswith("copy_")
)
def callback_copy(call):

    emoji_id = call.data.replace(
        "copy_",
        "",
        1
    )

    bot.answer_callback_query(
        call.id,
        "📋 ID: " + emoji_id,
        show_alert=True
    )


# ==================================================
# FLASK
# ==================================================

@app.route("/")
def home():

    return (
        "Custom Emoji Extractor V4 is running.",
        200
    )


@app.route("/health")
def health():

    return "OK", 200


# ==================================================
# TELEGRAM WEBHOOK
# ==================================================

@app.route(
    "/telegram/webhook",
    methods=["POST"]
)
def telegram_webhook():

    try:

        data = request.get_data().decode(
            "utf-8"
        )

        update = telebot.types.Update.de_json(
            data
        )

        bot.process_new_updates(
            [update]
        )

        return "OK", 200

    except Exception as e:

        logging.exception(
            "Webhook error: %s",
            e
        )

        return "ERROR", 500


# ==================================================
# SET WEBHOOK
# ==================================================

def setup_webhook():

    if not RENDER_EXTERNAL_URL:

        logging.warning(
            "RENDER_EXTERNAL_URL not found"
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
            "Webhook configured: %s",
            webhook_url
        )

    except Exception as e:

        logging.exception(
            "Webhook setup failed: %s",
            e
        )


# ==================================================
# RUN
# ==================================================

if __name__ == "__main__":

    setup_webhook()

    app.run(
        host="0.0.0.0",
        port
