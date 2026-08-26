import telebot

TOKEN = "8497450621:AAFAl7KrMth6mlJvHwzW5DuRDSsG8LQB0wk"

bot = telebot.TeleBot(TOKEN)


# /start
@bot.message_handler(commands=["start"])
def start(message):
    bot.reply_to(
        message,
        "🆔 Custom Emoji ID Finder\n\n"
        "बस अपना Telegram Custom Emoji मुझे भेजो।\n"
        "मैं उसका Custom Emoji ID बता दूँगा."
    )


# /emojiid
@bot.message_handler(commands=["emojiid"])
def emojiid(message):
    bot.reply_to(
        message,
        "🆔 अब अपना Custom Emoji भेजो.\n\n"
        "⚠️ Normal emoji नहीं, Telegram Custom Emoji भेजना है."
    )


# Custom Emoji detect करना
@bot.message_handler(
    func=lambda message: (
        message.entities is not None
        and any(e.type == "custom_emoji" for e in message.entities)
    )
)
def get_emoji_id(message):

    for entity in message.entities:

        if entity.type == "custom_emoji":

            emoji_id = entity.custom_emoji_id

            bot.reply_to(
                message,
                f"✅ Custom Emoji मिल गया!\n\n"
                f"🆔 Custom Emoji ID:\n"
                f"`{emoji_id}`\n\n"
                f"📋 इस ID को copy कर लो.",
                parse_mode="Markdown"
            )

            return


# बाकी messages
@bot.message_handler(func=lambda message: True)
def other_message(message):
    bot.reply_to(
        message,
        "❌ Custom Emoji नहीं मिला.\n\n"
        "Telegram का Custom Emoji सीधे भेजें."
    )


print("🆔 Custom Emoji ID Bot Running...")
bot.infinity_polling()
