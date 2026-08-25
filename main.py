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

# CONFIGURATIONS (Bina '@' ke username taaki link sahi kaam kare)
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
    markup.add(InlineKeyboardButton(f"✅ Confirm ₹{current_val}", callback_data="confirm_custom_pay"))
    markup.add(InlineKeyboardButton("🖐 Back", callback_data="btn_paytm_upi"))
    return markup

@bot.message_handler(commands=['start'])
def send_welcome(message):
    text = """✨ *WELCOME TO THE STORE*

🛒 Product Store : all key purchase & instantly delivery
👤 My Profile : check your account information
💰 Add Balance : deposit balance & secure service
🔑 All History : check all key purchase history
👥 Referral : invite friends & earn rewards
🌐 Support : bot problem fixed for support admin
🎁 Ludo Spin : play game and win balance
📥 Download Files : download latest apk for safety."""

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
    back_markup.add(InlineKeyboardButton("🔙 Back to Support", callback_data="btn_support"))
    success_msg = (
        f"✅ *TICKET CREATED SUCCESSFULLY!*\n\n"
        f"🎫 **Ticket ID:** `{ticket_id}`\n"
        f"📝 **Issue:** {message.text}\n"
        f"🕒 **Time:** {created_time}\n"
        f"📌 **Status:** OPEN 🟡\n\n"
        f"Our support team will contact you shortly!"
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
    back_markup.add(InlineKeyboardButton("🔙 BACK", callback_data="btn_back"))

    if data == "btn_back":
        bot.delete_message(chat_id=chat_id, message_id=message_id)
        send_welcome(call.message)

    elif data == "btn_store":
        text = "🛒 *SELECT PRODUCT PANEL*\n\n✅ Choose a panel to view its packages:"
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("🤖 ANDROID NON ROOT PANEL", callback_data="pnl_nonroot"))
        markup.add(InlineKeyboardButton("🤖 ANDROID ROOT PANEL", callback_data="pnl_root"))
        markup.add(InlineKeyboardButton("🍎 IPHONE PANEL", callback_data="pnl_iphone"))
        markup.add(InlineKeyboardButton("💻 PC PANEL", callback_data="pnl_pc"))
        markup.add(InlineKeyboardButton("🔙 BACK", callback_data="btn_back"))
        bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=text, parse_mode="Markdown", reply_markup=markup)

    elif data == "btn_profile":
        user_name = call.from_user.first_name
        join_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        bal = user_balances.get(user_id, 0.24)
        profile_text = (
            f"👤 **— YOUR SECURE PROFILE —** 👤\n\n"
            f"👤 Grid ID: `{user_id}`\n"
            f"👑 Name: {user_name}\n"
            f"👑 Account Level: 👤 Regular User\n\n"
            f"💰 **— Wallet —** 🪙\n"
            f"💰 Current Balance: ₹{bal:.2f} (~ ${(bal/90.0):.2f}) 🪙\n\n"
            f"📈 **— Global Statistics —**\n"
            f"🗂️ Total Orders: {len(user_purchase_history.get(user_id, []))}\n"
            f"💸 Total Spent: ₹0.00 (~ $0.00)\n"
            f"👥 Total Referrals: 0\n\n"
            f"📅 Joined Grid: {join_date}"
        )
        profile_markup = InlineKeyboardMarkup()
        profile_markup.add(InlineKeyboardButton("🎁 Redeem Promo Code", callback_data="btn_redeem"))
        profile_markup.add(InlineKeyboardButton("🔙 BACK", callback_data="btn_back"))
        bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=profile_text, parse_mode="Markdown", reply_markup=profile_markup)

    elif data == "btn_redeem":
        bot.answer_callback_query(call.id, "⚠️ आपके पास कोई वैलिड प्रोमो कोड नहीं है!", show_alert=True)

    elif data == "btn_support":
        text = (
            "🌐💬 — *PREMIUM SUPPORT CENTER* —\n\n"
            "Contact us via Telegram or WhatsApp for instant help, or open a support ticket for admin assistance."
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
        text = "🎫 *OPEN SUPPORT TICKET*\n\nKripya apni samasya (problem) niche type karke message karein.\n\n📌 *Example:* My balance is not added / Key not working."
        cancel_markup = InlineKeyboardMarkup()
        cancel_markup.add(InlineKeyboardButton("❌ Cancel", callback_data="btn_support"))
        bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=text, parse_mode="Markdown", reply_markup=cancel_markup)

    elif data == "ticket_view":
        user_tickets = [t_id for t_id, data in support_tickets.items() if data['user_id'] == user_id]
        if not user_tickets:
            text = "📋 *MY OPEN TICKETS*\n\nAapka koi bhi support ticket abhi active nahi hai."
        else:
            text = "📋 *MY TICKETS STATUS*\n\n"
            for t_id in user_tickets:
                info = support_tickets[t_id]
                text += f"🎫 **ID:** `{t_id}`\n📝 **Issue:** {info['issue']}\n🕒 **Time:** {info['time']}\n📌 **Status:** {info['status']}\n━━━━━━━━━━━━━━━━━━\n"

        ticket_markup = InlineKeyboardMarkup()
        ticket_markup.add(InlineKeyboardButton("🔙 BACK TO SUPPORT", callback_data="btn_support"))
        bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=text, parse_mode="Markdown", reply_markup=ticket_markup)

    elif data == "btn_history":
        user_history = user_purchase_history.get(user_id, [])
        if not user_history:
            history_text = "🔑 *PURCHASE HISTORY*\n\nYou haven't made any purchases yet. Your vault is empty."
        else:
            history_text = "🔑 *YOUR PURCHASE HISTORY*\n\n"
            for idx, item in enumerate(user_history, 1):
                history_text += f"{idx}. 📦 {item['app']} ({item['duration']}) - ₹{item['price']}\n   🕒 {item['time']}\n\n"
        bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=history_text, parse_mode="Markdown", reply_markup=back_markup)

    elif data == "btn_download":
        text = "📥 *DOWNLOAD PREMIUM APK & FILES*\n\n🔒 All our highly secured, premium, and updated files are securely hosted on our private channel!\n\n✨ *WHAT YOU GET:*\n• Latest APK Updates 🚀\n• 100% Virus Free & Secure 🛡️\n• All Configs & Scripts ⚙️\n• Complete Installation Guides 📖"
        download_markup = InlineKeyboardMarkup()
        download_markup.add(InlineKeyboardButton("📢 Access Download Channel", url="https://t.me/VickyXmodeofc"))
        download_markup.add(InlineKeyboardButton("🔙 BACK", callback_data="btn_back"))
        bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=text, parse_mode="Markdown", reply_markup=download_markup)

    elif data == "btn_balance":
        text = (
            "🎒 *ADD BALANCE* 💭\n\n"
            "💭 Select your preferred payment method. ✅\n\n"
            "├ 💳 **UPI** — Fast Indian payments 🛑\n"
            "└ 🪙 **Binance** — Crypto payments 🛑\n\n"
            "🛡️ Payments are verified securely. ✅"
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
        text = f"💸 *Add Balance (Paytm UPI)*\n\nCurrent balance: ₹{bal:.2f}\n\nPick a quick amount below, or enter a custom amount.\nMin: ₹50.00 · Max: ₹2,000.00"
        markup = InlineKeyboardMarkup()
        markup.row(InlineKeyboardButton("₹100", callback_data="pay_quick_100"), InlineKeyboardButton("₹500", callback_data="pay_quick_500"))
        markup.row(InlineKeyboardButton("₹1000", callback_data="pay_quick_1000"), InlineKeyboardButton("₹2000", callback_data="pay_quick_2000"))
        markup.add(InlineKeyboardButton("✏️ Custom Amount", callback_data="btn_custom_amount"))
        markup.add(InlineKeyboardButton("🖐 Back", callback_data="btn_balance"))
        bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=text, parse_mode="Markdown", reply_markup=markup)

    elif data == "btn_binance_pay":
        text = (
            f"🪙 *BINANCE PAY SYSTEM* 🪙\n\n"
            f"Send USDT / Crypto directly to our Binance Pay ID:\n\n"
            f"🆔 **Binance Pay ID:** `{BINANCE_PAY_ID}`\n\n"
            f"📌 *Instructions:*\n"
            f"1. Open Binance App -> Pay Section\n"
            f"2. Pay the desired USDT amount.\n"
            f"3. Send the payment screenshot & Transaction ID to Admin 👉 @{clean_admin}"
        )
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("💬 Send Proof to Admin", url=f"https://t.me/{clean_admin}"))
        markup.add(InlineKeyboardButton("🖐 Back", callback_data="btn_balance"))
        bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=text, parse_mode="Markdown", reply_markup=markup)

    elif data == "btn_bkash_pay":
        text = (
            f"💰 *bKASH PAYMENT (TAKA)* 🇧🇩\n\n"
            f"Bangladesh bKash personal payment detail:\n\n"
            f"📱 **bKash Personal Number:** `{BKASH_NUMBER}`\n\n"
            f"📌 *Instructions:*\n"
            f"1. Use Send Money option.\n"
            f"2. Send payment according to rate.\n"
            f"3. Send Transaction TrxID and Screenshot to Admin 👉 @{clean_admin}"
        )
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("💬 Send Proof to Admin", url=f"https://t.me/{clean_admin}"))
        markup.add(InlineKeyboardButton("🖐 Back", callback_data="btn_balance"))
        bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=text, parse_mode="Markdown", reply_markup=markup)

    elif data == "btn_custom_amount":
        user_amount_input[user_id] = "0"
        text = "💰 *Enter Amount*\n\n₹0\n\nMin: ₹50.00 · Max: ₹2,000.00"
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
        text = f"💰 *Enter Amount*\n\n₹{val}\n\nMin: ₹50.00 · Max: ₹2,000.00"
        bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=text, parse_mode="Markdown", reply_markup=create_keypad_markup(val))

    elif data == "confirm_custom_pay" or data.startswith("pay_quick_"):
        amount = int(data.replace("pay_quick_", "")) if data.startswith("pay_quick_") else int(user_amount_input.get(user_id, "0"))
        if amount < 50 or amount > 2000:
            bot.answer_callback_query(call.id, "⚠️ Amount Min ₹50 and Max ₹2,000 ke beech honi chahiye!", show_alert=True)
            return

        qr_url = f"https://api.qrserver.com/v1/create-qr-code/?size=300x300&data=upi://pay?pa={DEFAULT_UPI_ID}%26pn=Vicky%20Store%26am={amount}"
        text = f"💰 *PAYMENT DETAILS*\n\nSelected Amount: ₹{amount}\n\n💳 *UPI ID:* `{DEFAULT_UPI_ID}`\n\nQR Scan karke pay karein aur screenshot yaha bheje 👉 @{clean_admin}"
        bot.delete_message(chat_id=chat_id, message_id=message_id)
        bot.send_photo(chat_id=chat_id, photo=qr_url, caption=text, parse_mode="Markdown", reply_markup=back_markup)

    elif data == "btn_referral":
        bot_username = bot.get_me().username
        ref_link = f"https://t.me/{bot_username}?start={user_id}"
        text = f"👥 *AFFILIATE PROGRAM*\n\n✅ *Status:* ACTIVE\n🏆 Earn 15% commission on every successful purchase made by your referred friends!\n\n👥 Total Referred: 0\n💰 Total Earned: ₹0.00 (~ $0.00)\n\n🔗 *Your Invite Link:*\n`{ref_link}`"
        bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=text, parse_mode="Markdown", reply_markup=back_markup)

    elif data == "btn_ludo":
        text = "🎁 *LUDO SPIN & WIN*\n\nचक्र घुमाएं और पुरस्कार जीतें!\n⏳ *नियम:* आप इसे 24 घंटे में सिर्फ 1 बार घुमा सकते हैं।"
        spin_markup = InlineKeyboardMarkup()
        spin_markup.add(InlineKeyboardButton("🎲 Spin Dice Now", callback_data="btn_dospin"))
        spin_markup.add(InlineKeyboardButton("🔙 BACK", callback_data="btn_back"))
        bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=text, parse_mode="Markdown", reply_markup=spin_markup)

    elif data == "btn_dospin":
        current_time = time.time()
        cooldown_period = 86400

        if user_id in user_last_spin:
            elapsed_time = current_time - user_last_spin[user_id]
            if elapsed_time < cooldown_period:
                bot.answer_callback_query(call.id, "⏳ Cooldown Active!\nYou already played today. Come back tomorrow.", show_alert=True)
                return

        user_last_spin[user_id] = current_time

        # Pura message delete karke Telegram dice send karein
        bot.delete_message(chat_id=chat_id, message_id=message_id)
        dice_msg = bot.send_dice(chat_id=chat_id, emoji='🎲')
        dice_value = dice_msg.dice.value

        # Har dice number ka winning reward amount
        rewards = {1: 0.10, 2: 0.20, 3: 0.30, 4: 0.40, 5: 0.50, 6: 1.00}
        won_amount = rewards.get(dice_value, 0.10)

        # Balance update karna
        current_bal = user_balances.get(user_id, 0.24)
        new_balance = current_bal + won_amount
        user_balances[user_id] = new_balance

        # Dice roll animation ke liye 3 second wait
        time.sleep(3)

        # Output Text (Aapke screenshot format ke anusar)
        usd_won = won_amount / 90.0
        usd_total = new_balance / 90.0

        spin_text = (
            f"🎁 *LUCKY DICE RESULT* 🔨💯\n\n"
            f"🎲 **Dice Value:** {dice_value}\n\n"
            f"💸 **You Won:** ₹{won_amount:.2f} (~ ${usd_won:.2f})\n"
            f"💰 **Total Balance:** ₹{new_balance:.2f} (~ ${usd_total:.2f})\n\n"
            f"Congratulations! Come back after 24 hours."
        )

        spin_markup = InlineKeyboardMarkup()
        spin_markup.add(InlineKeyboardButton("📚 BACK TO MENU", callback_data="btn_back"))

        bot.send_message(
            chat_id=chat_id,
            text=spin_text,
            parse_mode="Markdown",
            reply_to_message_id=dice_msg.message_id,
            reply_markup=spin_markup
        )

    elif data == "pnl_nonroot":
        text = "🛒 *ANDROID NON ROOT PANELS*\n\n✅ Choose an app:"
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("💥 VALA MOD APK", callback_data="app_vala_mod"))
        markup.add(InlineKeyboardButton("📱 Drip Client Apk", callback_data="app_drip"))
        markup.add(InlineKeyboardButton("📱 Drip Client Proxy Apk", callback_data="app_drip_proxy"))
        markup.add(InlineKeyboardButton("📱 Prime Hook Apk", callback_data="app_prime"))
        markup.add(InlineKeyboardButton("📱 HG Proxy Apk", callback_data="app_hg_proxy"))
        markup.add(InlineKeyboardButton("📱 Patoteam Orange", callback_data="app_patorange"))
        markup.add(InlineKeyboardButton("📱 Patoteam Blue", callback_data="app_patblue"))
        markup.add(InlineKeyboardButton("📱 Br Mods Non Root", callback_data="app_brmods_nr"))
        markup.add(InlineKeyboardButton("📱 Reaper xPro Apk", callback_data="app_reaper_nr"))
        markup.add(InlineKeyboardButton("📱 Silent Cheats Apkmod", callback_data="app_silent_nr"))
        markup.add(InlineKeyboardButton("🔙 BACK TO PANELS", callback_data="btn_store"))
        bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=text, parse_mode="Markdown", reply_markup=markup)

    elif data == "pnl_root":
        text = "🛒 *ANDROID ROOT PANELS*\n\n✅ Choose an app:"
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("📱 Br Mods Apk", callback_data="app_brmods_root"))
        markup.add(InlineKeyboardButton("📱 Reaper x Pro", callback_data="app_reaper_root"))
        markup.add(InlineKeyboardButton("📱 Drip Client Root", callback_data="app_drip_root"))
        markup.add(InlineKeyboardButton("📱 Hg Cheats Apk", callback_data="app_hg_root"))
        markup.add(InlineKeyboardButton("📱 Stricks Br ~ Alpha", callback_data="app_stricks"))
        markup.add(InlineKeyboardButton("📱 Xyz Cheats Apk", callback_data="app_xyz"))
        markup.add(InlineKeyboardButton("📱 Hikari Mod Apk", callback_data="app_hikari"))
        markup.add(InlineKeyboardButton("📱 Lk Team Apk", callback_data="app_lk"))
        markup.add(InlineKeyboardButton("📱 Silent Cheats [Safe]", callback_data="app_safe"))
        markup.add(InlineKeyboardButton("📱 Silent Cheats [Brutal]", callback_data="app_brutal"))
        markup.add(InlineKeyboardButton("📱 Xreg Safe Apk", callback_data="app_xreg"))
        markup.add(InlineKeyboardButton("📱 Rapid Core Apk", callback_data="app_rapid"))
        markup.add(InlineKeyboardButton("📱 Haxx-cker Pro", callback_data="app_haxx"))
        markup.add(InlineKeyboardButton("📱 Zytron Pro Apk", callback_data="app_zytron"))
        markup.add(InlineKeyboardButton("📱 Angry Mod Apk", callback_data="app_angry"))
        markup.add(InlineKeyboardButton("📱 Scorpio Mods [Lite]", callback_data="app_scorpio_lite"))
        markup.add(InlineKeyboardButton("📱 Scorpio Mods [Brutal]", callback_data="app_scorpio_brutal"))
        markup.add(InlineKeyboardButton("🔙 BACK TO PANELS", callback_data="btn_store"))
        bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=text, parse_mode="Markdown", reply_markup=markup)

    elif data == "pnl_iphone":
        text = "🛒 *IPHONE PANELS*\n\n✅ Choose an app:"
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("🍏 Gbox Certificate", callback_data="app_gbox"))
        markup.add(InlineKeyboardButton("🍏 Esing Certificate", callback_data="app_esing"))
        markup.add(InlineKeyboardButton("🍏 Fluorite Ios", callback_data="app_fluorite"))
        markup.add(InlineKeyboardButton("🍏 Migul ~ Pro", callback_data="app_migul_pro"))
        markup.add(InlineKeyboardButton("🍏 Migul ~ Basic", callback_data="app_migul_basic"))
        markup.add(InlineKeyboardButton("🔙 BACK TO PANELS", callback_data="btn_store"))
        bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=text, parse_mode="Markdown", reply_markup=markup)

    elif data == "pnl_pc":
        text = "🛒 *PC PANELS*\n\n✅ Choose an app:"
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("💻 Drip Client Pc", callback_data="app_drip_pc"))
        markup.add(InlineKeyboardButton("💻 Br Mods Pc", callback_data="app_brmods_pc"))
        markup.add(InlineKeyboardButton("🔙 BACK TO PANELS", callback_data="btn_store"))
        bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=text, parse_mode="Markdown", reply_markup=markup)

    elif data.startswith("app_"):
        app_code = data.replace("app_", "")
        filename = f"{app_code}_keys.txt"
        stock = get_stock_count(filename)
        stock_status = "📦 ✅ In Stock" if stock > 0 else "📦 ❌ Out of Stock"

        default_app = {"name": app_code.upper(), 1: 80, 7: 300, 30: 700}
        app_data = APP_PRICES.get(app_code, default_app)
        app_title = app_data["name"]

        text = f"🛒 *PANEL - {app_title.upper()} PACKAGES*\n━━━━━━━━━━━━━━━━━━\n\n"
        for duration, price in app_data.items():
            if duration != "name":
                usd_price = round(price / 90.0, 2)
                val_text = f"{duration} Days" if isinstance(duration, int) else f"{duration}"
                text += f"🛒 ⏱️ **Validity: {val_text}**\n💰 Price: ₹{price}.00 (~ ${usd_price})\n📱 Limit: 1 Device | {stock_status}\n\n"
        text += "✅ *Select package below to instantly purchase:*"

        markup = InlineKeyboardMarkup()
        for duration, price in app_data.items():
            if duration != "name":
                usd_price = round(price / 90.0, 2)
                val_text = f"{duration} Days" if isinstance(duration, int) else f"{duration}"
                if stock > 0:
                    markup.add(InlineKeyboardButton(f"🛒 Buy {val_text} - ₹{price}.00 (~ ${usd_price})", callback_data=f"buy_{app_code}_{duration}"))
                else:
                    markup.add(InlineKeyboardButton(f"❌ {val_text} (Out of Stock)", callback_data=f"oos_{app_code}_{duration}"))

        back_btn = "btn_store"
        if app_code in ["vala_mod", "drip", "drip_proxy", "prime", "hg_proxy", "patorange", "patblue", "brmods_nr", "reaper_nr", "silent_nr"]:
            back_btn = "pnl_nonroot"
        elif app_code in ["brmods_root", "reaper_root", "drip_root", "hg_root", "stricks", "xyz", "hikari", "lk", "safe", "brutal", "xreg", "rapid", "haxx", "zytron", "angry", "scorpio_lite", "scorpio_brutal"]:
            back_btn = "pnl_root"
        elif app_code in ["gbox", "esing", "fluorite", "migul_pro", "migul_basic"]:
            back_btn = "pnl_iphone"
        elif app_code in ["drip_pc", "brmods_pc"]:
            back_btn = "pnl_pc"

        markup.add(InlineKeyboardButton("🔙 BACK TO PANELS", callback_data=back_btn))
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
