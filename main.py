import os
import random
import time
from datetime import datetime
import telebot
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup

TOKEN = "8849298752:AAGmiS4virj3rJ6xxuh1ba7vSKNSl3cj5ws"
bot = telebot.TeleBot(TOKEN)

# DATA STORES
user_last_spin = {}
user_amount_input = {}
user_balances = {}
user_purchase_history = {}
support_tickets = {}
user_ticket_state = {}

# CONFIGURATIONS
DEFAULT_UPI_ID = "vicky3198737@axl"
BINANCE_PAY_ID = "123456789"
BKASH_NUMBER = "01700000000"
ADMIN_TELEGRAM_USERNAME = "VICKYXMOD"
ADMIN_WHATSAPP_NUM = "918303304640"

APP_PRICES = {
    "vala_mod": {"name": "VALA MOD APK", "1 Hour": 45, "3 Hours": 100, "6 Hours": 150, "12 Hours": 250, "24 Hours": 400},
    "drip": {"name": "Drip Client Apk", 1: 80, 3: 160, 7: 270, 15: 420, 30: 620},
    "drip_proxy": {"name": "Drip Client Proxy Apk", 1: 80, 3: 160, 7: 270, 30: 620},
    "prime": {"name": "Prime Hook Apk", 1: 95, 3: 160, 7: 315},
    "hg_proxy": {"name": "Hg Proxy Apk", 1: 100, 7: 240, 10: 310, 30: 605},
    "patorange": {"name": "Patoteam Orange", 3: 230, 7: 370, 15: 605, 30: 960},
    "patblue": {"name": "Patoteam Blue", 3: 265, 7: 440, 15: 640, 30: 1020},
    "brmods_nr": {"name": "Br Mods Non Root", 1: 90, 7: 270, 15: 460, 30: 640},
    "reaper_nr": {"name": "Reaper xPro Apk", 10: 365, 30: 900},
    "silent_nr": {"name": "Silent Cheats Apkmod", 1: 110, 3: 200, 7: 370, 14: 620, 28: 920},
    "brmods_root": {"name": "Br Mods Apk", 1: 79, 7: 260, 15: 440, 30: 620},
    "reaper_root": {"name": "Reaper x Pro", 10: 345, 30: 795},
    "drip_root": {"name": "Drip Client Root", 1: 70, 7: 320, 30: 650},
    "hg_root": {"name": "Hg Cheats Apk (Root)", 1: 80, 7: 190, 10: 290, 30: 590},
    "stricks": {"name": "Stricks Br ~ Alpha", 1: 70, 5: 160, 7: 250, 15: 450, 30: 600},
    "xyz": {"name": "Xyz Cheats Apk", 1: 70, 3: 150, 7: 300, 15: 500, 30: 790},
    "hikari": {"name": "Hikari Mod Apk", 1: 70, 3: 149, 7: 299, 15: 499, 30: 799},
    "lk": {"name": "LK Team Apk", 1: 80, 5: 170, 10: 250, 30: 690},
    "safe": {"name": "Silent Cheats [Safe]", 1: 80, 3: 170, 7: 340, 14: 580, 28: 850},
    "brutal": {"name": "Silent Cheats [Brutal]", 1: 80, 3: 170, 7: 340, 14: 585, 30: 895},
    "xreg": {"name": "Xreg Safe Apk", 1: 90, 10: 300, 20: 500, 30: 680},
    "rapid": {"name": "Rapid Core Apk", 1: 89, 7: 299, 14: 549, 30: 1099},
    "haxx": {"name": "Haxx-cker Pro", 10: 545, 20: 1030, 30: 1400},
    "zytron": {"name": "Zytron Pro Apk", 1: 80, 7: 320, 15: 480, 30: 620},
    "angry": {"name": "Angry Mod Apk", 1: 75, 7: 320, 15: 530, 30: 750},
    "scorpio_lite": {"name": "Scorpio Mods [Lite]", 7: 240, 15: 400, 30: 600},
    "scorpio_brutal": {"name": "Scorpio Mods [Brutal]", 7: 300, 15: 450, 30: 800},
    "gbox": {"name": "Gbox Certificate", "1 year validity": 1000},
    "esing": {"name": "Esing Certificate", "1 year validity": 500},
    "fluorite": {"name": "Fluorite Ios", 1: 390, 7: 1240, 31: 2000},
    "migul_pro": {"name": "Migul ~ Pro", 1: 300, 7: 890, 31: 1700},
    "migul_basic": {"name": "Migul ~ Basic", 1: 220, 7: 530, 31: 1320},
    "drip_pc": {"name": "Drip Client Pc", 1: 150, 7: 360, 15: 650, 30: 1020},
    "brmods_pc": {"name": "Br Mods Pc", 1: 85, 10: 350, 30: 690}
}

def get_stock_count(filename):
    if not os.path.exists(filename):
        return 0
    try:
        with open(filename, "r", encoding="utf-8") as f:
            keys = f.readlines()
        return len([k for k in keys if k.strip()])
    except:
        return 0

def create_keypad_markup(current_val):
    markup = InlineKeyboardMarkup()
    markup.row(
        InlineKeyboardButton("1", callback_data="num_1"),
        InlineKeyboardButton("2", callback_data="num_2"),
        InlineKeyboardButton("3", callback_data="num_3")
    )
    markup.row(
        InlineKeyboardButton("4", callback_data="num_4"),
        InlineKeyboardButton("5", callback_data="num_5"),
        InlineKeyboardButton("6", callback_data="num_6")
    )
    markup.row(
        InlineKeyboardButton("7", callback_data="num_7"),
        InlineKeyboardButton("8", callback_data="num_8"),
        InlineKeyboardButton("9", callback_data="num_9")
    )
    markup.row(
        InlineKeyboardButton("C", callback_data="num_clear"),
        InlineKeyboardButton("0", callback_data="num_0"),
        InlineKeyboardButton("⌫", callback_data="num_backspace")
    )
    markup.add(InlineKeyboardButton(f"✅ 𝙲𝚘𝚗𝚏𝚒𝚛𝚖 ₹{current_val}", callback_data="confirm_custom_pay"))
    markup.add(InlineKeyboardButton("🖐 𝙱𝚊𝚌𝚔", callback_data="btn_paytm_upi"))
    return markup

@bot.message_handler(commands=['start'])
def send_welcome(message):
    text = """✨ *𝚆𝙴𝙻𝙲𝙾𝙼𝙴 𝚃𝙾 𝚃𝙷𝙴 𝚂𝚃𝙾𝚁𝙴*

🛒 *𝙿𝚛𝚘𝚍𝚞𝚌𝚝 𝚂𝚝𝚘𝚛𝚎* : 𝚊𝚕𝚕 𝚔𝚎𝚢 𝚙𝚞𝚛𝚌𝚑𝚊𝚜𝚎 & 𝚒𝚗𝚜𝚝𝚊𝚗𝚝𝚕𝚢 𝚍𝚎𝚕𝚒𝚟𝚎𝚛𝚢
👤 *𝙼𝚢 𝙿𝚛𝚘𝚏𝚒𝚕𝚎* : 𝚌𝚑𝚎𝚌𝚔 𝚢𝚘𝚞𝚛 𝚊𝚌𝚌𝚘𝚞𝚗𝚝 𝚒𝚗𝚏𝚘𝚛𝚖𝚊𝚝𝚒𝚘𝚗
💰 *𝙰𝚍𝚍 𝙱𝚊𝚕𝚊𝚗𝚌𝚎* : 𝚍𝚎𝚙𝚘𝚜𝚒𝚝 𝚋𝚊𝚕𝚊𝚗𝚌𝚎 & 𝚜𝚎𝚌𝚞𝚛𝚎 𝚜𝚎𝚛𝚟𝚒𝚌𝚎
🔑 *𝙰𝚕𝚕 𝙷𝚒𝚜𝚝𝚘𝚛𝚢* : 𝚌𝚑𝚎𝚌𝚔 𝚊𝚕𝚕 𝚔𝚎𝚢 𝚙𝚞𝚛𝚌𝚑𝚊𝚜𝚎 𝚑𝚒𝚜𝚝𝚘𝚛𝚢
👥 *𝚁𝚎𝚏𝚎𝚛𝚛𝚊𝚕* : 𝚒𝚗𝚟𝚒𝚝𝚎 𝚏𝚛𝚒𝚎𝚗𝚍𝚜 & 𝚎𝚊𝚛𝚗 𝚛𝚎𝚠𝚊𝚛𝚍𝚜
🌐 *𝚂𝚞𝚙𝚙𝚘𝚛𝚝* : 𝚋𝚘𝚝 𝚙𝚛𝚘𝚋𝚕𝚎𝚖 𝚏𝚒𝚡𝚎𝚍 𝚏𝚘𝚛 𝚜𝚞𝚙𝚙𝚘𝚛𝚝 𝚊𝚍𝚖𝚒𝚗
🎁 *𝙻𝚞𝚍𝚘 𝚂𝚙𝚒𝚗* : 𝚙𝚕𝚊𝚢 𝚐𝚊𝚖𝚎 𝚊𝚗𝚍 𝚠𝚒𝚗 𝚋𝚊𝚕𝚊𝚗𝚌𝚎
📥 *𝙳𝚘𝚠𝚗𝚕𝚘𝚊𝚍 𝙵𝚒𝚕𝚎𝚜* : 𝚍𝚘𝚠𝚗𝚕𝚘𝚊𝚍 𝚕𝚊𝚝𝚎𝚜𝚝 𝚊𝚙𝚔 𝚏𝚘𝚛 𝚜𝚊𝚏𝚎𝚝𝚢."""

    markup = InlineKeyboardMarkup()
    btn_store = InlineKeyboardButton("🛒 𝙿𝚛𝚘𝚍𝚞𝚌𝚝 𝚂𝚝𝚘𝚛𝚎", callback_data="btn_store")
    btn_profile = InlineKeyboardButton("👤 𝙼𝚢 𝙿𝚛𝚘𝚏𝚒𝚕𝚎", callback_data="btn_profile")
    btn_balance = InlineKeyboardButton("💰 𝙰𝚍𝚍 𝙱𝚊𝚕𝚊𝚗𝚌𝚎", callback_data="btn_balance")
    btn_history = InlineKeyboardButton("🔑 𝙰𝚕𝚕 𝙷𝚒𝚜𝚝𝚘𝚛𝚢", callback_data="btn_history")
    btn_referral = InlineKeyboardButton("👥 𝚁𝚎𝚏𝚎𝚛𝚛𝚊𝚕", callback_data="btn_referral")
    btn_support = InlineKeyboardButton("🌐 𝚂𝚞𝚙𝚙𝚘𝚛𝚝", callback_data="btn_support")
    btn_ludo = InlineKeyboardButton("🎁 𝙻𝚞𝚍𝚘 𝚂𝚙𝚒𝚗", callback_data="btn_ludo")
    btn_download = InlineKeyboardButton("📥 𝙳𝚘𝚠𝚗𝚕𝚘𝚊𝚍 𝙵𝚒𝚕𝚎𝚜", callback_data="btn_download")

    markup.add(btn_store)
    markup.row(btn_profile, btn_balance)
    markup.row(btn_history, btn_referral)
    markup.row(btn_support, btn_ludo)
    markup.add(btn_download)

    bot.send_message(message.chat.id, text, reply_markup=markup, parse_mode="Markdown")

@bot.message_handler(func=lambda msg: user_ticket_state.get(msg.from_user.id) == "WAITING_FOR_TICKET")
def handle_ticket_message(message):
    user_id = message.from_user.id
    user_ticket_state[user_id] = None
    ticket_id = f"#TCK-{random.randint(1000, 9999)}"
    created_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    support_tickets[ticket_id] = {
        "user_id": user_id,
        "username": message.from_user.username or message.from_user.first_name,
        "issue": message.text,
        "time": created_time,
        "status": "OPEN"
    }

    back_markup = InlineKeyboardMarkup()
    back_markup.add(InlineKeyboardButton("🔙 𝙱𝚊𝚌𝚔 𝚝𝚘 𝚂𝚞𝚙𝚙𝚘𝚛𝚝", callback_data="btn_support"))
    success_msg = (
        f"✅ *𝚃𝙸𝙲𝙺𝙴𝚃 𝙲𝚁𝙴𝙰𝚃𝙴𝙳 𝚂𝚄𝙲𝙲𝙴𝚂𝚂𝙵𝚄𝙻𝙻𝚈!*\n\n"
        f"🎫 **𝚃𝚒𝚌𝚔𝚎𝚝 𝙸𝙳:** `{ticket_id}`\n"
        f"📝 **𝙸𝚜𝚜𝚞𝚎:** {message.text}\n"
        f"🕒 **𝚃𝚒𝚖𝚎:** {created_time}\n"
        f"📌 **𝚂𝚝𝚊𝚝𝚞𝚜:** 𝙾𝙿𝙴𝙽 🟡\n\n"
        f"𝙾𝚞𝚛 𝚜𝚞𝚙𝚙𝚘𝚛𝚝 𝚝𝚎𝚊𝚖 𝚠𝚒𝚕𝚕 𝚌𝚘𝚗𝚝𝚊𝚌𝚝 𝚢𝚘𝚞 𝚜𝚑𝚘𝚛𝚝𝚕𝚢!"
    )
    bot.reply_to(message, success_msg, parse_mode="Markdown", reply_markup=back_markup)

@bot.callback_query_handler(func=lambda call: True)
def callback_listener(call):
    user_id = call.from_user.id
    chat_id = call.message.chat.id
    message_id = call.message.message_id
    data = call.data

    clean_admin = ADMIN_TELEGRAM_USERNAME.replace("@", "").strip()

    back_markup = InlineKeyboardMarkup()
    back_markup.add(InlineKeyboardButton("🔙 𝙱𝙰𝙲𝙺", callback_data="btn_back"))

    if data == "btn_back":
        bot.delete_message(chat_id=chat_id, message_id=message_id)
        send_welcome(call.message)

    elif data == "btn_store":
        text = "🛒 *𝚂𝙴𝙻𝙴𝙲𝚃 𝙿𝚁𝙾𝙳𝚄𝙲𝚃 𝙿𝙰𝙽𝙴𝙻*\n\n✅ 𝙲𝚑𝚘𝚘𝚜𝚎 𝚊 𝚙𝚊𝚗𝚎𝚕 𝚝𝚘 𝚟𝚒𝚎𝚠 𝚒𝚝𝚜 𝚙𝚊𝚌𝚔𝚊𝚐𝚎𝚜:"
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("🤖 𝙰𝙽𝙳𝚁𝙾𝙸𝙳 𝙽𝙾𝙽 𝚁𝙾𝙾𝚃 𝙿𝙰𝙽𝙴𝙻", callback_data="pnl_nonroot"))
        markup.add(InlineKeyboardButton("🤖 𝙰𝙽𝙳𝚁𝙾𝙸𝙳 𝚁𝙾𝙾𝚃 𝙿𝙰𝙽𝙴𝙻", callback_data="pnl_root"))
        markup.add(InlineKeyboardButton("🍎 𝙸𝙿𝙷𝙾𝙽𝙴 𝙿𝙰𝙽𝙴𝙻", callback_data="pnl_iphone"))
        markup.add(InlineKeyboardButton("💻 𝙿𝙲 𝙿𝙰𝙽𝙴𝙻", callback_data="pnl_pc"))
        markup.add(InlineKeyboardButton("🔙 𝙱𝙰𝙲𝙺", callback_data="btn_back"))
        bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=text, parse_mode="Markdown", reply_markup=markup)

    elif data == "btn_profile":
        user_name = call.from_user.first_name
        join_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        bal = user_balances.get(user_id, 0.24)
        profile_text = (
            f"👤 **— 𝚈𝙾𝚄𝚁 𝚂𝙴𝙲𝚄𝚁𝙴 𝙿𝚁𝙾𝙵𝙸𝙻𝙴 —** 👤\n\n"
            f"👤 𝙶𝚛𝚒𝚍 𝙸𝙳: `{user_id}`\n"
            f"👑 𝙽𝚊𝚖𝚎: {user_name}\n"
            f"👑 𝙰𝚌𝚌𝚘𝚞𝚗𝚝 𝙻𝚎𝚟𝚎𝚕: 👤 𝚁𝚎𝚐𝚞𝚕𝚊𝚛 𝚄𝚜𝚎𝚛\n\n"
            f"💰 **— 𝚆𝚊𝚕𝚕𝚎𝚝 —** 🪙\n"
            f"💰 𝙲𝚞𝚛𝚛𝚎𝚗𝚝 𝙱𝚊𝚕𝚊𝚗𝚌𝚎: ₹{bal:.2f} (~ ${(bal/90.0):.2f}) 🪙\n\n"
            f"📈 **— 𝙶𝚕𝚘𝚋𝚊𝚕 𝚂𝚝𝚊𝚝𝚒𝚜𝚝𝚒𝚌𝚜 —**\n"
            f"🗂️ 𝚃𝚘𝚝𝚊𝚕 𝙾𝚛𝚍𝚎𝚛𝚜: {len(user_purchase_history.get(user_id, []))}\n"
            f"💸 𝚃𝚘𝚝𝚊𝚕 𝚂𝚙𝚎𝚗𝚝: ₹0.00 (~ $0.00)\n"
            f"👥 𝚃𝚘𝚝𝚊𝚕 𝚁𝚎𝚏𝚎𝚛𝚛𝚊𝚕𝚜: 0\n\n"
            f"📅 𝙹𝚘𝚒𝚗𝚎𝚍 𝙶𝚛𝚒𝚍: {join_date}"
        )
        profile_markup = InlineKeyboardMarkup()
        profile_markup.add(InlineKeyboardButton("🎁 𝚁𝚎𝚍𝚎𝚎𝚖 𝙿𝚛𝚘𝚖𝚘 𝙲𝚘𝚍𝚎", callback_data="btn_redeem"))
        profile_markup.add(InlineKeyboardButton("🔙 𝙱𝙰𝙲𝙺", callback_data="btn_back"))
        bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=profile_text, parse_mode="Markdown", reply_markup=profile_markup)

    elif data == "btn_redeem":
        bot.answer_callback_query(call.id, "⚠️ आपके पास कोई वैलिड प्रोमो कोड नहीं है!", show_alert=True)

    elif data == "btn_support":
        text = (
            "🌐💬 — *𝙿𝚁𝙴𝙼𝙸𝚄𝙼 𝚂𝚄𝙿𝙿𝙾𝚁𝚃 𝙲𝙴𝙽𝚃𝙴𝚁* —\n\n"
            "𝙲𝚘𝚗𝚝𝚊𝚌𝚝 𝚞𝚜 𝚟𝚒𝚊 𝚃𝚎𝚕𝚎𝚐𝚛𝚊𝚖 𝚘𝚛 𝚆𝚑𝚊𝚝𝚜𝙰𝚙𝚙 𝚏𝚘𝚛 𝚒𝚗𝚜𝚝𝚊𝚗𝚝 𝚑𝚎𝚕𝚙, 𝚘𝚛 𝚘𝚙𝚎𝚗 𝚊 𝚜𝚞𝚙𝚙𝚘𝚛𝚝 𝚝𝚒𝚌𝚔𝚎𝚝 𝚏𝚘𝚛 𝚊𝚍𝚖𝚒𝚗 𝚊𝚜𝚜𝚒𝚜𝚝𝚊𝚗𝚌𝚎."
        )
        support_markup = InlineKeyboardMarkup()
        support_markup.add(InlineKeyboardButton("✈️ 𝙲𝚘𝚗𝚝𝚊𝚌𝚝 𝚘𝚗 𝚃𝚎𝚕𝚎𝚐𝚛𝚊𝚖", url=f"https://t.me/{clean_admin}"))
        support_markup.add(InlineKeyboardButton("💬 𝙲𝚘𝚗𝚝𝚊𝚌𝚝 𝚘𝚗 𝚆𝚑𝚊𝚝𝚜𝙰𝚙𝚙", url=f"https://wa.me/{ADMIN_WHATSAPP_NUM}"))
        support_markup.row(
            InlineKeyboardButton("🎫 𝙾𝚙𝚎𝚗 𝙽𝚎𝚠 𝚃𝚒𝚌𝚔𝚎𝚝", callback_data="ticket_open"),
            InlineKeyboardButton("📋 𝙼𝚢 𝙾𝚙𝚎𝚗 𝚃𝚒𝚌𝚔𝚎𝚝𝚜", callback_data="ticket_view")
        )
        support_markup.add(InlineKeyboardButton("🔙 𝙱𝙰𝙲𝙺", callback_data="btn_back"))
        bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=text, parse_mode="Markdown", reply_markup=support_markup)

    elif data == "ticket_open":
        user_ticket_state[user_id] = "WAITING_FOR_TICKET"
        text = "🎫 *𝙾𝙿𝙴𝙽 𝚂𝚄𝙿𝙿𝙾𝚁𝚃 𝚃𝙸𝙲𝙺𝙴𝚃*\n\n𝙺𝚛𝚒𝚙𝚢𝚊 𝚊𝚙𝚗𝚒 𝚜𝚊𝚖𝚊𝚜𝚢𝚊 (𝚙𝚛𝚘𝚋𝚕𝚎𝚖) 𝚗𝚒𝚌𝚑𝚎 𝚝𝚢𝚙𝚎 𝚔𝚊𝚛𝚔𝚎 𝚖𝚎𝚜𝚜𝚊𝚐𝚎 𝚔𝚊𝚛𝚎𝚒𝚗.\n\n📌 *𝙴𝚡𝚊𝚖𝚙𝚕𝚎:* 𝙼𝚢 𝚋𝚊𝚕𝚊𝚗𝚌𝚎 𝚒𝚜 𝚗𝚘𝚝 𝚊𝚍𝚍𝚎𝚍 / 𝙺𝚎𝚢 𝚗𝚘𝚝 𝚠𝚘𝚛𝚔𝚒𝚗𝚐."
        cancel_markup = InlineKeyboardMarkup()
        cancel_markup.add(InlineKeyboardButton("❌ 𝙲𝚊𝚗𝚌𝚎𝚕", callback_data="btn_support"))
        bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=text, parse_mode="Markdown", reply_markup=cancel_markup)

    elif data == "ticket_view":
        user_tickets = [t_id for t_id, data in support_tickets.items() if data['user_id'] == user_id]
        if not user_tickets:
            text = "📋 *𝙼𝚈 𝙾𝙿𝙴𝙽 𝚃𝙸𝙲𝙺𝙴𝚃𝚂*\n\n𝙰𝚊𝚙𝚔𝚊 𝚔𝚘𝚒 𝚋𝚑𝚒 𝚜𝚞𝚙𝚙𝚘𝚛𝚝 𝚝𝚒𝚌𝚔𝚎𝚝 𝚊𝚋𝚑𝚒 𝚊𝚌𝚝𝚒𝚟𝚎 𝚗𝚊𝚑𝚒 𝚑𝚊𝚒."
        else:
            text = "📋 *𝙼𝚈 𝚃𝙸𝙲𝙺𝙴𝚃𝚂 𝚂𝚃𝙰𝚃𝚄𝚂*\n\n"
            for t_id in user_tickets:
                info = support_tickets[t_id]
                text += f"🎫 **𝙸𝙳:** `{t_id}`\n📝 **𝙸𝚜𝚜𝚞𝚎:** {info['issue']}\n🕒 **𝚃𝚒𝚖𝚎:** {info['time']}\n📌 **𝚂𝚝𝚊𝚝𝚞𝚜:** {info['status']}\n━━━━━━━━━━━━━━━━━━\n"

        ticket_markup = InlineKeyboardMarkup()
        ticket_markup.add(InlineKeyboardButton("🔙 𝙱𝙰𝙲𝙺 𝚃𝙾 𝚂𝚄𝙿𝙿𝙾𝚁𝚃", callback_data="btn_support"))
        bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=text, parse_mode="Markdown", reply_markup=ticket_markup)

    elif data == "btn_history":
        user_history = user_purchase_history.get(user_id, [])
        if not user_history:
            history_text = "🔑 *𝙿𝚄𝚁𝙲𝙷𝙰𝚂𝙴 𝙷𝙸𝚂𝚃𝙾𝚁𝚈*\n\n𝚈𝚘𝚞 𝚑𝚊𝚟𝚎𝚗'𝚝 𝚖𝚊𝚍𝚎 𝚊𝚗𝚢 𝚙𝚞𝚛𝚌𝚑𝚊𝚜𝚎𝚜 𝚢𝚎𝚝. 𝚈𝚘𝚞𝚛 𝚟𝚊𝚞𝚕𝚝 𝚒𝚜 𝚎𝚖𝚙𝚝𝚢."
        else:
            history_text = "🔑 *𝚈𝙾𝚄𝚁 𝙿𝚄𝚁𝙲𝙷𝙰𝚂𝙴 𝙷𝙸𝚂𝚃𝙾𝚁𝚈*\n\n"
            for idx, item in enumerate(user_history, 1):
                history_text += f"{idx}. 📦 {item['app']} ({item['duration']}) - ₹{item['price']}\n   🕒 {item['time']}\n\n"
        bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=history_text, parse_mode="Markdown", reply_markup=back_markup)

    elif data == "btn_download":
        text = "📥 *𝙳𝙾𝚆𝙽𝙻𝙾𝙰𝙳 𝙿𝚁𝙴𝙼𝙸𝚄𝙼 𝙰𝙿𝙺 & 𝙵𝙸𝙻𝙴𝚂*\n\n🔒 𝙰𝚕𝚕 𝚘𝚞𝚛 𝚑𝚒𝚐𝚑𝚕𝚢 𝚜𝚎𝚌𝚞𝚛𝚎𝚍, 𝚙𝚛𝚎𝚖𝚒𝚞𝚖, 𝚊𝚗𝚍 𝚞𝚙𝚍𝚊𝚝𝚎𝚍 𝚏𝚒𝚕𝚎𝚜 𝚊𝚛𝚎 𝚜𝚎𝚌𝚞𝚛𝚎𝚕𝚢 𝚑𝚘𝚜𝚝𝚎𝚍 𝚘𝚗 𝚘𝚞𝚛 𝚙𝚛𝚒𝚟𝚊𝚝𝚎 𝚌𝚑𝚊𝚗𝚗𝚎𝚕!\n\n✨ *𝚆𝙷𝙰𝚃 𝚈𝙾𝚄 𝙶𝙴𝚃:*\n• 𝙻𝚊𝚝𝚎𝚜𝚝 𝙰𝙿𝙺 𝚄𝚙𝚍𝚊𝚝𝚎𝚜 🚀\n• 100% 𝚅𝚒𝚛𝚞𝚜 𝙵𝚛𝚎𝚎 & 𝚂𝚎𝚌𝚞𝚛𝚎 🛡️\n• 𝙰𝚕𝚕 𝙲𝚘𝚗𝚏𝚒𝚐𝚜 & 𝚂𝚌𝚛𝚒𝚙𝚝𝚜 ⚙️\n• 𝙲𝚘𝚖𝚙𝚕𝚎𝚝𝚎 𝙸𝚗𝚜𝚝𝚊𝚕𝚕𝚊𝚝𝚒𝚘𝚗 𝙶𝚞𝚒𝚍𝚎𝚜 📖"
        download_markup = InlineKeyboardMarkup()
        download_markup.add(InlineKeyboardButton("📢 𝙰𝚌𝚌𝚎𝚜𝚜 𝙳𝚘𝚠𝚗𝚕𝚘𝚊𝚍 𝙲𝚑𝚊𝚗𝚗𝚎𝚕", url="https://t.me/VickyXmodeofc"))
        download_markup.add(InlineKeyboardButton("🔙 𝙱𝙰𝙲𝙺", callback_data="btn_back"))
        bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=text, parse_mode="Markdown", reply_markup=download_markup)

    elif data == "btn_balance":
        text = (
            "🎒 *𝙰𝙳𝙳 𝙱𝙰𝙻𝙰𝙽𝙲𝙴* 💭\n\n"
            "💭 𝚂𝚎𝚕𝚎𝚌𝚝 𝚢𝚘𝚞𝚛 𝚙𝚛𝚎𝚏𝚎𝚛𝚛𝚎𝚍 𝚙𝚊𝚢𝚖𝚎𝚗𝚝 𝚖𝚎𝚝𝚑𝚘𝚍. ✅\n\n"
            "├ 💳 **𝚄𝙿𝙸** — 𝙵𝚊𝚜𝚝 𝙸𝚗𝚍𝚒𝚊𝚗 𝚙𝚊𝚢𝚖𝚎𝚗𝚝𝚜 🛑\n"
            "└ 🪙 **𝙱𝚒𝚗𝚊𝚗𝚌𝚎** — 𝙲𝚛𝚢𝚙𝚝𝚘 𝚙𝚊𝚢𝚖𝚎𝚗𝚝𝚜 🛑\n\n"
            "🛡️ 𝙿𝚊𝚢𝚖𝚎𝚗𝚝𝚜 𝚊𝚛𝚎 𝚟𝚎𝚛𝚒𝚏𝚒𝚎𝚍 𝚜𝚎𝚌𝚞𝚛𝚎𝚕𝚢. ✅"
        )
        markup = InlineKeyboardMarkup()
        markup.row(
            InlineKeyboardButton("💳 𝙿𝚊𝚢𝚝𝚖 𝚄𝙿𝙸", callback_data="btn_paytm_upi"),
            InlineKeyboardButton("🪙 𝙱𝚒𝚗𝚊𝚗𝚌𝚎 𝙿𝚊𝚢", callback_data="btn_binance_pay")
        )
        markup.add(InlineKeyboardButton("💰 𝚋𝙺𝚊𝚜𝚑 (𝚝𝚊𝚔𝚊)", callback_data="btn_bkash_pay"))
        markup.add(InlineKeyboardButton("🔙 𝙱𝙰𝙲𝙺", callback_data="btn_back"))
        bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=text, parse_mode="Markdown", reply_markup=markup)

    elif data == "btn_paytm_upi":
        bal = user_balances.get(user_id, 0.24)
        text = f"💸 *𝙰𝚍𝚍 𝙱𝚊𝚕𝚊𝚗𝚌𝚎 (𝙿𝚊𝚢𝚝𝚖 𝚄𝙿𝙸)*\n\n𝙲𝚞𝚛𝚛𝚎𝚗𝚝 𝚋𝚊𝚕𝚊𝚗𝚌𝚎: ₹{bal:.2f}\n\n𝙿𝚒𝚌𝚔 𝚊 𝚚𝚞𝚒𝚌𝚔 𝚊𝚖𝚘𝚞𝚗𝚝 𝚋𝚎𝚕𝚘𝚠, 𝚘𝚛 𝚎𝚗𝚝𝚎𝚛 𝚊 𝚌𝚞𝚜𝚝𝚘𝚖 𝚊𝚖𝚘𝚞𝚗𝚝.\n𝙼𝚒𝚗: ₹50.00 · 𝙼𝚊𝚡: ₹2,000.00"
        markup = InlineKeyboardMarkup()
        markup.row(InlineKeyboardButton("₹100", callback_data="pay_quick_100"), InlineKeyboardButton("₹500", callback_data="pay_quick_500"))
        markup.row(InlineKeyboardButton("₹1000", callback_data="pay_quick_1000"), InlineKeyboardButton("₹2000", callback_data="pay_quick_2000"))
        markup.add(InlineKeyboardButton("✏️ 𝙲𝚞𝚜𝚝𝚘𝚖 𝙰𝚖𝚘𝚞𝚗𝚝", callback_data="btn_custom_amount"))
        markup.add(InlineKeyboardButton("🖐 𝙱𝚊𝚌𝚔", callback_data="btn_balance"))
        bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=text, parse_mode="Markdown", reply_markup=markup)

    elif data == "btn_binance_pay":
        text = (
            f"🪙 *𝙱𝙸𝙽𝙰𝙽𝙲𝙴 𝙿𝙰𝚈 𝚂𝚈𝚂𝚃𝙴𝙼* 🪙\n\n"
            f"𝚂𝚎𝚗𝚍 𝚄𝚂𝙳𝚃 / 𝙲𝚛𝚢𝚙𝚝𝚘 𝚍𝚒𝚛𝚎𝚌𝚝𝚕𝚢 𝚝𝚘 𝚘𝚞𝚛 𝙱𝚒𝚗𝚊𝚗𝚌𝚎 𝙿𝚊𝚢 𝙸𝙳:\n\n"
            f"🆔 **𝙱𝚒𝚗𝚊𝚗𝚌𝚎 𝙿𝚊𝚢 𝙸𝙳:** `{BINANCE_PAY_ID}`\n\n"
            f"📌 *𝙸𝚗𝚜𝚝𝚛𝚞𝚌𝚝𝚒𝚘𝚗𝚜:*\n"
            f"1. 𝙾𝚙𝚎𝚗 𝙱𝚒𝚗𝚊𝚗𝚌𝚎 𝙰𝚙𝚙 -> 𝙿𝚊𝚢 𝚂𝚎𝚌𝚝𝚒𝚘𝚗\n"
            f"2. 𝙿𝚊𝚢 𝚝𝚑𝚎 𝚍𝚎𝚜𝚒𝚛𝚎𝚍 𝚄𝚂𝙳𝚃 𝚊𝚖𝚘𝚞𝚗𝚝.\n"
            f"3. 𝚂𝚎𝚗𝚍 𝚝𝚑𝚎 𝚙𝚊𝚢𝚖𝚎𝚗𝚝 𝚜𝚌𝚛𝚎𝚎𝚗𝚜𝚑𝚘𝚝 & 𝚃𝚛𝚊𝚗𝚜𝚊𝚌𝚝𝚒𝚘𝚗 𝙸𝙳 𝚝𝚘 𝙰𝚍𝚖𝚒𝚗 👉 @{clean_admin}"
        )
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("💬 𝚂𝚎𝚗𝚍 𝙿𝚛𝚘𝚘𝚏 𝚝𝚘 𝙰𝚍𝚖𝚒𝚗", url=f"https://t.me/{clean_admin}"))
        markup.add(InlineKeyboardButton("🖐 𝙱𝚊𝚌𝚔", callback_data="btn_balance"))
        bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=text, parse_mode="Markdown", reply_markup=markup)

    elif data == "btn_bkash_pay":
        text = (
            f"💰 *𝚋𝙺𝙰𝚂𝙷 𝙿𝙰𝚈𝙼𝙴𝙽𝚃 (𝚃𝙰𝙺𝙰)* 🇧🇩\n\n"
            f"𝙱𝚊𝚗𝚐𝚕𝚊𝚍𝚎𝚜𝚑 𝚋𝙺𝚊𝚜𝚑 𝚙𝚎𝚛𝚜𝚘𝚗𝚊𝚕 𝚙𝚊𝚢𝚖𝚎𝚗𝚝 𝚍𝚎𝚝𝚊𝚒𝚕:\n\n"
            f"📱 **𝚋𝙺𝚊𝚜𝚑 𝙿𝚎𝚛𝚜𝚘𝚗𝚊𝚕 𝙽𝚞𝚖𝚋𝚎𝚛:** `{BKASH_NUMBER}`\n\n"
            f"📌 *𝙸𝚗𝚜𝚝𝚛𝚞𝚌𝚝𝚒𝚘𝚗𝚜:*\n"
            f"1. 𝚄𝚜𝚎 𝚂𝚎𝚗𝚍 𝙼𝚘𝚗𝚎𝚢 𝚘𝚙𝚝𝚒𝚘𝚗.\n"
            f"2. 𝚂𝚎𝚗𝚍 𝚙𝚊𝚢𝚖𝚎𝚗𝚝 𝚊𝚌𝚌𝚘𝚛𝚍𝚒𝚗𝚐 𝚝𝚘 𝚛𝚊𝚝𝚎.\n"
            f"3. 𝚂𝚎𝚗𝚍 𝚃𝚛𝚊𝚗𝚜𝚊𝚌𝚝𝚒𝚘𝚗 𝚃𝚛𝚡𝙸𝙳 𝚊𝚗𝚍 𝚂𝚌𝚛𝚎𝚎𝚗𝚜𝚑𝚘𝚝 𝚝𝚘 𝙰𝚍𝚖𝚒𝚗 👉 @{clean_admin}"
        )
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("💬 𝚂𝚎𝚗𝚍 𝙿𝚛𝚘𝚘𝚏 𝚝𝚘 𝙰𝚍𝚖𝚒𝚗", url=f"https://t.me/{clean_admin}"))
        markup.add(InlineKeyboardButton("🖐 𝙱𝚊𝚌𝚔", callback_data="btn_balance"))
        bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=text, parse_mode="Markdown", reply_markup=markup)

    elif data == "btn_custom_amount":
        user_amount_input[user_id] = "0"
        text = "💰 *𝙴𝚗𝚝𝚎𝚛 𝙰𝚖𝚘𝚞𝚗𝚝*\n\n₹0\n\n𝙼𝚒𝚗: ₹50.00 · 𝙼𝚊𝚡: ₹2,000.00"
        bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=text, parse_mode="Markdown", reply_markup=create_keypad_markup("0"))

    elif data.startswith("num_"):
        val = user_amount_input.get(user_id, "0")
        action = data.replace("num_", "")
        if action.isdigit():
            val = action if val == "0" else val + action
        elif action == "clear":
            val = "0"
        elif action == "backspace":
            val = val[:-1]
            if not val:
                val = "0"

        user_amount_input[user_id] = val
        text = f"💰 *𝙴𝚗𝚝𝚎𝚛 𝙰𝚖𝚘𝚞𝚗𝚝*\n\n₹{val}\n\n𝙼𝚒𝚗: ₹50.00 · 𝙼𝚊𝚡: ₹2,000.00"
        bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=text, parse_mode="Markdown", reply_markup=create_keypad_markup(val))

    elif data == "confirm_custom_pay" or data.startswith("pay_quick_"):
        amount = int(data.replace("pay_quick_", "")) if data.startswith("pay_quick_") else int(user_amount_input.get(user_id, "0"))
        if amount < 50 or amount > 2000:
            bot.answer_callback_query(call.id, "⚠️ Amount Min ₹50 and Max ₹2,000 ke beech honi chahiye!", show_alert=True)
            return

        qr_url = f"https://api.qrserver.com/v1/create-qr-code/?size=300x300&data=upi://pay?pa={DEFAULT_UPI_ID}%26pn=Vicky%20Store%26am={amount}"
        text = f"💰 *𝙿𝙰𝚈𝙼𝙴𝙽𝚃 𝙳𝙴𝚃𝙰𝙸𝙻𝚂*\n\n𝚂𝚎𝚕𝚎𝚌𝚝𝚎𝚍 𝙰𝚖𝚘𝚞𝚗𝚝: ₹{amount}\n\n💳 *𝚄𝙿𝙸 𝙸𝙳:* `{DEFAULT_UPI_ID}`\n\n𝚀𝚁 𝚂𝚌𝚊𝚗 𝚔𝚊𝚛𝚔𝚎 𝚙𝚊𝚢 𝚔𝚊𝚛𝚎𝚒𝚗 𝚊𝚞𝚛 𝚜𝚌𝚛𝚎𝚎𝚗𝚜𝚑𝚘𝚝 𝚢𝚊𝚑𝚊 𝚋𝚑𝚎𝚓𝚎 👉 @{clean_admin}"
        bot.delete_message(chat_id=chat_id, message_id=message_id)
        bot.send_photo(chat_id=chat_id, photo=qr_url, caption=text, parse_mode="Markdown", reply_markup=back_markup)

    elif data == "btn_referral":
        bot_username = bot.get_me().username
        ref_link = f"https://t.me/{bot_username}?start={user_id}"
        text = f"👥 *𝙰𝙵𝙵𝙸𝙻𝙸𝙰𝚃𝙴 𝙿𝚁𝙾𝙶𝚁𝙰𝙼*\n\n✅ *𝚂𝚝𝚊𝚝𝚞𝚜:* 𝙰𝙲𝚃𝙸𝚅𝙴\n🏆 𝙴𝚊𝚛𝚗 15% 𝚌𝚘𝚖𝚖𝚒𝚜𝚜𝚒𝚘𝚗 𝚘𝚗 𝚎𝚟𝚎𝚛𝚢 𝚜𝚞𝚌𝚌𝚎𝚜𝚜𝚏𝚞𝚕 𝚙𝚞𝚛𝚌𝚑𝚊𝚜𝚎 𝚖𝚊𝚍𝚎 𝚋𝚢 𝚢𝚘𝚞𝚛 𝚛𝚎𝚏𝚎𝚛𝚛𝚎𝚍 𝚏𝚛𝚒𝚎𝚗𝚍𝚜!\n\n👥 𝚃𝚘𝚝𝚊𝚕 𝚁𝚎𝚏𝚎𝚛𝚛𝚎𝚍: 0\n💰 𝚃𝚘𝚝𝚊𝚕 𝙴𝚊𝚛𝚗𝚎𝚍: ₹0.00 (~ $0.00)\n\n🔗 *𝚈𝚘𝚞𝚛 𝙸𝚗𝚟𝚒𝚝𝚎 𝙻𝚒𝚗𝚔:*\n`{ref_link}`"
        bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=text, parse_mode="Markdown", reply_markup=back_markup)

    elif data == "btn_ludo":
        text = "🎁 *𝙻𝚄𝙳𝙾 𝚂𝙿𝙸𝙽 & 𝚆𝙸𝙽*\n\nचक्र घुमाएं और पुरस्कार जीतें!\n⏳ *नियम:* आप इसे 24 घंटे में सिर्फ 1 बार घुमा सकते हैं।"
        spin_markup = InlineKeyboardMarkup()
        spin_markup.add(InlineKeyboardButton("🎲 𝚂𝚙𝚒𝚗 𝙳𝚒𝚌𝚎 𝙽𝚘𝚠", callback_data="btn_dospin"))
        spin_markup.add(InlineKeyboardButton("🔙 𝙱𝙰𝙲𝙺", callback_data="btn_back"))
        bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=text, parse_mode="Markdown", reply_markup=spin_markup)

    elif data == "btn_dospin":
        current_time = time.time()
        cooldown_period = 86400  # 24 घंटे

        # 24 घंटे का कूलडाउन चेक
        if user_id in user_last_spin:
            elapsed_time = current_time - user_last_spin[user_id]
            if elapsed_time < cooldown_period:
                bot.delete_message(chat_id=chat_id, message_id=message_id)

                cooldown_text = (
                    "❌ *𝙲𝚘𝚘𝚕𝚍𝚘𝚠𝚗 𝙰𝚌𝚝𝚒𝚟𝚎!*\n"
                    "𝚈𝚘𝚞 𝚊𝚕𝚛𝚎𝚊𝚍𝚢 𝚙𝚕𝚊𝚢𝚎𝚍 𝚝𝚘𝚍𝚊𝚢. 𝙲𝚘𝚖𝚎 𝚋𝚊𝚌𝚔 𝚝𝚘𝚖𝚘𝚛𝚛𝚘𝚠."
                )

                back_markup_ludo = InlineKeyboardMarkup()
                back_markup_ludo.add(InlineKeyboardButton("↩️ 𝙱𝙰𝙲𝙺", callback_data="btn_ludo"))

                bot.send_message(
                    chat_id=chat_id,
                    text=cooldown_text,
                    parse_mode="Markdown",
                    reply_markup=back_markup_ludo
                )
                return

        user_last_spin[user_id] = current_time

        # मैसेज डिलीट करके डाइस रोल करें
        bot.delete_message(chat_id=chat_id, message_id=message_id)
        dice_msg = bot.send_dice(chat_id=chat_id, emoji='🎲')
        dice_value = dice_msg.dice.value

        rewards = {1: 0.10, 2: 0.20, 3: 0.30, 4: 0.40, 5: 0.50, 6: 1.00}
        won_amount = rewards.get(dice_value, 0.10)

        current_bal = user_balances.get(user_id, 0.24)
        new_balance = current_bal + won_amount
        user_balances[user_id] = new_balance

        time.sleep(3)

        usd_won = won_amount / 90.0
        usd_total = new_balance / 90.0

        spin_text = (
            f"🎁 *𝙻𝚄𝙲𝙺𝚈 𝙳𝙸𝙲𝙴 𝚁𝙴𝚂𝚄𝙻𝚃* 🔨💯\n\n"
            f"🎲 **𝙳𝚒𝚌𝚎 𝚅𝚊𝚕𝚞𝚎:** {dice_value}\n\n"
            f"💸 **𝚈𝚘𝚞 𝚆𝚘𝚗:** ₹{won_amount:.2f} (~ ${usd_won:.2f})\n"
            f"💰 **𝚃𝚘𝚝𝚊𝚕 𝙱𝚊𝚕𝚊𝚗𝚌𝚎:** ₹{new_balance:.2f} (~ ${usd_total:.2f})\n\n"
            f"𝙲𝚘𝚗𝚐𝚛𝚊𝚝𝚞𝚕𝚊𝚝𝚒𝚘𝚗𝚜! 𝙲𝚘𝚖𝚎 𝚋𝚊𝚌𝚔 𝚊𝚏𝚝𝚎𝚛 24 𝚑𝚘𝚞𝚛𝚜."
        )

        spin_markup = InlineKeyboardMarkup()
        spin_markup.add(InlineKeyboardButton("📚 𝙱𝙰𝙲𝙺 𝚃𝙾 𝙼𝙴𝙽𝚄", callback_data="btn_back"))

        bot.send_message(
            chat_id=chat_id,
            text=spin_text,
            parse_mode="Markdown",
            reply_to_message_id=dice_msg.message_id,
            reply_markup=spin_markup
        )

    elif data == "pnl_nonroot":
        text = "🛒 *𝙰𝙽𝙳𝚁𝙾𝙸𝙳 𝙽𝙾𝙽 𝚁𝙾𝙾𝚃 𝙿𝙰𝙽𝙴𝙻𝚂*\n\n✅ 𝙲𝚑𝚘𝚘𝚜𝚎 𝚊𝚗 𝚊𝚙𝚙:"
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("💥 𝚅𝙰𝙻𝙰 𝙼𝙾𝙳 𝙰𝙿𝙺", callback_data="app_vala_mod"))
        markup.add(InlineKeyboardButton("📱 𝙳𝚛𝚒𝚙 𝙲𝚕𝚒𝚎𝚗𝚝 𝙰𝚙𝚔", callback_data="app_drip"))
        markup.add(InlineKeyboardButton("📱 𝙳𝚛𝚒𝚙 𝙲𝚕𝚒𝚎𝚗𝚝 𝙿𝚛𝚘𝚡𝚢 𝙰𝚙𝚔", callback_data="app_drip_proxy"))
        markup.add(InlineKeyboardButton("📱 𝙿𝚛𝚒𝚖𝚎 𝙷𝚘𝚘𝚔 𝙰𝚙𝚔", callback_data="app_prime"))
        markup.add(InlineKeyboardButton("📱 𝙷𝙶 𝙿𝚛𝚘𝚡𝚢 𝙰𝚙𝚔", callback_data="app_hg_proxy"))
        markup.add(InlineKeyboardButton("📱 𝙿𝚊𝚝𝚘𝚝𝚎𝚊𝚖 𝙾𝚛𝚊𝚗𝚐𝚎", callback_data="app_patorange"))
        markup.add(InlineKeyboardButton("📱 𝙿𝚊𝚝𝚘𝚝𝚎𝚊𝚖 𝙱𝚕𝚞𝚎", callback_data="app_patblue"))
        markup.add(InlineKeyboardButton("📱 𝙱𝚛 𝙼𝚘𝚍𝚜 𝙽𝚘𝚗 𝚁𝚘𝚘𝚝", callback_data="app_brmods_nr"))
        markup.add(InlineKeyboardButton("📱 𝚁𝚎𝚊𝚙𝚎𝚛 𝚡𝙿𝚛𝚘 𝙰𝚙𝚔", callback_data="app_reaper_nr"))
        markup.add(InlineKeyboardButton("📱 𝚂𝚒𝚕𝚎𝚗𝚝 𝙲𝚑𝚎𝚊𝚝𝚜 𝙰𝚙𝚔𝚖𝚘𝚍", callback_data="app_silent_nr"))
        markup.add(InlineKeyboardButton("🔙 𝙱𝙰𝙲𝙺 𝚃𝙾 𝙿𝙰𝙽𝙴𝙻𝚂", callback_data="btn_store"))
        bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=text, parse_mode="Markdown", reply_markup=markup)

    elif data == "pnl_root":
        text = "🛒 *𝙰𝙽𝙳𝚁𝙾𝙸𝙳 𝚁𝙾𝙾𝚃 𝙿𝙰𝙽𝙴𝙻𝚂*\n\n✅ 𝙲𝚑𝚘𝚘𝚜𝚎 𝚊𝚗 𝚊𝚙𝚙:"
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("📱 𝙱𝚛 𝙼𝚘𝚍𝚜 𝙰𝚙𝚔", callback_data="app_brmods_root"))
        markup.add(InlineKeyboardButton("📱 𝚁𝚎𝚊𝚙𝚎𝚛 𝚡 𝙿𝚛𝚘", callback_data="app_reaper_root"))
        markup.add(InlineKeyboardButton("📱 𝙳𝚛𝚒𝚙 𝙲𝚕𝚒𝚎𝚗𝚝 𝚁𝚘𝚘𝚝", callback_data="app_drip_root"))
        markup.add(InlineKeyboardButton("📱 𝙷𝚐 𝙲𝚑𝚎𝚊𝚝𝚜 𝙰𝚙𝚔", callback_data="app_hg_root"))
        markup.add(InlineKeyboardButton("📱 𝚂𝚝𝚛𝚒𝚌𝚔𝚜 𝙱𝚛 ~ 𝙰𝚕𝚙𝚑𝚊", callback_data="app_stricks"))
        markup.add(InlineKeyboardButton("📱 𝚇𝚢𝚣 𝙲𝚑𝚎𝚊𝚝𝚜 𝙰𝚙𝚔", callback_data="app_xyz"))
        markup.add(InlineKeyboardButton("📱 𝙷𝚒𝚔𝚊𝚛𝚒 𝙼𝚘𝚍 𝙰𝚙𝚔", callback_data="app_hikari"))
        markup.add(InlineKeyboardButton("📱 𝙻𝚔 𝚃𝚎𝚊𝚖 𝙰𝚙𝚔", callback_data="app_lk"))
        markup.add(InlineKeyboardButton("📱 𝚂𝚒𝚕𝚎𝚗𝚝 𝙲𝚑𝚎𝚊𝚝𝚜 [𝚂𝚊𝚏𝚎]", callback_data="app_safe"))
        markup.add(InlineKeyboardButton("📱 𝚂𝚒𝚕𝚎𝚗𝚝 𝙲𝚑𝚎𝚊𝚝𝚜 [𝙱𝚛𝚞𝚝𝚊𝚕]", callback_data="app_brutal"))
        markup.add(InlineKeyboardButton("📱 𝚇𝚛𝚎𝚐 𝚂𝚊𝚏𝚎 𝙰𝚙𝚔", callback_data="app_xreg"))
        markup.add(InlineKeyboardButton("📱 𝚁𝚊𝚙𝚒𝚍 𝙲𝚘𝚛𝚎 𝙰𝚙𝚔", callback_data="app_rapid"))
        markup.add(InlineKeyboardButton("📱 𝙷𝚊𝚡𝚡-𝚌𝚔𝚎𝚛 𝙿𝚛𝚘", callback_data="app_haxx"))
        markup.add(InlineKeyboardButton("📱 𝚉𝚢𝚝𝚛𝚘𝚗 𝙿𝚛𝚘 𝙰𝚙𝚔", callback_data="app_zytron"))
        markup.add(InlineKeyboardButton("📱 𝙰𝚗𝚐𝚛𝚢 𝙼𝚘𝚍 𝙰𝚙𝚔", callback_data="app_angry"))
        markup.add(InlineKeyboardButton("📱 𝚂𝚌𝚘𝚛𝚙𝚒𝚘 𝙼𝚘𝚍𝚜 [𝙻𝚒𝚝𝚎]", callback_data="app_scorpio_lite"))
        markup.add(InlineKeyboardButton("📱 𝚂𝚌𝚘𝚛𝚙𝚒𝚘 𝙼𝚘𝚍𝚜 [𝙱𝚛𝚞𝚝𝚊𝚕]", callback_data="app_scorpio_brutal"))
        markup.add(InlineKeyboardButton("🔙 𝙱𝙰𝙲𝙺 𝚃𝙾 𝙿𝙰𝙽𝙴𝙻𝚂", callback_data="btn_store"))
        bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=text, parse_mode="Markdown", reply_markup=markup)

    elif data == "pnl_iphone":
        text = "🛒 *𝙸𝙿𝙷𝙾𝙽𝙴 𝙿𝙰𝙽𝙴𝙻𝚂*\n\n✅ 𝙲𝚑𝚘𝚘𝚜𝚎 𝚊𝚗 𝚊𝚙𝚙:"
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("🍏 𝙶𝚋𝚘𝚡 𝙲𝚎𝚛𝚝𝚒𝚏𝚒𝚌𝚊𝚝𝚎", callback_data="app_gbox"))
        markup.add(InlineKeyboardButton("🍏 𝙴𝚜𝚒𝚗𝚐 𝙲𝚎𝚛𝚝𝚒𝚏𝚒𝚌𝚊𝚝𝚎", callback_data="app_esing"))
        markup.add(InlineKeyboardButton("🍏 𝙵𝚕𝚞𝚘𝚛𝚒𝚝𝚎 𝙸𝚘𝚜", callback_data="app_fluorite"))
        markup.add(InlineKeyboardButton("🍏 𝙼𝚒𝚐𝚞𝚕 ~ 𝙿𝚛𝚘", callback_data="app_migul_pro"))
        markup.add(InlineKeyboardButton("🍏 𝙼𝚒𝚐𝚞𝚕 ~ 𝙱𝚊𝚜𝚒𝚌", callback_data="app_migul_basic"))
        markup.add(InlineKeyboardButton("🔙 𝙱𝙰𝙲𝙺 𝚃𝙾 𝙿𝙰𝙽𝙴𝙻𝚂", callback_data="btn_store"))
        bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=text, parse_mode="Markdown", reply_markup=markup)

    elif data == "pnl_pc":
        text = "🛒 *𝙿𝙲 𝙿𝙰𝙽𝙴𝙻𝚂*\n\n✅ 𝙲𝚑𝚘𝚘𝚜𝚎 𝚊𝚗 𝚊𝚙𝚙:"
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("💻 𝙳𝚛𝚒𝚙 𝙲𝚕𝚒𝚎𝚗𝚝 𝙿𝚌", callback_data="app_drip_pc"))
        markup.add(InlineKeyboardButton("💻 𝙱𝚛 𝙼𝚘𝚍𝚜 𝙿𝚌", callback_data="app_brmods_pc"))
        markup.add(InlineKeyboardButton("🔙 𝙱𝙰𝙲𝙺 𝚃𝙾 𝙿𝙰𝙽𝙴𝙻𝚂", callback_data="btn_store"))
        bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=text, parse_mode="Markdown", reply_markup=markup)

    elif data.startswith("app_"):
        app_code = data.replace("app_", "")
        filename = f"{app_code}_keys.txt"
        stock = get_stock_count(filename)
        stock_status = "📦 ✅ 𝙸𝚗 𝚂𝚝𝚘𝚌𝚔" if stock > 0 else "📦 ❌ 𝙾𝚞𝚝 𝚘𝚏 𝚂𝚝𝚘𝚌𝚔"

        default_app = {"name": app_code.upper(), 1: 80, 7: 300, 30: 700}
        app_data = APP_PRICES.get(app_code, default_app)
        app_title = app_data["name"]

        text = f"🛒 *𝙿𝙰𝙽𝙴𝙻 - {app_title.upper()} 𝙿𝙰𝙲𝙺𝙰𝙶𝙴𝚂*\n━━━━━━━━━━━━━━━━━━\n\n"
        for duration, price in app_data.items():
            if duration != "name":
                usd_price = round(price / 90.0, 2)
                val_text = f"{duration} 𝙳𝚊𝚢𝚜" if isinstance(duration, int) else f"{duration}"
                text += f"🛒 ⏱️ **𝚅𝚊𝚕𝚒𝚍𝚒𝚝𝚢: {val_text}**\n💰 𝙿𝚛𝚒𝚌𝚎: ₹{price}.00 (~ ${usd_price})\n📱 𝙻𝚒𝚖𝚒𝚝: 1 𝙳𝚎𝚟𝚒𝚌𝚎 | {stock_status}\n\n"
        text += "✅ *𝚂𝚎𝚕𝚎𝚌𝚝 𝚙𝚊𝚌𝚔𝚊𝚐𝚎 𝚋𝚎𝚕𝚘𝚠 𝚝𝚘 𝚒𝚗𝚜𝚝𝚊𝚗𝚝𝚕𝚢 𝚙𝚞𝚛𝚌𝚑𝚊𝚜𝚎:*"

        markup = InlineKeyboardMarkup()
        for duration, price in app_data.items():
            if duration != "name":
                usd_price = round(price / 90.0, 2)
                val_text = f"{duration} 𝙳𝚊𝚢𝚜" if isinstance(duration, int) else f"{duration}"
                if stock > 0:
                    markup.add(InlineKeyboardButton(f"🛒 𝙱𝚞𝚢 {val_text} - ₹{price}.00 (~ ${usd_price})", callback_data=f"buy_{app_code}_{duration}"))
                else:
                    markup.add(InlineKeyboardButton(f"❌ {val_text} (𝙾𝚞𝚝 𝚘𝚏 𝚂𝚝𝚘𝚌𝚔)", callback_data=f"oos_{app_code}_{duration}"))

        back_btn = "btn_store"
        if app_code in ["vala_mod", "drip", "drip_proxy", "prime", "hg_proxy", "patorange", "patblue", "brmods_nr", "reaper_nr", "silent_nr"]:
            back_btn = "pnl_nonroot"
        elif app_code in ["brmods_root", "reaper_root", "drip_root", "hg_root", "stricks", "xyz", "hikari", "lk", "safe", "brutal", "xreg", "rapid", "haxx", "zytron", "angry", "scorpio_lite", "scorpio_brutal"]:
            back_btn = "pnl_root"
        elif app_code in ["gbox", "esing", "fluorite", "migul_pro", "migul_basic"]:
            back_btn = "pnl_iphone"
        elif app_code in ["drip_pc", "brmods_pc"]:
            back_btn = "pnl_pc"

        markup.add(InlineKeyboardButton("🔙 𝙱𝙰𝙲𝙺 𝚃𝙾 𝙿𝙰𝙽𝙴𝙻𝚂", callback_data=back_btn))
        bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=text, parse_mode="Markdown", reply_markup=markup)

    elif data.startswith("buy_"):
        parts = data.split("_")
        duration_selected = parts[-1]
        app_code_selected = "_".join(parts[1:-1])

        if user_id not in user_purchase_history:
            user_purchase_history[user_id] = []

        purchase_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        app_real_name = APP_PRICES.get(app_code_selected, {}).get("name", app_code_selected.upper())

        user_purchase_history[user_id].append({
            "app": app_real_name,
            "duration": duration_selected,
            "price": "देखें",
            "time": purchase_time
        })

        bot.answer_callback_query(call.id, f"आपने {duration_selected} वाला पैक चुना है!", show_alert=True)
        bot.send_message(
            chat_id=chat_id,
            text=f"🛒 आपने **{app_real_name}** का **{duration_selected}** वाला पैक सेलेक्ट किया है।\n\n💰 बैलेंस एड करने या खरीदने के लिए एडमिन से संपर्क करें 👉 @{clean_admin}",
            parse_mode="Markdown"
        )

    elif data.startswith("oos_"):
        bot.answer_callback_query(call.id, "⚠️ यह पैकेज अभी स्टॉक में उपलब्ध नहीं है!", show_alert=True)

print("Bot fixed and running perfectly...")
bot.polling(none_stop=True)
