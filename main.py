import os
import logging
from flask import Flask, request
import telebot
from telebot.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    CopyTextButton
)

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
# BUTTON STYLES
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
    return InlineKeyboardButton(
        text="📋 COPY ID",
        copy_text=CopyTextButton(
            text=str(emoji_id)
        ),
        style="primary"
    )


# =========================
# HOME MENU
# =========================

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
def start(message):

    bot.send_message(
        message.chat.id,
        (
            "👋 <b>Custom Emoji Extractor V3</b>\n\n"
            "🧩 Custom Emoji wala message mujhe bhejo "
            "ya forward karo.\n\n"
            "✨ Main automatically Custom Emoji ID "
            "extract karunga.\n\n"
            "📋 Har ID ke saamne alag "
            "<b>COPY ID</b> button milega."
        ),
        reply_markup=home_keyboard()
    )


# =========================
# HELP
# =========================

@bot.message_handler(commands=["help"])
def help_command(message):

    bot.send_message(
        message.chat.id,
        (
            "ℹ️ <b>HELP</b>\n\n"
            "1️⃣ Custom Emoji wala message bhejo.\n"
            "2️⃣ Bot sabhi Custom Emoji detect karega.\n"
            "3️⃣ Har Emoji ki ID alag show hogi.\n"
            "4️⃣ 📋 COPY ID par tap karke ID copy karo.\n\n"
            "🔵 Primary = Copy\n"
            "🟢 Success = Extract\n"
            "🔴 Danger = Close"
        ),
        reply_markup=home_keyboard()
    )


# =========================
# EXTRACT CUSTOM EMOJIS
# =========================

def extract_custom_emojis(text, entities):

    found = []

    if not text or not entities:
        return found

    for entity in entities:

        if entity.type != "custom_emoji":
            continue

        emoji_id = getattr(
            entity,
            "custom_emoji_id",
            None
        )

        if emoji_id:
            found.append(str(emoji_id))

    return found


# =========================
# SEND RESULTS
# =========================

def send_results(message, emoji_ids):

    if not emoji_ids:

        bot.reply_to(
            message,
            (
                "❌ <b>Custom Emoji नहीं मिला.</b>\n\n"
                "Telegram का actual Custom Emoji वाला "
                "message भेजकर फिर try करो."
            )
        )

        return

    # Remove duplicates
    unique_ids = list(dict.fromkeys(emoji_ids))

    bot.send_message(
        message.chat.id,
        f"✅ <b>{len(unique_ids)} Custom Emoji Found</
