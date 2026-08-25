import os
import random
import time
import json
from datetime import datetime
import telebot
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

TOKEN = "8849298752:AAFKpZRS8gtzYBvm81OSx8jLB6uN9IV93Kw"
bot = telebot.TeleBot(TOKEN)

# PERMANENT DATA STORES
SPIN_FILE = "user_spins.json"
ALL_USERS_FILE = "all_users.json"
BUYERS_FILE = "buyers.json"
VERIFIED_USERS_FILE = "verified_users.json"

def load_json_data(file_path, default_type=dict):
    if os.path.exists(file_path):
        try:
            with open(file_path, "r") as f:
                return json.load(f)
        except:
            return default_type()
    return default_type()

def save_json_data(file_path, data):
    with open(file_path, "w") as f:
        json.dump(data, f)

# Memory Stores - Strict String conversion for precise matching
user_last_spin = load_json_data(SPIN_FILE, dict)
all_users = set(map(str, load_json_data(ALL_USERS_FILE, list)))
buyer_users = set(map(str, load_json_data(BUYERS_FILE, list)))
verified_users = set(map(str, load_json_data(VERIFIED_USERS_FILE, list)))

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
    "vala_mod": {"name": "VALA MOD APK", "emoji": "⚡", "1 Hour": 45, "3 Hours": 100, "6 Hours": 150, "12 Hours": 250, "24 Hours": 400},
    "drip": {"name": "Drip Client Apk", "emoji": "💧", 1: 80, 3: 160, 7: 270, 15: 420, 30: 620},
    "drip_proxy": {"name": "Drip Client Proxy Apk", "emoji": "🌐", 1: 80, 3: 160, 7: 270, 30: 620},
    "hg_cheats_nr": {"name": "Hg Cheats Apk", "emoji": "👾", 1: 55, 7: 140, 10: 179, 30: 425},
    "prime": {"name": "Prime Hook Apk", "emoji": "👑", 1: 95, 3: 160, 7: 315},
    "hg_proxy": {"name": "Hg Proxy Apk", "emoji": "🛡️", 1: 100, 7: 240, 10: 310, 30: 605},
    "patorange": {"name": "Patoteam Orange", "emoji": "🍊", 3: 230, 7: 370, 15: 605, 30: 960},
    "patblue": {"name": "Patoteam Blue", "emoji": "🔵", 3: 265, 7: 440, 15: 640, 30: 1020},
    "brmods_nr": {"name": "Br Mods Non Root", "emoji": "🔥", 1: 90, 7: 270, 15: 460, 30: 640},
    "reaper_nr": {"name": "Reaper xPro Apk", "emoji": "☠️", 10: 365, 30: 900},
    "silent_nr": {"name": "Silent Cheats Apkmod", "emoji": "🤫", 1: 110, 3: 200, 7: 370, 14: 620, 28: 920},
    "ninex": {"name": "NineX Mod Injector", "emoji": "💉", 10: 420, 20: 800, 30: 1200},
    "abcd": {"name": "ABCD Panel", "emoji": "🔤", "12 Hours": 30, 1: 90, 3: 150, 7: 200},
    "pato_regedit": {"name": "Patoteam Regedit Orange", "emoji": "⚙️", 3: 200, 7: 330, 15: 500, 30: 920},
    "aimhack": {"name": "AimHack Apk", "emoji": "🎯", "1 Hour": 20, "3 Hours": 35, "6 Hours": 55, "12 Hours": 110},
    "brmods_root": {"name": "Br Mods Apk", "emoji": "🔓", 1: 79, 7: 260, 15: 440, 30: 620},
    "reaper_root": {"name": "Reaper x Pro", "emoji": "⚔️", 10: 345, 30: 795},
    "drip_root": {"name": "Drip Client Root", "emoji": "💦", 1: 70, 7: 320, 30: 650},
    "hg_root": {"name": "Hg Cheats Apk (Root)", "emoji": "🎯", 1: 80, 7: 190, 10: 290, 30: 590},
    "stricks": {"name": "Stricks Br ~ Alpha", "emoji": "⚡", 1: 70, 5: 160, 7: 250, 15: 450, 30: 600},
    "xyz": {"name": "Xyz Cheats Apk", "emoji": "🧪", 1: 70, 3: 150, 7: 300, 15: 500, 30: 790},
    "hikari": {"name": "Hikari Mod Apk", "emoji": "✨", 1: 70, 3: 149, 7: 299, 15: 499, 30: 799},
    "lk": {"name": "LK Team Apk", "emoji": "🛡️", 1: 80, 5: 170, 10: 250, 30: 690},
    "safe": {"name": "Silent Cheats [Safe]", "emoji": "🟢", 1: 80, 3: 170, 7: 340, 14: 580, 28: 850},
    "brutal": {"name": "Silent Cheats [Brutal]", "emoji": "🔴", 1: 80, 3: 170, 7: 340, 14: 585, 30: 895},
    "xreg": {"name": "Xreg Safe Apk", "emoji": "⚙️", 1: 90, 10: 300, 20: 500, 30: 680},
    "rapid": {"name": "Rapid Core Apk", "emoji": "🚀", 1: 89, 7: 299, 14: 549, 30: 1099},
    "haxx": {"name": "Haxx-cker Pro", "emoji": "☣️", 10: 545, 20: 1030, 30: 1400},
    "zytron": {"name": "Zytron Pro Apk", "emoji": "🤖", 1: 80, 7: 320, 15: 480, 30: 620},
    "angry": {"name": "Angry Mod Apk", "emoji": "😡", 1: 75, 7: 320, 15: 530, 30: 750},
    "scorpio_lite": {"name": "Scorpio Mods [Lite]", "emoji": "🦂", 7: 240, 15: 400, 30: 600},
    "scorpio_brutal": {"name": "Scorpio Mods [Brutal]", "emoji": "🦂", 7: 300, 15: 450, 30: 800},
    "gbox": {"name": "Gbox Certificate", "emoji": "📜", "1 year validity": 1000},
    "esing": {"name": "Esing Certificate", "emoji": "🔑", "1 year validity": 500},
    "fluorite": {"name": "Fluorite Ios", "emoji": "💎", 1: 390, 7: 1240, 31: 2000},
    "migul_pro": {"name": "Migul ~ Pro", "emoji": "🏆", 1: 300, 7: 890, 31: 1700},
    "migul_basic": {"name": "Migul ~ Basic", "emoji": "🔰", 1: 220, 7: 530, 31: 1320},
    # NAYA ITEM ADDED (iPhone Panel)
    "alpha_regedit": {"name": "AlphaRegedit External", "emoji": "🍎", 1: 90, 3: 180, 7: 350, 30: 800},
    "drip_pc": {"name": "Drip Client Pc", "emoji": "🖥️", 1: 150, 7: 360, 15: 650, 30: 1020},
    "brmods_pc": {"name": "Br Mods Pc", "emoji": "💻", 1: 85, 10: 350, 30: 690},
    # NAYA ITEM ADDED (PC Panel)
    "only_exe": {"name": "Only Exe Aimkill", "emoji": "🛒", 1: 60, 3: 150, 7: 290, 30: 780}
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
    markup.add(InlineKeyboardButton(f"✅ Confirm ₹{current_val}", callback_data="confirm_custom_pay"))
    markup.add(InlineKeyboardButton("🖐 Back", callback_data="btn_paytm_upi"))
    return markup

# --- START COMMAND ---
@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_id = str(message.chat.id)
    user_name = message.from_user.first_name if message.from_user.first_name else "User"
    
    if user_id not in all_users:
        all_users.add(user_id)
        save_json_data(ALL_USERS_FILE, list(all_users))

    if user_id not in verified_users:
        markup = ReplyKeyboardMarkup(row_width=1, resize_keyboard=True, one_time_keyboard=True)
        btn_contact = KeyboardButton("📱 Share Contact to Verify", request_contact=True)
        markup.add(btn_contact)
        
        verify_text = (
            f"🔒 𝗩𝗘𝗥𝗜𝗙𝗜𝗖𝗔𝗧𝗜𝗢𝗡 𝗥𝗘𝗤𝗨𝗜𝗥𝗘𝗗\n"
            f"━━━━━━━━━━━━━━━━━━━━━\n"
            f"𝗣𝗹𝗲𝗮𝘀𝗲 𝘀𝗵𝗮𝗿𝗲 𝘆𝗼𝘂𝗿 𝗰𝗼𝗻𝘁𝗮𝗰𝘁 𝗼𝗻𝗰𝗲 𝘁𝗼 𝘀𝘁𝗮𝗿𝘁 𝘂𝘀𝗶𝗻𝗴 𝘁𝗵𝗲 𝘀𝗵𝗼𝗽 𝘀𝗲𝗿𝘃𝗶𝗰𝗲𝘀."
        )
        bot.send_message(message.chat.id, verify_text, reply_markup=markup, parse_mode='Markdown')
    else:
        show_main_menu(message.chat.id, user_name)

@bot.message_handler(content_types=['contact'])
def handle_contact(message):
    user_id = str(message.from_user.id)
    user_name = message.from_user.first_name if message.from_user.first_name else "User"
    if message.contact is not None:
        verified_users.add(user_id)
        save_json_data(VERIFIED_USERS_FILE, list(verified_users))
        
        remove_markup = ReplyKeyboardRemove()
        bot.send_message(
            message.chat.id, 
            "✅ 𝗩𝗲𝗿𝗶𝗳𝗶𝗰𝗮𝘁𝗶𝗼𝗻 𝗖𝗼𝗺𝗽𝗹𝗲𝘁𝗲𝗱!", 
            reply_markup=remove_markup, 
            parse_mode='Markdown'
        )
        show_main_menu(message.chat.id, user_name)

def show_main_menu(chat_id, user_name="User"):
    welcome_text = (
        f"𝗪𝗘𝗟𝗖𝗢𝗠𝗘 𝗧𝗢 𝗩𝗜𝗖𝗞𝗬 𝗫 𝗠𝗢𝗗𝗘 𝗦𝗛𝗢𝗣 🔒\n"
        "━━━━━━━━━━━━━━━━━━━━━━\n\n"
        f"👏 𝗛𝗘𝗟𝗟𝗢 {user_name.upper()}!\n\n"
        "━━━━━━━━━━━━━━━━━━━━━━\n"
        "💫 𝗪𝗛𝗬 𝗖𝗛𝗢𝗢𝗦𝗘 𝗨𝗦?\n\n"
        "🔒 𝗙𝗮𝘀𝘁𝗲𝘀𝘁 𝗗𝗲𝗹𝗶𝘃𝗲𝗿𝘆\n"
        "🔒 𝟭𝟬𝟬% 𝗔𝘂𝘁𝗼𝗺𝗮𝘁𝗲𝗱\n"
        "🔒 𝟮𝟰𝘅𝟳 𝗗𝗲𝗱𝗶𝗰𝗮𝘁𝗲𝗱 𝗦𝘂𝗽𝗽𝗼𝗿𝘁\n"
        "🔒 𝗕𝗲𝘀𝘁 𝗖𝗼𝗺𝗽𝗲𝘁𝗶𝘁𝗶𝘃𝗲 𝗣𝗿𝗶𝗰𝗲𝘀\n\n"
        "━━━━━━━━━━━━━━━━━━━━━━\n"
        "🔒 𝐒ᴇʟᴇᴄᴛ 𝐀ɴ 𝐎ᴘᴛɪᴏɴ 𝐅ʀᴏᴍ 𝐓ʜᴇ 𝐌ᴇɴᴜ 𝐁ᴇʟᴏᴡ :"
    )

    markup = InlineKeyboardMarkup()
    btn_store = InlineKeyboardButton("🛒 Product Store", callback_data="btn_store")
    btn_profile = InlineKeyboardButton("👤 My Profile", callback_data="btn_profile")
    btn_balance = InlineKeyboardButton("💰 Add Balance", callback_data="btn_balance")
    btn_history = InlineKeyboardButton("🔑 All History", callback_data="btn_history")
    btn_referral = InlineKeyboardButton("👥 Referral", callback_data="btn_referral")
    btn_support = InlineKeyboardButton("🌐 Support", callback_data="btn_support")
    btn_ludo = InlineKeyboardButton("🎁 Ludo Spin", callback_data="btn_ludo")
    btn_download = InlineKeyboardButton("📥 Download Files", callback_data="btn_download")

    markup.add(btn_store)
    markup.row(btn_profile, btn_balance)
    markup.row(btn_history, btn_referral)
    markup.row(btn_support, btn_ludo)
    markup.add(btn_download)

    bot.send_message(chat_id, welcome_text, reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def callback_listener(call):
    user_id = call.from_user.id
    user_name = call.from_user.first_name if call.from_user.first_name else "User"
    str_user_id = str(user_id)
    chat_id = call.message.chat.id
    message_id = call.message.message_id
    data = call.data

    clean_admin = ADMIN_TELEGRAM_USERNAME.replace("@", "").strip()
    back_markup = InlineKeyboardMarkup()
    back_markup.add(InlineKeyboardButton("🔙 BACK", callback_data="btn_back"))

    if data == "btn_back":
        bot.delete_message(chat_id=chat_id, message_id=message_id)
        show_main_menu(chat_id, user_name)

    elif data == "btn_store":
        text = (
            "━━━━━━━━━━━━━━━━━━━━\n"
            "🔒 𝗖𝗛𝗢𝗢𝗦𝗘 𝗬𝗢𝗨𝗥 𝗗𝗘𝗩𝗜𝗖𝗘 𝗖𝗔𝗧𝗘𝗚𝗢𝗥𝗬 🔒\n"
            "━━━━━━━━━━━━━━━━━━━━\n\n"
            "• 🔒 𝗣𝗥𝗘𝗠𝗜𝗨𝗠 𝗠𝗢𝗗𝗦, 𝗣𝗔𝗡𝗘𝗟𝗦\n"
            "━━━━━━━━━━━━━━━━━━━━\n"
            "• 🔒 𝗜𝗡𝗦𝗧𝗔𝗡𝗧 𝗗𝗘𝗟𝗜𝗩𝗘𝗥\n"
            "━━━━━━━━━━━━━━━━━━━━\n"
            "• 🔒 𝗩𝗘𝗥𝗜𝗙𝗜𝗘𝗗 𝗦𝗘𝗟𝗟𝗘𝗥𝗦\n"
            "━━━━━━━━━━━━━━━━━━━━\n"
            "• 🔒 𝗧𝗥𝗨𝗦𝗧𝗘𝗗 𝗕𝗬 𝟭𝟬𝟬𝟬+ 𝗕𝗨𝗬𝗘𝗥𝗦\n\n"
            "━━━━━━━━━━━━━━━━━━━━\n"
            "🔒 𝗧𝗮𝗽 𝗮 𝗰𝗮𝘁𝗲𝗴𝗼𝗿𝘆 𝗯𝗲𝗹𝗼𝘄 𝘁𝗼 𝗴𝗲𝘁 𝘀𝘁𝗮𝗿𝘁𝗲𝗱:"
        )
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("🤖 ANDROID NON ROOT PANEL", callback_data="pnl_nonroot"))
        markup.add(InlineKeyboardButton("🔓 ANDROID ROOT PANEL", callback_data="pnl_root"))
        markup.add(InlineKeyboardButton("🍎 IPHONE PANEL", callback_data="pnl_iphone"))
        markup.add(InlineKeyboardButton("💻 PC PANEL", callback_data="pnl_pc"))
        markup.add(InlineKeyboardButton("🔙 BACK", callback_data="btn_back"))
        bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=text, parse_mode="Markdown", reply_markup=markup)

    elif data == "btn_profile":
        user_name_prof = call.from_user.first_name
        join_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        bal = user_balances.get(user_id, 0.24)
        profile_text = (
            f"👤 𝗬𝗢𝗨𝗥 𝗦𝗘𝗖𝗨𝗥𝗘 𝗣𝗥𝗢𝗙𝗜𝗟𝗘 👤\n\n"
            f"👤 𝗚𝗿𝗶𝗱 𝗜𝗗: `{user_id}`\n"
            f"👑 𝗡𝗮𝗺𝗲: {user_name_prof}\n"
            f"👑 𝗔𝗰𝗰𝗼𝘂𝗻𝘁 𝗟𝗲𝘃𝗲𝗹: 👤 𝗥𝗲𝗴𝘂𝗹𝗮𝗿 𝗨𝘀𝗲𝗿\n\n"
            f"💰 𝗪𝗮𝗹𝗹𝗲𝘁 🪙\n"
            f"💰 𝗖𝘂𝗿𝗿𝗲𝗻𝘁 𝗕𝗮𝗹𝗮𝗻𝗰𝗲: ₹{bal:.2f} (~ ${(bal/90.0):.2f}) 🪙\n\n"
            f"📈 𝗚𝗹𝗼𝗯𝗮𝗹 𝗦𝘁𝗮𝘁𝗶𝘀𝘁𝗶𝗰𝘀\n"
            f"🗂️ 𝗧𝗼𝘁𝗮𝗹 𝗢𝗿𝗱𝗲𝗿𝘀: {len(user_purchase_history.get(user_id, []))}\n"
            f"💸 𝗧𝗼𝘁𝗮𝗹 𝗦𝗽𝗲𝗻𝘁: ₹0.00 (~ $0.00)\n"
            f"👥 𝗧𝗼𝘁𝗮𝗹 𝗥𝗲𝗳𝗲𝗿𝗿𝗮𝗹𝘀: 0\n\n"
            f"📅 𝗝𝗼𝗶𝗻𝗲𝗱 𝗚𝗿𝗶𝗱: {join_date}"
        )
        profile_markup = InlineKeyboardMarkup()
        profile_markup.add(InlineKeyboardButton("🎁 Redeem Promo Code", callback_data="btn_redeem"))
        profile_markup.add(InlineKeyboardButton("🔙 BACK", callback_data="btn_back"))
        bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=profile_text, parse_mode="Markdown", reply_markup=profile_markup)

    elif data == "btn_redeem":
        bot.answer_callback_query(call.id, "⚠️ आपके पास कोई वैलिड प्रोमो कोड नहीं है!", show_alert=True)

    elif data == "btn_support":
        text = (
            "🌐💬 𝗣𝗥𝗘𝗠𝗜𝗨𝗠 𝗦𝗨𝗣𝗣𝗢𝗥𝗧 𝗖𝗘𝗡𝗧𝗘𝗥\n\n"
            "𝗖𝗼𝗻𝘁𝗮𝗰𝘁 𝘂𝘀 𝘃𝗶𝗮 𝗧𝗲𝗹𝗲𝗴𝗿𝗮𝗺 𝗼𝗿 𝗪𝗵𝗮𝘁𝘀𝗔𝗽𝗽 𝗳𝗼𝗿 𝗶𝗻𝘀𝘁𝗮𝗻𝘁 𝗵𝗲𝗹𝗽, 𝗼𝗿 𝗼𝗽𝗲𝗻 𝗮 𝘀𝘂𝗽𝗽𝗼𝗿𝘁 𝘁𝗶𝗰𝗸𝗲𝘁 𝗳𝗼𝗿 𝗮𝗱𝗺𝗶𝗻 𝗮𝘀𝘀𝗶𝘀𝘁𝗮𝗻𝗰𝗲."
        )
        support_markup = InlineKeyboardMarkup()
        support_markup.add(InlineKeyboardButton("✈️ Contact on Telegram", url=f"https://t.me/{clean_admin}"))
        support_markup.add(InlineKeyboardButton("💬 Contact on WhatsApp", url=f"https://wa.me/{ADMIN_WHATSAPP_NUM}"))
        support_markup.row(
            InlineKeyboardButton("🎫 Open New Ticket", callback_data="ticket_open"),
            InlineKeyboardButton("📋 My Open Tickets", callback_data="ticket_view")
        )
        support_markup.add(InlineKeyboardButton("🔙 BACK", callback_data="btn_back"))
        bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=text, parse_mode="Markdown", reply_markup=support_markup)

    elif data == "ticket_open":
        user_ticket_state[user_id] = "WAITING_FOR_TICKET"
        text = "🎫 𝗢𝗣𝗘𝗡 𝗦𝗨𝗣𝗣𝗢𝗥𝗧 𝗧𝗜𝗖𝗞𝗘𝗧\n\n𝗞𝗿𝗶𝗽𝘆𝗮 𝗮𝗽𝗻𝗶 𝘀𝗮𝗺𝗮𝘀𝘆𝗮 𝗻𝗶𝗰𝗵𝗲 𝘁𝘆𝗽𝗲 𝗸𝗮𝗿𝗸𝗲 𝗺𝗲𝘀𝘀𝗮𝗴𝗲 𝗸𝗮𝗿𝗲𝗶𝗻.\n\n📌 𝗘𝘅𝗮𝗺𝗽𝗹𝗲: My balance is not added / Key not working."
        cancel_markup = InlineKeyboardMarkup()
        cancel_markup.add(InlineKeyboardButton("❌ Cancel", callback_data="btn_support"))
        bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=text, parse_mode="Markdown", reply_markup=cancel_markup)

    elif data == "ticket_view":
        user_tickets = [t_id for t_id, data in support_tickets.items() if data['user_id'] == user_id]
        if not user_tickets:
            text = "📋 𝗠𝗬 𝗢𝗣𝗘𝗡 𝗧𝗜𝗖𝗞𝗘𝗧𝗦\n\n𝗔𝗮𝗽𝗸𝗮 𝗸𝗼𝗶 𝗯𝗵𝗶 𝘀𝘂𝗽𝗽𝗼𝗿𝘁 𝘁𝗶𝗰𝗸𝗲𝘁 𝗮𝗯𝗵𝗶 𝗮𝗰𝘁𝗶𝘃𝗲 𝗻𝗮𝗵𝗶 𝗵𝗮𝗶."
        else:
            text = "📋 𝗠𝗬 𝗧𝗜𝗖𝗞𝗘𝗧𝗦 𝗦𝗧𝗔𝗧𝗨𝗦\n\n"
            for t_id in user_tickets:
                info = support_tickets[t_id]
                text += f"🎫 𝗜𝗗: `{t_id}`\n📝 𝗜𝘀𝘀𝘂𝗲: {info['issue']}\n🕒 𝗧𝗶𝗺𝗲: {info['time']}\n📌 𝗦𝘁𝗮𝘁𝘂𝘀: {info['status']}\n━━━━━━━━━━━━━━━━━━\n"

        ticket_markup = InlineKeyboardMarkup()
        ticket_markup.add(InlineKeyboardButton("🔙 BACK TO SUPPORT", callback_data="btn_support"))
        bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=text, parse_mode="Markdown", reply_markup=ticket_markup)

    elif data == "btn_history":
        user_history = user_purchase_history.get(user_id, [])
        if not user_history:
            history_text = "🔑 𝗣𝗨𝗥𝗖𝗛𝗔𝗦𝗘 𝗛𝗜𝗦𝗧𝗢𝗥𝗬\n\n𝗬𝗼𝘂 𝗵𝗮𝘃𝗲𝗻'𝘁 𝗺𝗮𝗱𝗲 𝗮𝗻𝘆 𝗽𝘂𝗿𝗰𝗵𝗮𝘀𝗲𝘀 𝘆𝗲𝘁. 𝗬𝗼𝘂𝗿 𝘃𝗮𝘂𝗹𝘁 𝗶𝘀 𝗲𝗺𝗽𝘁𝘆."
        else:
            history_text = "🔑 𝗬𝗢𝗨𝗥 𝗣𝗨𝗥𝗖𝗛𝗔𝗦𝗘 𝗛𝗜𝗦𝗧𝗢𝗥𝗬\n\n"
            for idx, item in enumerate(user_history, 1):
                history_text += f"{idx}. 📦 {item['app']} ({item['duration']}) - ₹{item['price']}\n   🕒 {item['time']}\n\n"
        bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=history_text, parse_mode="Markdown", reply_markup=back_markup)

    elif data == "btn_download":
        text = "📥 𝗗𝗢𝗪𝗡𝗟𝗢𝗔𝗗 𝗣𝗥𝗘𝗠𝗜𝗨𝗠 𝗔𝗣𝗞 & 𝗙𝗜𝗟𝗘𝗦\n\n🔒 𝗔𝗹𝗹 𝗼𝘂𝗿 𝗵𝗶𝗴𝗵𝗹𝘆 𝘀𝗲𝗰𝘂𝗿𝗲𝗱, 𝗽𝗿𝗲𝗺𝗶𝘂𝗺, 𝗮𝗻𝗱 𝘂𝗽𝗱𝗮𝘁𝗲𝗱 𝗳𝗶𝗹𝗲𝘀 𝗮𝗿𝗲 𝘀𝗲𝗰𝘂𝗿𝗲𝗹𝘆 𝗵𝗼𝘀𝘁𝗲𝗱 𝗼𝗻 𝗼𝘂𝗿 𝗽𝗿𝗶𝘃𝗮𝘁𝗲 𝗰𝗵𝗮𝗻𝗻𝗲𝗹!\n\n✨ 𝗪𝗛𝗔𝗧 𝗬𝗢𝗨 𝗚𝗘𝗧:\n• Latest APK Updates 🚀\n• 100% Virus Free & Secure 🛡️\n• All Configs & Scripts ⚙️\n• Complete Installation Guides 📖"
        download_markup = InlineKeyboardMarkup()
        download_markup.add(InlineKeyboardButton("📢 Access Download Channel", url="https://t.me/VickyXmodeofc"))
        download_markup.add(InlineKeyboardButton("🔙 BACK", callback_data="btn_back"))
        bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=text, parse_mode="Markdown", reply_markup=download_markup)

    elif data == "btn_balance":
        text = (
            "🎒 𝗔𝗗𝗗 𝗕𝗔𝗟𝗔𝗡𝗖𝗘 💭\n\n"
            "💭 𝗦𝗲𝗹𝗲𝗰𝘁 𝘆𝗼𝘂𝗿 𝗽𝗿𝗲𝗳𝗲𝗿𝗿𝗲𝗱 𝗽𝗮𝘆𝗺𝗲𝗻𝘁 𝗺𝗲𝘁𝗵𝗼𝗱. ✅\n\n"
            "├ 💳 𝗨𝗣𝗜 — Fast Indian payments 🛑\n"
            "├ 🪙 𝗕𝗶𝗻𝗮𝗻𝗰𝗲 — Crypto payments 💳\n"
            "└ 💸 𝗯𝗞𝗮𝘀𝗵 — Bangladesh Taka payments 🇧🇩\n\n"
            "🛡️ 𝗣𝗮𝘆𝗺𝗲𝗻𝘁𝘀 𝗮𝗿𝗲 𝘃𝗲𝗿𝗶𝗳𝗶𝗲𝗱 𝘀𝗲𝗰𝘂𝗿𝗲𝗹𝘆. ✅"
        )
        markup = InlineKeyboardMarkup()
        markup.row(
            InlineKeyboardButton("💳 Paytm UPI", callback_data="btn_paytm_upi"),
            InlineKeyboardButton("🪙 Binance Pay", callback_data="btn_binance_pay")
        )
        markup.add(InlineKeyboardButton("💰 bKash (taka)", callback_data="btn_bkash_pay"))
        markup.add(InlineKeyboardButton("🔙 BACK", callback_data="btn_back"))
        bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=text, parse_mode="Markdown", reply_markup=markup)

    elif data == "btn_paytm_upi":
        bal = user_balances.get(user_id, 0.24)
        text = f"💸 𝗔𝗱𝗱 𝗕𝗮𝗹𝗮𝗻𝗰𝗲 (𝗣𝗮𝘆𝘁𝗺 𝗨𝗣𝗜)\n\n𝗖𝘂𝗿𝗿𝗲𝗻𝘁 𝗯𝗮𝗹𝗮𝗻𝗰𝗲: ₹{bal:.2f}\n\n𝗣𝗶𝗰𝗸 𝗮 𝗾𝘂𝗶𝗰𝗸 𝗮𝗺𝗼𝘂𝗻𝘁 𝗯𝗲𝗹𝗼𝘄, 𝗼𝗿 𝗲𝗻𝘁𝗲𝗿 𝗮 𝗰𝘂𝘀𝘁𝗼𝗺 𝗮𝗺𝗼𝘂𝗻𝘁.\n𝗠𝗶𝗻: ₹𝟱𝟬.𝟬𝟬 · 𝗠𝗮𝘅: ₹𝟮,𝟬𝟬𝟬.𝟬𝟬"
        markup = InlineKeyboardMarkup()
        markup.row(InlineKeyboardButton("₹100", callback_data="pay_quick_100"), InlineKeyboardButton("₹500", callback_data="pay_quick_500"))
        markup.row(InlineKeyboardButton("₹1000", callback_data="pay_quick_1000"), InlineKeyboardButton("₹2000", callback_data="pay_quick_2000"))
        markup.add(InlineKeyboardButton("✏️ Custom Amount", callback_data="btn_custom_amount"))
        markup.add(InlineKeyboardButton("🖐 Back", callback_data="btn_balance"))
        bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=text, parse_mode="Markdown", reply_markup=markup)

    elif data == "btn_binance_pay":
        text = (
            f"🪙 𝗕𝗜𝗡𝗔𝗡𝗖𝗘 𝗣𝗔𝗬 𝗦𝗬𝗦𝗧𝗘𝗠 (𝗨𝗦𝗗𝗧) 🪙\n\n"
            f"𝗦𝗲𝗻𝗱 𝗨𝗦𝗗𝗧 / 𝗖𝗿𝘆𝗽𝘁𝗼 𝘃𝗶𝗮 𝗕𝗶𝗻𝗮𝗻𝗰𝗲 𝗣𝗮𝘆 𝗜𝗗:\n\n"
            f"🆔 𝗕𝗶𝗻𝗮𝗻𝗰𝗲 𝗣𝗮𝘆 𝗜𝗗: `{BINANCE_PAY_ID}`\n\n"
            f"📌 𝗜𝗻𝘀𝘁𝗿𝘂𝗰𝘁𝗶𝗼𝗻𝘀:\n"
            f"1. Open Binance App -> Pay Section\n"
            f"2. Send desired USDT amount.\n"
            f"3. Send screenshot & Transaction ID to Admin 👉 @{clean_admin}\n\n"
            f"💡 𝗡𝗼𝘁𝗲: Payment auto-converted & directly credited to UPI: `{DEFAULT_UPI_ID}`"
        )
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("💬 Send Proof to Admin", url=f"https://t.me/{clean_admin}"))
        markup.add(InlineKeyboardButton("🖐 Back", callback_data="btn_balance"))
        bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=text, parse_mode="Markdown", reply_markup=markup)

    elif data == "btn_bkash_pay":
        text = (
            f"💰 𝗯𝗞𝗔𝗦𝗛 𝗣𝗔𝗬𝗠𝗘𝗡𝗧 (𝗕𝗔𝗡𝗚𝗟𝗔𝗗𝗘𝗦𝗛) 🇧🇩\n\n"
            f"𝗦𝗲𝗻𝗱 𝗧𝗮𝗸𝗮 𝘁𝗼 𝗼𝘂𝗿 𝗯𝗞𝗮𝘀𝗵 𝗔𝗴𝗲𝗻𝘁/𝗣𝗲𝗿𝘀𝗼𝗻𝗮𝗹 𝗻𝘂𝗺𝗯𝗲𝗿:\n\n"
            f"📱 𝗯𝗞𝗮𝘀𝗵 𝗣𝗲𝗿𝘀𝗼𝗻𝗮𝗹 𝗡𝘂𝗺𝗯𝗲𝗿: `{BKASH_NUMBER}`\n\n"
            f"📌 𝗜𝗻𝘀𝘁𝗿𝘂𝗰𝘁𝗶𝗼𝗻𝘀:\n"
            f"1. Use 'Send Money' option.\n"
            f"2. Send screenshot & TrxID to Admin 👉 @{clean_admin}\n\n"
            f"💡 𝗡𝗼𝘁𝗲: BD Taka auto-converted & credited to UPI: `{DEFAULT_UPI_ID}`"
        )
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("💬 Send Proof to Admin", url=f"https://t.me/{clean_admin}"))
        markup.add(InlineKeyboardButton("🖐 Back", callback_data="btn_balance"))
        bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=text, parse_mode="Markdown", reply_markup=markup)

    elif data == "btn_custom_amount":
        user_amount_input[user_id] = "0"
        text = "💰 𝗘𝗻𝘁𝗲𝗿 𝗔𝗺𝗼𝘂𝗻𝘁\n\n₹0\n\n𝗠𝗶𝗻: ₹𝟱𝟬.𝟬𝟬 · 𝗠𝗮𝘅: ₹𝟮,𝟬𝟬𝟬.𝟬𝟬"
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
        text = f"💰 𝗘𝗻𝘁𝗲𝗿 𝗔𝗺𝗼𝘂𝗻𝘁\n\n₹{val}\n\n𝗠𝗶𝗻: ₹𝟱𝟬.𝟬𝟬 · 𝗠𝗮𝘅: ₹𝟮,𝟬𝟬𝟬.𝟬𝟬"
        bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=text, parse_mode="Markdown", reply_markup=create_keypad_markup(val))

    elif data == "confirm_custom_pay" or data.startswith("pay_quick_"):
        amount = int(data.replace("pay_quick_", "")) if data.startswith("pay_quick_") else int(user_amount_input.get(user_id, "0"))
        if amount < 50 or amount > 2000:
            bot.answer_callback_query(call.id, "⚠️ Amount Min ₹50 ke beech honi chahiye!", show_alert=True)
            return

        qr_url = f"https://api.qrserver.com/v1/create-qr-code/?size=300x300&data=upi://pay?pa={DEFAULT_UPI_ID}%26pn=Vicky%20Store%26am={amount}"
        text = f"💰 𝗣𝗔𝗬𝗠𝗘𝗡𝗧 𝗗𝗘𝗧𝗔𝗜𝗟𝗦\n\n𝗦𝗲𝗹𝗲𝗰𝘁𝗲𝗱 𝗔𝗺𝗼𝘂𝗻𝘁: ₹{amount}\n\n💳 𝗨𝗣𝗜 𝗜𝗗: `{DEFAULT_UPI_ID}`\n\n𝗤𝗥 𝗦𝗰𝗮𝗻 𝗸𝗮𝗿𝗸𝗲 𝗽𝗮𝘆 𝗸𝗮𝗿𝗲𝗶𝗻 𝗮𝘂𝗿 𝘀𝗰𝗿𝗲𝗲𝗻𝘀𝗵𝗼𝘁 𝘆𝗮𝗵𝗮 𝗯𝗵𝗲𝗷𝗲 👉 @{clean_admin}"
        bot.delete_message(chat_id=chat_id, message_id=message_id)
        bot.send_photo(chat_id=chat_id, photo=qr_url, caption=text, parse_mode="Markdown", reply_markup=back_markup)

    elif data == "btn_referral":
        bot_username = bot.get_me().username
        ref_link = f"https://t.me/{bot_username}?start={user_id}"
        text = f"👥 𝗔𝗙𝗙𝗜𝗟𝗜𝗔𝗧𝗘 𝗣𝗥𝗢𝗚𝗥𝗔𝗠\n\n✅ 𝗦𝘁𝗮𝘁𝘂𝘀: ACTIVE\n🏆 𝗘𝗮𝗿𝗻 𝟭𝟱% 𝗰𝗼𝗺𝗺𝗶𝘀𝘀𝗶𝗼𝗻 𝗼𝗻 𝗲𝘃𝗲𝗿𝘆 𝘀𝘂𝗰𝗰𝗲𝘀𝘀𝗳𝘂𝗹 𝗽𝘂𝗿𝗰𝗵𝗮𝘀𝗲 𝗺𝗮𝗱𝗲 𝗯𝘆 𝘆𝗼𝘂𝗿 𝗿𝗲𝗳𝗲𝗿𝗿𝗲𝗱 𝗳𝗿𝗶𝗲𝗻𝗱𝘀!\n\n👥 𝗧𝗼𝘁𝗮𝗹 𝗥𝗲𝗳𝗲𝗿𝗿𝗲𝗱: 0\n💰 𝗧𝗼𝘁𝗮𝗹 𝗘𝗮𝗿𝗻𝗲𝗱: ₹0.00 (~ $0.00)\n\n🔗 𝗬𝗼𝘂𝗿 𝗜𝗻𝘃𝗶𝘁𝗲 𝗟𝗶𝗻𝗸:\n`{ref_link}`"
        bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=text, parse_mode="Markdown", reply_markup=back_markup)

    elif data == "btn_ludo":
        text = "🎁 𝗟𝗨𝗗𝗢 𝗦𝗣𝗜𝗡 & 𝗪𝗜𝗡\n\nचक्र घुमाएं और पुरस्कार जीतें!\n⏳ 𝗡𝗶𝘆𝗮𝗺: आप इसे 24 घंटे में सिर्फ 1 बार घुमा सकते हैं।"
        spin_markup = InlineKeyboardMarkup()
        spin_markup.add(InlineKeyboardButton("🎲 Spin Dice Now", callback_data="btn_dospin"))
        spin_markup.add(InlineKeyboardButton("🔙 BACK", callback_data="btn_back"))
        bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=text, parse_mode="Markdown", reply_markup=spin_markup)

    elif data == "btn_dospin":
        current_time = time.time()
        cooldown_period = 86400

        if str_user_id in user_last_spin:
            elapsed_time = current_time - user_last_spin[str_user_id]
            if elapsed_time < cooldown_period:
                bot.delete_message(chat_id=chat_id, message_id=message_id)
                cooldown_text = "❌ 𝗖𝗼𝗼𝗹𝗱𝗼𝘄𝗻 𝗔𝗰𝘁𝗶𝘃𝗲!\n𝗬𝗼𝘂 𝗮𝗹𝗿𝗲𝗮𝗱𝘆 𝗽𝗹𝗮𝘆𝗲𝗱 𝘁𝗼𝗱𝗮𝘆. 𝗖𝗼𝗺𝗲 𝗯𝗮𝗰𝗸 𝘁𝗼𝗺𝗼𝗿𝗿𝗼𝘄."
                back_markup_ludo = InlineKeyboardMarkup()
                back_markup_ludo.add(InlineKeyboardButton("↩️ BACK", callback_data="btn_ludo"))
                bot.send_message(chat_id=chat_id, text=cooldown_text, parse_mode="Markdown", reply_markup=back_markup_ludo)
                return

        user_last_spin[str_user_id] = current_time
        save_json_data(SPIN_FILE, user_last_spin)

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
            f"🎁 𝗟𝗨𝗖𝗞𝗬 𝗗𝗜𝗖𝗘 𝗥𝗘𝗦𝗨𝗟𝗧 🔨💯\n\n"
            f"🎲 𝗗𝗶𝗰𝗲 𝗩𝗮𝗹𝘂𝗲: {dice_value}\n\n"
            f"💸 𝗬𝗼𝘂 𝗪𝗼𝗻: ₹{won_amount:.2f} (~ ${usd_won:.2f})\n"
            f"💰 𝗧𝗼𝘁𝗮𝗹 𝗕𝗮𝗹𝗮𝗻𝗰𝗲: ₹{new_balance:.2f} (~ ${usd_total:.2f})\n\n"
            f"𝗖𝗼𝗻𝗴𝗿𝗮𝘁𝘂𝗹𝗮𝘁𝗶𝗼𝗻𝘀! 𝗖𝗼𝗺𝗲 𝗯𝗮𝗰𝗸 𝗮𝗳𝘁𝗲𝗿 𝟮𝟰 𝗵𝗼𝘂𝗿𝘀."
        )

        spin_markup = InlineKeyboardMarkup()
        spin_markup.add(InlineKeyboardButton("📚 BACK TO MENU", callback_data="btn_back"))
        bot.send_message(chat_id=chat_id, text=spin_text, parse_mode="Markdown", reply_to_message_id=dice_msg.message_id, reply_markup=spin_markup)

    elif data == "pnl_nonroot":
        text = "🛒 𝗔𝗡𝗗𝗥𝗢𝗜𝗗 𝗡𝗢𝗡 𝗥𝗢𝗢𝗧 𝗣𝗔𝗡𝗘𝗟𝗦\n\n✅ Choose an app:"
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("💧 Drip Client Apk", callback_data="app_drip"))
        markup.add(InlineKeyboardButton("🌐 Drip Client Proxy Apk", callback_data="app_drip_proxy"))
        markup.add(InlineKeyboardButton("👾 Hg Cheats Apk", callback_data="app_hg_cheats_nr"))
        markup.add(InlineKeyboardButton("👑 Prime Hook Apk", callback_data="app_prime"))
        markup.add(InlineKeyboardButton("🛡️ Hg Proxy Apk", callback_data="app_hg_proxy"))
        markup.add(InlineKeyboardButton("🍊 Patoteam Orange", callback_data="app_patorange"))
        markup.add(InlineKeyboardButton("🔵 Patoteam Blue", callback_data="app_patblue"))
        markup.add(InlineKeyboardButton("🔥 Br Mods Non Root", callback_data="app_brmods_nr"))
        markup.add(InlineKeyboardButton("☠️ Reaper xPro Apk", callback_data="app_reaper_nr"))
        markup.add(InlineKeyboardButton("🤫 Silent Cheats Apkmod", callback_data="app_silent_nr"))
        markup.add(InlineKeyboardButton("💉 NineX Mod Injector", callback_data="app_ninex"))
        markup.add(InlineKeyboardButton("🔤 ABCD Panel", callback_data="app_abcd"))
        markup.add(InlineKeyboardButton("⚙️ Patoteam Regedit Orange", callback_data="app_pato_regedit"))
        markup.add(InlineKeyboardButton("🎯 AimHack Apk", callback_data="app_aimhack"))
        markup.add(InlineKeyboardButton("🔙 BACK TO PANELS", callback_data="btn_store"))
        bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=text, parse_mode="Markdown", reply_markup=markup)

    elif data == "pnl_root":
        text = "🛒 𝗔𝗡𝗗𝗥𝗢𝗜𝗗 𝗥𝗢𝗢𝗧 𝗣𝗔𝗡𝗘𝗟𝗦\n\n✅ Choose an app:"
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("🔓 Br Mods Apk", callback_data="app_brmods_root"))
        markup.add(InlineKeyboardButton("⚔️ Reaper x Pro", callback_data="app_reaper_root"))
        markup.add(InlineKeyboardButton("💦 Drip Client Root", callback_data="app_drip_root"))
        markup.add(InlineKeyboardButton("🎯 Hg Cheats Apk", callback_data="app_hg_root"))
        markup.add(InlineKeyboardButton("⚡ Stricks Br ~ Alpha", callback_data="app_stricks"))
        markup.add(InlineKeyboardButton("🧪 Xyz Cheats Apk", callback_data="app_xyz"))
        markup.add(InlineKeyboardButton("✨ Hikari Mod Apk", callback_data="app_hikari"))
        markup.add(InlineKeyboardButton("🛡️ Lk Team Apk", callback_data="app_lk"))
        markup.add(InlineKeyboardButton("🟢 Silent Cheats [Safe]", callback_data="app_safe"))
        markup.add(InlineKeyboardButton("🔴 Silent Cheats [Brutal]", callback_data="app_brutal"))
        markup.add(InlineKeyboardButton("⚙️ Xreg Safe Apk", callback_data="app_xreg"))
        markup.add(InlineKeyboardButton("🚀 Rapid Core Apk", callback_data="app_rapid"))
        markup.add(InlineKeyboardButton("☣️ Haxx-cker Pro", callback_data="app_haxx"))
        markup.add(InlineKeyboardButton("🤖 Zytron Pro Apk", callback_data="app_zytron"))
        markup.add(InlineKeyboardButton("😡 Angry Mod Apk", callback_data="app_angry"))
        markup.add(InlineKeyboardButton("🦂 Scorpio Mods [Lite]", callback_data="app_scorpio_lite"))
        markup.add(InlineKeyboardButton("🦂 Scorpio Mods [Brutal]", callback_data="app_scorpio_brutal"))
        markup.add(InlineKeyboardButton("🔙 BACK TO PANELS", callback_data="btn_store"))
        bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=text, parse_mode="Markdown", reply_markup=markup)

    elif data == "pnl_iphone":
        text = "🛒 𝗜𝗣𝗛𝗢𝗡𝗘 𝗣𝗔𝗡𝗘𝗟𝗦\n\n✅ Choose an app:"
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("📜 Gbox Certificate", callback_data="app_gbox"))
        markup.add(InlineKeyboardButton("🔑 Esing Certificate", callback_data="app_esing"))
        markup.add(InlineKeyboardButton("💎 Fluorite Ios", callback_data="app_fluorite"))
        markup.add(InlineKeyboardButton("🏆 Migul ~ Pro", callback_data="app_migul_pro"))
        markup.add(InlineKeyboardButton("🔰 Migul ~ Basic", callback_data="app_migul_basic"))
        # NAYA BUTTON ADDED
        markup.add(InlineKeyboardButton("🍎 AlphaRegedit External", callback_data="app_alpha_regedit"))
        markup.add(InlineKeyboardButton("🔙 BACK TO PANELS", callback_data="btn_store"))
        bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=text, parse_mode="Markdown", reply_markup=markup)

    elif data == "pnl_pc":
        text = "🛒 𝗣𝗖 𝗣𝗔𝗡𝗘𝗟𝗦\n\n✅ Choose an app:"
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("🖥️ Drip Client Pc", callback_data="app_drip_pc"))
        markup.add(InlineKeyboardButton("💻 Br Mods Pc", callback_data="app_brmods_pc"))
        # NAYA BUTTON ADDED
        markup.add(InlineKeyboardButton("🛒 Only Exe Aimkill", callback_data="app_only_exe"))
        markup.add(InlineKeyboardButton("🔙 BACK TO PANELS", callback_data="btn_store"))
        bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=text, parse_mode="Markdown", reply_markup=markup)

    elif data.startswith("app_"):
        app_code = data.replace("app_", "")
        filename = f"{app_code}_keys.txt"
        stock = get_stock_count(filename)
        stock_status = "📦 ✅ In Stock" if stock > 0 else "📦 ❌ Out of Stock"

        default_app = {"name": app_code.upper(), "emoji": "📱", 1: 80, 7: 300, 30: 700}
        app_data = APP_PRICES.get(app_code, default_app)
        app_title = app_data["name"]
        app_emoji = app_data.get("emoji", "📱")

        text = f"{app_emoji} 𝗣𝗔𝗡𝗘𝗟 - {app_title.upper()} 𝗣𝗔𝗖𝗞𝗔𝗚𝗘𝗦\n━━━━━━━━━━━━━━━━━━\n\n"
        for duration, price in app_data.items():
            if duration not in ["name", "emoji"]:
                usd_price = round(price / 90.0, 2)
                val_text = f"{duration} Days" if isinstance(duration, int) else f"{duration}"
                text += f"🛒 ⏱️ 𝗩𝗮𝗹𝗶𝗱𝗶𝘁𝘆: {val_text}\n💰 𝗣𝗿𝗶𝗰𝗲: ₹{price}.00 (~ ${usd_price})\n📱 𝗟𝗶𝗺𝗶𝘁: 1 Device | {stock_status}\n\n"
        text += "✅ 𝗦𝗲𝗹𝗲𝗰𝘁 𝗽𝗮𝗰𝗸𝗮𝗴𝗲 𝗯𝗲𝗹𝗼𝘄 𝘁𝗼 𝗶𝗻𝘀𝘁𝗮𝗻𝘁𝗹𝘆 𝗽𝘂𝗿𝗰𝗵𝗮𝘀𝗲:"

        markup = InlineKeyboardMarkup()
        for duration, price in app_data.items():
            if duration not in ["name", "emoji"]:
                usd_price = round(price / 90.0, 2)
                val_text = f"{duration} Days" if isinstance(duration, int) else f"{duration}"
                if stock > 0:
                    markup.add(InlineKeyboardButton(f"🛒 Buy {val_text} - ₹{price}.00 (~ ${usd_price})", callback_data=f"buy_{app_code}_{duration}"))
                else:
                    markup.add(InlineKeyboardButton(f"❌ {val_text} (Out of Stock)", callback_data=f"oos_{app_code}_{duration}"))

        back_btn = "btn_store"
        if app_code in ["vala_mod", "drip", "drip_proxy", "hg_cheats_nr", "prime", "hg_proxy", "patorange", "patblue", "brmods_nr", "reaper_nr", "silent_nr", "ninex", "abcd", "pato_regedit", "aimhack"]:
            back_btn = "pnl_nonroot"
        elif app_code in ["brmods_root", "reaper_root", "drip_root", "hg_root", "stricks", "xyz", "hikari", "lk", "safe", "brutal", "xreg", "rapid", "haxx", "zytron", "angry", "scorpio_lite", "scorpio_brutal"]:
            back_btn = "pnl_root"
        elif app_code in ["gbox", "esing", "fluorite", "migul_pro", "migul_basic", "alpha_regedit"]:
            back_btn = "pnl_iphone"
        elif app_code in ["drip_pc", "brmods_pc", "only_exe"]:
            back_btn = "pnl_pc"

        markup.add(InlineKeyboardButton("🔙 BACK TO PANELS", callback_data=back_btn))
        bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=text, parse_mode="Markdown", reply_markup=markup)

    elif data.startswith("buy_"):
        parts = data.split("_")
        duration_selected = parts[-1]
        app_code_selected = "_".join(parts[1:-1])

        if str_user_id not in buyer_users:
            buyer_users.add(str_user_id)
            save_json_data(BUYERS_FILE, list(buyer_users))

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
 
