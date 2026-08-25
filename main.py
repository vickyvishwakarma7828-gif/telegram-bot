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
    markup.add(InlineKeyboardButton(f"✅ Confirm ₹{current_val}", callback_data="confirm_custom_pay"))
    markup.add(InlineKeyboardButton("🖐 Back", callback_data="btn_paytm_upi"))
    return markup

@bot.message_handler(commands=['start'])
def send_welcome(message):
    text = """✨ <b>WELCOME TO THE STORE</b>

🛒 <b>Product Store</b> : <b>all key purchase & instantly delivery</b>
👤 <b>My Profile</b> : <b>check your account information</b>
💰 <b>Add Balance</b> : <b>deposit balance & secure service</b>
🔑 <b>All History</b> : <b>check all key purchase history</b>
👥 <b>Referral</b> : <b>invite friends & earn rewards</b>
🌐 <b>Support</b> : <b>bot problem fixed for support admin</b>
🎁 <b>Ludo Spin</b> : <b>play game and win balance</b>
📥 <b>Download Files</b> : <b>download latest apk for safety.</b>"""

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

    bot.send_message(message.chat.id, text, reply_markup=markup, parse_mode="HTML")

@bot.callback_query_handler(func=lambda call: True)
def callback_listener(call):
    chat_id = call.message.chat.id
    user_id = call.from_user.id
    msg_id = call.message.message_id

    if call.data == "back_to_main":
        send_welcome(call.message)
        return

    # PRODUCT STORE
    if call.data == "btn_store":
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("🤖 NON ROOT MOD APK", callback_data="cat_nonroot"))
        markup.add(InlineKeyboardButton("⚡ ROOT MOD APK", callback_data="cat_root"))
        markup.add(InlineKeyboardButton("🍏 IOS CERTIFICATE / MOD", callback_data="cat_ios"))
        markup.add(InlineKeyboardButton("🖥 PC MODS", callback_data="cat_pc"))
        markup.add(InlineKeyboardButton("🖐 Back", callback_data="back_to_main"))
        bot.edit_message_text("🛒 <b>SELECT A CATEGORY BELOW:</b>", chat_id=chat_id, message_id=msg_id, reply_markup=markup, parse_mode="HTML")

    elif call.data == "cat_nonroot":
        markup = InlineKeyboardMarkup()
        apps = ["vala_mod", "drip", "drip_proxy", "prime", "hg_proxy", "patorange", "patblue", "brmods_nr", "reaper_nr", "silent_nr"]
        for app in apps:
            markup.add(InlineKeyboardButton(f"• {APP_PRICES[app]['name']}", callback_data=f"app_{app}"))
        markup.add(InlineKeyboardButton("🖐 Back", callback_data="btn_store"))
        bot.edit_message_text("🤖 <b>SELECT A NON ROOT MOD:</b>", chat_id=chat_id, message_id=msg_id, reply_markup=markup, parse_mode="HTML")

    elif call.data == "cat_root":
        markup = InlineKeyboardMarkup()
        apps = ["brmods_root", "reaper_root", "drip_root", "hg_root", "stricks", "xyz", "hikari", "lk", "safe", "brutal", "xreg", "rapid", "haxx", "zytron", "angry", "scorpio_lite", "scorpio_brutal"]
        for app in apps:
            markup.add(InlineKeyboardButton(f"• {APP_PRICES[app]['name']}", callback_data=f"app_{app}"))
        markup.add(InlineKeyboardButton("🖐 Back", callback_data="btn_store"))
        bot.edit_message_text("⚡ <b>SELECT A ROOT MOD:</b>", chat_id=chat_id, message_id=msg_id, reply_markup=markup, parse_mode="HTML")

    elif call.data == "cat_ios":
        markup = InlineKeyboardMarkup()
        apps = ["gbox", "esing", "fluorite", "migul_pro", "migul_basic"]
        for app in apps:
            markup.add(InlineKeyboardButton(f"• {APP_PRICES[app]['name']}", callback_data=f"app_{app}"))
        markup.add(InlineKeyboardButton("🖐 Back", callback_data="btn_store"))
        bot.edit_message_text("🍏 <b>SELECT AN IOS MOD / CERTIFICATE:</b>", chat_id=chat_id, message_id=msg_id, reply_markup=markup, parse_mode="HTML")

    elif call.data == "cat_pc":
        markup = InlineKeyboardMarkup()
        apps = ["drip_pc", "brmods_pc"]
        for app in apps:
            markup.add(InlineKeyboardButton(f"• {APP_PRICES[app]['name']}", callback_data=f"app_{app}"))
        markup.add(InlineKeyboardButton("🖐 Back", callback_data="btn_store"))
        bot.edit_message_text("🖥 <b>SELECT A PC MOD:</b>", chat_id=chat_id, message_id=msg_id, reply_markup=markup, parse_mode="HTML")

    elif call.data.startswith("app_"):
        app_id = call.data.replace("app_", "")
        data = APP_PRICES.get(app_id)
        if data:
            markup = InlineKeyboardMarkup()
            for key, val in data.items():
                if key != "name":
                    stock = get_stock_count(f"{app_id}_{key}.txt")
                    markup.add(InlineKeyboardButton(f"{key} Day - ₹{val} (Stock: {stock})", callback_data=f"buy_{app_id}_{key}"))
            markup.add(InlineKeyboardButton("🖐 Back", callback_data="btn_store"))
            bot.edit_message_text(f"🛍 <b>{data['name']} Options:</b>", chat_id=chat_id, message_id=msg_id, reply_markup=markup, parse_mode="HTML")

    elif call.data.startswith("buy_"):
        parts = call.data.split("_")
        app_id = parts[1]
        duration = parts[2]
        price = APP_PRICES[app_id][duration if duration.isdigit() else str(duration)]
        
        balance = user_balances.get(user_id, 0)
        if balance < price:
            bot.answer_callback_query(call.id, f"Insufficient Balance! You need ₹{price}.", show_alert=True)
            return

        filename = f"{app_id}_{duration}.txt"
        if not os.path.exists(filename) or get_stock_count(filename) == 0:
            bot.answer_callback_query(call.id, "Sorry, this item is out of stock!", show_alert=True)
            return

        with open(filename, "r", encoding="utf-8") as f:
            keys = f.readlines()
        
        assigned_key = keys[0].strip()
        remaining_keys = keys[1:]

        with open(filename, "w", encoding="utf-8") as f:
            f.writelines(remaining_keys)

        user_balances[user_id] -= price

        if user_id not in user_purchase_history:
            user_purchase_history[user_id] = []
        
        purchased_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        user_purchase_history[user_id].append({
            "item": APP_PRICES[app_id]['name'],
            "duration": duration,
            "key": assigned_key,
            "date": purchased_time
        })

        msg = f"🎉 <b>PURCHASE SUCCESSFUL!</b>\n\n📌 <b>Item:</b> {APP_PRICES[app_id]['name']}\n⏳ <b>Duration:</b> {duration}\n🔑 <b>Key:</b> <code>{assigned_key}</code>\n\nThank you for purchasing!"
        bot.send_message(chat_id, msg, parse_mode="HTML")

    # ADD BALANCE
    elif call.data == "btn_balance":
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("💳 PAYTM / PhonePe / GPay (UPI)", callback_data="btn_paytm_upi"))
        markup.add(InlineKeyboardButton("🟡 Binance Pay (USDT)", callback_data="btn_binance"))
        markup.add(InlineKeyboardButton("🔴 bKash (Bangladesh)", callback_data="btn_bkash"))
        markup.add(InlineKeyboardButton("🖐 Back", callback_data="back_to_main"))
        bot.edit_message_text("💰 <b>SELECT PAYMENT METHOD:</b>", chat_id=chat_id, message_id=msg_id, reply_markup=markup, parse_mode="HTML")

    elif call.data == "btn_paytm_upi":
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("₹50", callback_data="custom_pay_50"), InlineKeyboardButton("₹100", callback_data="custom_pay_100"))
        markup.add(InlineKeyboardButton("₹200", callback_data="custom_pay_200"), InlineKeyboardButton("₹500", callback_data="custom_pay_500"))
        markup.add(InlineKeyboardButton("⌨ Enter Custom Amount", callback_data="custom_pay_keypad"))
        markup.add(InlineKeyboardButton("🖐 Back", callback_data="btn_balance"))
        bot.edit_message_text("💵 <b>Select or Enter Amount:</b>", chat_id=chat_id, message_id=msg_id, reply_markup=markup, parse_mode="HTML")

    elif call.data.startswith("custom_pay_"):
        val = call.data.replace("custom_pay_", "")
        if val == "keypad":
            user_amount_input[user_id] = "0"
            markup = create_keypad_markup("0")
            bot.edit_message_text("⌨ <b>Enter custom amount (INR):</b>\n\nAmount: ₹0", chat_id=chat_id, message_id=msg_id, reply_markup=markup, parse_mode="HTML")
        else:
            user_amount_input[user_id] = val
            amount = val
            qr_url = f"https://api.qrserver.com/v1/create-qr-code/?size=300x300&data=upi://pay?pa={DEFAULT_UPI_ID}%26pn=Store%26am={amount}%26cu=INR"
            text = f"📲 <b>UPI PAYMENT</b>\n\n<b>UPI ID:</b> <code>{DEFAULT_UPI_ID}</code>\n<b>Amount:</b> ₹{amount}\n\nPay using the QR or UPI ID, then contact admin with screenshot to add balance."
            bot.send_photo(chat_id, qr_url, caption=text, parse_mode="HTML")

    elif call.data.startswith("num_"):
        action = call.data.replace("num_", "")
        curr = user_amount_input.get(user_id, "0")
        
        if action.isdigit():
            if curr == "0":
                curr = action
            else:
                curr += action
        elif action == "clear":
            curr = "0"
        elif action == "backspace":
            curr = curr[:-1]
            if not curr:
                curr = "0"
        
        user_amount_input[user_id] = curr
        markup = create_keypad_markup(curr)
        bot.edit_message_text(f"⌨ <b>Enter custom amount (INR):</b>\n\nAmount: ₹{curr}", chat_id=chat_id, message_id=msg_id, reply_markup=markup, parse_mode="HTML")

    elif call.data == "confirm_custom_pay":
        amount = user_amount_input.get(user_id, "0")
        if amount == "0":
            bot.answer_callback_query(call.id, "Please enter an amount greater than 0!", show_alert=True)
            return
        qr_url = f"https://api.qrserver.com/v1/create-qr-code/?size=300x300&data=upi://pay?pa={DEFAULT_UPI_ID}%26pn=Store%26am={amount}%26cu=INR"
        text = f"📲 <b>UPI PAYMENT</b>\n\n<b>UPI ID:</b> <code>{DEFAULT_UPI_ID}</code>\n<b>Amount:</b> ₹{amount}\n\nPay using the QR or UPI ID, then contact admin with screenshot to add balance."
        bot.send_photo(chat_id, qr_url, caption=text, parse_mode="HTML")

    elif call.data == "btn_binance":
        text = f"🟡 <b>BINANCE PAY</b>\n\n<b>Binance Pay ID:</b> <code>{BINANCE_PAY_ID}</code>\n\nSend USDT and contact Admin with Payment Proof."
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("🖐 Back", callback_data="btn_balance"))
        bot.edit_message_text(text, chat_id=chat_id, message_id=msg_id, reply_markup=markup, parse_mode="HTML")

    elif call.data == "btn_bkash":
        text = f"🔴 <b>BKASH PAYMENT</b>\n\n<b>bKash Personal Number:</b> <code>{BKASH_NUMBER}</code>\n\nSend money and contact Admin with Transaction ID."
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("🖐 Back", callback_data="btn_balance"))
        bot.edit_message_text(text, chat_id=chat_id, message_id=msg_id, reply_markup=markup, parse_mode="HTML")

    # MY PROFILE
    elif call.data == "btn_profile":
        bal = user_balances.get(user_id, 0)
        text = f"👤 <b>ACCOUNT INFORMATION</b>\n\n🆔 <b>User ID:</b> <code>{user_id}</code>\n👤 <b>Name:</b> {call.from_user.first_name}\n💰 <b>Balance:</b> ₹{bal}"
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("🖐 Back", callback_data="back_to_main"))
        bot.edit_message_text(text, chat_id=chat_id, message_id=msg_id, reply_markup=markup, parse_mode="HTML")

    # ALL HISTORY
    elif call.data == "btn_history":
        history = user_purchase_history.get(user_id, [])
        if not history:
            text = "🔑 <b>PURCHASE HISTORY</b>\n\nNo purchases found."
        else:
            text = "🔑 <b>YOUR PURCHASE HISTORY:</b>\n\n"
            for idx, item in enumerate(history, 1):
                text += f"{idx}. <b>{item['item']}</b> ({item['duration']})\n   Key: <code>{item['key']}</code>\n   Date: {item['date']}\n\n"
        
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("🖐 Back", callback_data="back_to_main"))
        bot.edit_message_text(text, chat_id=chat_id, message_id=msg_id, reply_markup=markup, parse_mode="HTML")

    # REFERRAL
    elif call.data == "btn_referral":
        bot_username = bot.get_me().username
        ref_link = f"https://t.me/{bot_username}?start={user_id}"
        text = f"👥 <b>REFERRAL SYSTEM</b>\n\nShare your referral link with friends and earn rewards when they join!\n\n🔗 <b>Your Link:</b>\n<code>{ref_link}</code>"
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("🖐 Back", callback_data="back_to_main"))
        bot.edit_message_text(text, chat_id=chat_id, message_id=msg_id, reply_markup=markup, parse_mode="HTML")

    # SUPPORT
    elif call.data == "btn_support":
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("💬 Telegram Admin", url=f"https://t.me/{ADMIN_TELEGRAM_USERNAME}"))
        markup.add(InlineKeyboardButton("📱 WhatsApp Support", url=f"https://wa.me/{ADMIN_WHATSAPP_NUM}"))
        markup.add(InlineKeyboardButton("📩 Open Support Ticket", callback_data="create_ticket"))
        markup.add(InlineKeyboardButton("🖐 Back", callback_data="back_to_main"))
        bot.edit_message_text("🌐 <b>SUPPORT CENTER</b>\n\nChoose an option below to contact support:", chat_id=chat_id, message_id=msg_id, reply_markup=markup, parse_mode="HTML")

    elif call.data == "create_ticket":
        user_ticket_state[user_id] = True
        bot.send_message(chat_id, "📝 Please type your support message below. An admin will read it shortly.")

    # LUDO SPIN
    elif call.data == "btn_ludo":
        curr_time = time.time()
        last_time = user_last_spin.get(user_id, 0)
        
        if curr_time - last_time < 86400:
            rem = int(86400 - (curr_time - last_time))
            hours = rem // 3600
            mins = (rem % 3600) // 60
            bot.answer_callback_query(call.id, f"You can spin again in {hours}h {mins}m!", show_alert=True)
            return

        user_last_spin[user_id] = curr_time
        win_amount = random.choice([0, 5, 10, 15, 20, 50])
        user_balances[user_id] = user_balances.get(user_id, 0) + win_amount
        
        if win_amount > 0:
            msg = f"🎁 <b>CONGRATULATIONS!</b>\n\nYou won ₹{win_amount}! It has been added to your balance."
        else:
            msg = "🎰 <b>BETTER LUCK NEXT TIME!</b>\n\nYou got ₹0. Try again tomorrow!"

        bot.answer_callback_query(call.id, f"Spin Result: ₹{win_amount}", show_alert=True)
        
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("🖐 Back", callback_data="back_to_main"))
        bot.edit_message_text(msg, chat_id=chat_id, message_id=msg_id, reply_markup=markup, parse_mode="HTML")

    # DOWNLOAD FILES
    elif call.data == "btn_download":
        text = "📥 <b>DOWNLOAD LATEST APKS:</b>\n\n• Offical Store App: http://example.com/download"
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("🖐 Back", callback_data="back_to_main"))
        bot.edit_message_text(text, chat_id=chat_id, message_id=msg_id, reply_markup=markup, parse_mode="HTML")

@bot.message_handler(func=lambda m: user_ticket_state.get(m.from_user.id, False))
def handle_ticket_message(message):
    user_id = message.from_user.id
    user_ticket_state[user_id] = False
    
    ticket_id = random.randint(1000, 9999)
    support_tickets[ticket_id] = {"user_id": user_id, "msg": message.text}
    
    bot.reply_to(message, f"✅ <b>Ticket #{ticket_id} Created!</b> Support team will reach out soon.", parse_mode="HTML")

bot.polling(none_stop=True)
