import telebot
import random
import time
import os
from datetime import datetime
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo

TOKEN = '8849298752:AAFKpZRS8gtzYBvm81OSx8jLB6uN9IV93Kw'
bot = telebot.TeleBot(TOKEN)

# आपकी GitHub Pages वाली Mini App का URL
WEB_APP_URL = "https://vickyvishwakarma7828-gif.github.io/store-app/"

user_last_spin = {}

# केवल Single Regular Price के साथ Updated Prices
APP_PRICES = {
    # 💥 VALA MOD PACKAGES
    "vala_mod": {
        "name": "VALA MOD APK", 
        "1 Hour": 60, 
        "3 Hours": 150, 
        "6 Hours": 220, 
        "12 Hours": 350, 
        "24 Hours": 550
    },
    
    # IMAGES DATA (REGULAR PRICES ONLY)
    "abcd": {
        "name": "ABCD Panel",
        "12 Hours": 49,
        "1 Days": 99,
        "3 Days": 149,
        "7 Days": 299
    },
    "ninex": {
        "name": "NineX Mod Injector",
        "10 Days": 420,
        "20 Days": 800,
        "30 Days": 1200
    },
    "aimhack": {
        "name": "AimHack Apk",
        "1 Hour": 35,
        "3 Hours": 70,
        "6 Hours": 110,
        "12 Hours": 150
    },
    "pato_regedit": {
        "name": "Patoteam Regedit Orange",
        "3 Days": 200,
        "7 Days": 330,
        "15 Days": 500,
        "30 Days": 920
    },
    "hg_cheats_nr": {
        "name": "Hg Cheats Apk",
        "1 Days": 55,
        "7 Days": 140,
        "10 Days": 179,
        "30 Days": 425
    },

    # OTHER EXISTING PACKAGES
    "drip": {"name": "Drip Client Apk", 1: 120, 3: 220, 7: 380, 15: 580, 30: 850},
    "drip_proxy": {"name": "Drip Client Proxy Apk", 1: 120, 3: 220, 7: 380, 30: 850},
    "prime": {"name": "Prime Hook Apk", 1: 140, 3: 240, 7: 450},
    "hg_proxy": {"name": "Hg Proxy Apk", 1: 150, 7: 350, 10: 450, 30: 880},
    "patorange": {"name": "Patoteam Orange", 3: 320, 7: 500, 15: 850, 30: 1350},
    "patblue": {"name": "Patoteam Blue", 3: 380, 7: 600, 15: 900, 30: 1450},
    "brmods_nr": {"name": "Br Mods Non Root", 1: 130, 7: 380, 15: 650, 30: 900},
    "reaper_nr": {"name": "Reaper xPro Apk", 10: 500, 30: 1250},
    "silent_nr": {"name": "Silent Cheats Apkmod", 1: 160, 3: 290, 7: 520, 14: 880, 28: 1300},
    "brmods_root": {"name": "Br Mods Apk", 1: 110, 7: 360, 15: 620, 30: 880},
    "reaper_root": {"name": "Reaper x Pro", 10: 480, 30: 1100},
    "drip_root": {"name": "Drip Client Root", 1: 100, 7: 450, 30: 900},
    "hg_root": {"name": "Hg Cheats Apk (Root)", 1: 120, 7: 280, 10: 400, 30: 850},
    "stricks": {"name": "Stricks Br ~ Alpha", 1: 100, 5: 230, 7: 350, 15: 650, 30: 850},
    "xyz": {"name": "Xyz Cheats Apk", 1: 100, 3: 220, 7: 420, 15: 720, 30: 1100},
    "hikari": {"name": "Hikari Mod Apk", 1: 100, 3: 210, 7: 420, 15: 720, 30: 1100},
    "lk": {"name": "LK Team Apk", 1: 120, 5: 250, 10: 360, 30: 950},
    "safe": {"name": "Silent Cheats [Safe]", 1: 120, 3: 240, 7: 480, 14: 820, 28: 1200},
    "brutal": {"name": "Silent Cheats [Brutal]", 1: 120, 3: 240, 7: 480, 14: 830, 30: 1250},
    "xreg": {"name": "Xreg Safe Apk", 1: 130, 10: 420, 20: 700, 30: 950},
    "rapid": {"name": "Rapid Core Apk", 1: 130, 7: 420, 14: 780, 30: 1500},
    "haxx": {"name": "Haxx-cker Pro", 10: 750, 20: 1450, 30: 1950},
    "zytron": {"name": "Zytron Pro Apk", 1: 120, 7: 450, 15: 680, 30: 880},
    "angry": {"name": "Angry Mod Apk", 1: 110, 7: 450, 15: 750, 30: 1050},
    "scorpio_lite": {"name": "Scorpio Mods [Lite]", 7: 350, 15: 580, 30: 850},
    "scorpio_brutal": {"name": "Scorpio Mods [Brutal]", 7: 420, 15: 650, 30: 1150},
    "gbox": {"name": "Gbox Certificate", "1 year validity": 1400},
    "esing": {"name": "Esing Certificate", "1 year validity": 750},
    "fluorite": {"name": "Fluorite Ios", 1: 550, 7: 1750, 31: 2800},
    "migul_pro": {"name": "Migul ~ Pro", 1: 420, 7: 1250, 31: 2400},
    "migul_basic": {"name": "Migul ~ Basic", 1: 320, 7: 750, 31: 1850},
    "drip_pc": {"name": "Drip Client Pc", 1: 220, 7: 520, 15: 920, 30: 1450},
    "brmods_pc": {"name": "Br Mods Pc", 1: 120, 10: 500, 30: 980},
}

user_purchase_history = {}

def get_stock_count(filename):
    if not os.path.exists(filename):
        return 0
    try:
        with open(filename, "r", encoding="utf-8") as f:
            keys = f.readlines()
        return len([k for k in keys if k.strip()])
    except:
        return 0

@bot.message_handler(commands=['start'])
def send_welcome(message):
    text = """✨ *WELCOME TO THE STORE*

🟢 Open Green Store Menu : Click below to access full app UI
🛒 Product Store : all key purchase & instantly delivery
👤 My Profile : check your account information
💰 Add Balance : deposit balance & secure service
🔑 All History : check all key purchase history
👥 Referral : invite friends & earn rewards
🌐 Support : bot problem fixed for support admin
🎁 Ludo Spin : play game and win balance
📥 Download Files : download latest apk for safety."""

    markup = InlineKeyboardMarkup()
    
    # 🟢 GREEN MINI APP BUTTON ADDED HERE
    btn_webapp = InlineKeyboardButton("🟢 Open Green Store Menu", web_app=WebAppInfo(url=WEB_APP_URL))
    
    btn_store = InlineKeyboardButton("🛒 Product Store", callback_data="btn_store")
    btn_profile = InlineKeyboardButton("👤 My Profile", callback_data="btn_profile")
    btn_balance = InlineKeyboardButton("💰 Add Balance", callback_data="btn_balance")
    btn_history = InlineKeyboardButton("🔑 All History", callback_data="btn_history")
    btn_referral = InlineKeyboardButton("👥 Referral", callback_data="btn_referral")
    btn_support = InlineKeyboardButton("🌐 Support", callback_data="btn_support")
    btn_ludo = InlineKeyboardButton("🎁 Ludo Spin", callback_data="btn_ludo")
    btn_download = InlineKeyboardButton("📥 Download Files", callback_data="btn_download")

    # Layout Arrangement
    markup.add(btn_webapp) # सबसे ऊपर हरा वेब ऐप बटन
    markup.add(btn_store) 
    markup.row(btn_profile, btn_balance) 
    markup.row(btn_history, btn_referral)
    markup.row(btn_support, btn_ludo)
    markup.add(btn_download)

    bot.send_message(message.chat.id, text, reply_markup=markup, parse_mode='Markdown')

@bot.callback_query_handler(func=lambda call: True)
def callback_listener(call):
    user_id = call.from_user.id
    chat_id = call.message.chat.id
    message_id = call.message.message_id
    data = call.data

    back_markup = InlineKeyboardMarkup()
    back_markup.add(InlineKeyboardButton("🔙 BACK", callback_data="btn_back"))

    # 1. Back Button Handler
    if data == "btn_back":
        bot.delete_message(chat_id=chat_id, message_id=message_id)
        send_welcome(call.message)

    # 2. Main Store Button
    elif data == "btn_store":
        text = "🛒 *SELECT PRODUCT PANEL*\n\n✅ Choose a panel to view its packages:"
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("🤖 ANDROID NON ROOT PANEL", callback_data="pnl_nonroot"))
        markup.add(InlineKeyboardButton("🤖 ANDROID ROOT PANEL", callback_data="pnl_root"))
        markup.add(InlineKeyboardButton("🍎 IPHONE PANEL", callback_data="pnl_iphone"))
        markup.add(InlineKeyboardButton("💻 PC PANEL", callback_data="pnl_pc"))
        markup.add(InlineKeyboardButton("🔙 BACK", callback_data="btn_back"))
        bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=text, parse_mode='Markdown', reply_markup=markup)

    # 3. Profile
    elif data == "btn_profile":
        user_name = call.from_user.first_name
        join_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        profile_text = (
            f"👤 **— YOUR SECURE PROFILE —** 👤\n\n"
            f"👤 Grid ID: `{user_id}`\n"
            f"👑 Name: {user_name}\n"
            f"👑 Account Level: 👤 Regular User\n\n"
            f"💰 **— Wallet —** 🪙\n"
            f"💰 Current Balance: ₹0.00 (~ $0.00) 🪙\n\n"
            f"📈 **— Global Statistics —**\n"
            f"🗂️ Total Orders: {len(user_purchase_history.get(user_id, []))}\n"
            f"💸 Total Spent: ₹0.00 (~ $0.00)\n"
            f"👥 Total Referrals: 0\n\n"
            f"📅 Joined Grid: {join_date}"
        )
        profile_markup = InlineKeyboardMarkup()
        profile_markup.add(InlineKeyboardButton("🎁 Redeem Promo Code", callback_data="btn_redeem"))
        profile_markup.add(InlineKeyboardButton("🔙 BACK", callback_data="btn_back"))
        bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=profile_text, parse_mode='Markdown', reply_markup=profile_markup)

    elif data == "btn_redeem":
        bot.answer_callback_query(call.id, "⚠️ आपके पास कोई वैलिड प्रोमो कोड नहीं है!", show_alert=True)

    # 4. Support
    elif data == "btn_support":
        text = "🌐 *SUPPORT*\n\nअगर कोई समस्या है तो एडमिन से संपर्क करें:\n👉 @Vickyseller0"
        bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=text, parse_mode='Markdown', reply_markup=back_markup)

    # 5. History
    elif data == "btn_history":
        user_history = user_purchase_history.get(user_id, [])
        if not user_history:
            history_text = "🔑 *PURCHASE HISTORY*\n\nYou haven't made any purchases yet. Your vault is empty."
        else:
            history_text = "🔑 *YOUR PURCHASE HISTORY*\n\n"
            for idx, item in enumerate(user_history, 1):
                history_text += f"{idx}. 📦 {item['app']} ({item['duration']}) - ₹{item['price']}\n   🕒 {item['time']}\n\n"
        bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=history_text, parse_mode='Markdown', reply_markup=back_markup)

    # 6. Download
    elif data == "btn_download":
        text = "📥 *DOWNLOAD PREMIUM APK & FILES*\n\n🔒 All our highly secured, premium, and updated files are securely hosted on our private channel!\n\n✨ *WHAT YOU GET:*\n• Latest APK Updates 🚀\n• 100% Virus Free & Secure 🛡️\n• All Configs & Scripts ⚙️\n• Complete Installation Guides 📖"
        download_markup = InlineKeyboardMarkup()
        download_markup.add(InlineKeyboardButton("📢 Access Download Channel", url="https://t.me/allfileupdate2"))
        download_markup.add(InlineKeyboardButton("🔙 BACK", callback_data="btn_back"))
        bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=text, parse_mode='Markdown', reply_markup=download_markup)

    # 7. Add Balance
    elif data == "btn_balance":
        upi_id = "vicky3198737@axl" 
        qr_url = f"https://api.qrserver.com/v1/create-qr-code/?size=300x300&data=upi://pay?pa={upi_id}%26pn=Vicky%20Store"
        text = f"💰 *ADD BALANCE*\n\nपेमेंट करने के लिए नीचे दिए गए QR Code को स्कैन करें या UPI ID इस्तेमाल करें:\n\n💳 *UPI ID:* `{upi_id}`\n\nपेमेंट का स्क्रीनशॉट यहाँ भेजें 👉 @Vickyseller0"
        bot.delete_message(chat_id=chat_id, message_id=message_id)
        bot.send_photo(chat_id=chat_id, photo=qr_url, caption=text, parse_mode='Markdown', reply_markup=back_markup)

    # 8. Referral
    elif data == "btn_referral":
        bot_username = bot.get_me().username
        ref_link = f"https://t.me/{bot_username}?start={user_id}"
        text = f"👥 *AFFILIATE PROGRAM*\n\n✅ *Status:* ACTIVE\n🏆 Earn 15% commission on every successful purchase made by your referred friends!\n\n👥 Total Referred: 0\n💰 Total Earned: ₹0.00 (~ $0.00)\n\n🔗 *Your Invite Link:*\n`{ref_link}`"
        bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=text, parse_mode='Markdown', reply_markup=back_markup)

    # 9. Ludo Spin
    elif data == "btn_ludo":
        text = "🎁 *LUDO SPIN & WIN*\n\nचक्र घुमाएं और पुरस्कार जीतें!\n⏳ *नियम:* आप इसे 24 घंटे में सिर्फ 1 बार घुमा सकते हैं।"
        spin_markup = InlineKeyboardMarkup()
        spin_markup.add(InlineKeyboardButton("🎲 Spin Dice Now", callback_data="btn_dospin"))
        spin_markup.add(InlineKeyboardButton("🔙 BACK", callback_data="btn_back"))
        bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=text, parse_mode='Markdown', reply_markup=spin_markup)

    elif data == "btn_dospin":
        current_time = time.time()
        cooldown_period = 86400  
        if user_id in user_last_spin:
            elapsed_time = current_time - user_last_spin[user_id]
            if elapsed_time < cooldown_period:
                bot.answer_callback_query(call.id, "⏳ Cooldown Active!\nYou already played today. Come back tomorrow.", show_alert=True)
                return

        user_last_spin[user_id] = current_time
        win_amount = random.choice([0.10, 0.30, 0.60, 1.00, 2.00])
        spin_text = f"🎉 बधाई हो! आपने Ludo Spin में **₹{win_amount}** जीत लिया है!\n\nइसे क्लेम करने के लिए स्क्रीनशॉट भेजें 👉 @Vickyseller0"
        spin_markup = InlineKeyboardMarkup()
        spin_markup.add(InlineKeyboardButton("🔙 BACK", callback_data="btn_back"))
        bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=spin_text, parse_mode='Markdown', reply_markup=spin_markup)

    # 10. Panels
    elif data == "pnl_nonroot":
        text = "🛒 *ANDROID NON ROOT PANELS*\n\n✅ Choose an app:"
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("💥 VALA MOD APK", callback_data="app_vala_mod"))
        markup.add(InlineKeyboardButton("📱 Drip Client Apk", callback_data="app_drip"))
        markup.add(InlineKeyboardButton("📱 Drip Client Proxy Apk", callback_data="app_drip_proxy"))
        markup.add(InlineKeyboardButton("📱 Hg Cheats Apk", callback_data="app_hg_cheats_nr"))
        markup.add(InlineKeyboardButton("📱 Prime Hook Apk", callback_data="app_prime"))
        markup.add(InlineKeyboardButton("📱 HG Proxy Apk", callback_data="app_hg_proxy"))
        markup.add(InlineKeyboardButton("📱 Patoteam Orange", callback_data="app_patorange"))
        markup.add(InlineKeyboardButton("📱 Patoteam Blue", callback_data="app_patblue"))
        markup.add(InlineKeyboardButton("📱 Br Mods Non Root", callback_data="app_brmods_nr"))
        markup.add(InlineKeyboardButton("📱 Reaper xPro Apk", callback_data="app_reaper_nr"))
        markup.add(InlineKeyboardButton("📱 Silent Cheats ApkMod", callback_data="app_silent_nr"))
        markup.add(InlineKeyboardButton("📱 NineX Mod Injector", callback_data="app_ninex"))
        markup.add(InlineKeyboardButton("📱 ABCD Panel", callback_data="app_abcd"))
        markup.add(InlineKeyboardButton("📱 Patoteam Regedit Orange", callback_data="app_pato_regedit"))
        markup.add(InlineKeyboardButton("📱 AimHack Apk", callback_data="app_aimhack"))
        markup.add(InlineKeyboardButton("🔙 BACK TO PANELS", callback_data="btn_store"))
        bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=text, parse_mode='Markdown', reply_markup=markup)

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
        bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=text, parse_mode='Markdown', reply_markup=markup)

    elif data == "pnl_iphone":
        text = "🛒 *IPHONE PANELS*\n\n✅ Choose an app:"
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("🍏 Gbox Certificate", callback_data="app_gbox"))
        markup.add(InlineKeyboardButton("🍏 Esing Certificate", callback_data="app_esing"))
        markup.add(InlineKeyboardButton("🍏 Fluorite Ios", callback_data="app_fluorite"))
        markup.add(InlineKeyboardButton("🍏 Migul ~ Pro", callback_data="app_migul_pro"))
        markup.add(InlineKeyboardButton("🍏 Migul ~ Basic", callback_data="app_migul_basic"))
        markup.add(InlineKeyboardButton("🔙 BACK TO PANELS", callback_data="btn_store"))
        bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=text, parse_mode='Markdown', reply_markup=markup)

    elif data == "pnl_pc":
        text = "💻 *PC PANELS*\n\n✅ Choose an app:"
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("💻 Drip Client Pc", callback_data="app_drip_pc"))
        markup.add(InlineKeyboardButton("💻 Br Mods Pc", callback_data="app_brmods_pc"))
        markup.add(InlineKeyboardButton("🔙 BACK TO PANELS", callback_data="btn_store"))
        bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=text, parse_mode='Markdown', reply_markup=markup)

    # 11. Apps Details (Only Single Price Display)
    elif data.startswith("app_"):
        app_code = data.replace("app_", "")
        filename = f"{app_code}_keys.txt"
        stock = get_stock_count(filename)
        stock_status = "📦 ✅ In Stock" if stock > 0 else "📦 ❌ Out of Stock"

        default_app = {"name": app_code.upper(), 1: 100}
        app_data = APP_PRICES.get(app_code, default_app)
        app_title = app_data["name"]

        text = f"🛒 *PANEL - {app_title.upper()} PACKAGES*\n━━━━━━━━━━━━━━━━━━\n\n"
        for duration, price in app_data.items():
            if duration != "name":
                price_usd = round(price / 90.0, 2)
                val_text = f"{duration} Days" if isinstance(duration, int) else f"{duration}"
                text += (
                    f"🛒 ⏱️ **Validity: {val_text}**\n"
                    f"💰 Price: ₹{price}.00 (~ ${price_usd})\n"
                    f"📱 Limit: 1 Device | {stock_status}\n\n"
                )
        text += "✅ *Select package below to instantly purchase:*"

        markup = InlineKeyboardMarkup()
        for duration, price in app_data.items():
            if duration != "name":
                price_usd = round(price / 90.0, 2)
                val_text = f"{duration} Days" if isinstance(duration, int) else f"{duration}"
                
                if stock > 0:
                    markup.add(InlineKeyboardButton(f"🛒 Buy {val_text} - ₹{price}.00 (~ ${price_usd})", callback_data=f"buy_{app_code}_{duration}"))
                else:
                    markup.add(InlineKeyboardButton(f"❌ {val_text} (Out of Stock)", callback_data=f"oos_{app_code}_{duration}"))

        back_btn = "btn_store"
        if app_code in ["vala_mod", "drip", "drip_proxy", "hg_cheats_nr", "prime", "hg_proxy", "patorange", "patblue", "brmods_nr", "reaper_nr", "silent_nr", "ninex", "abcd", "pato_regedit", "aimhack"]:
            back_btn = "pnl_nonroot"
        elif app_code in ["brmods_root", "reaper_root", "drip_root", "hg_root", "stricks", "xyz", "hikari", "lk", "safe", "brutal", "xreg", "rapid", "haxx", "zytron", "angry", "scorpio_lite", "scorpio_brutal"]:
            back_btn = "pnl_root"
        elif app_code in ["gbox", "esing", "fluorite", "migul_pro", "migul_basic"]:
            back_btn = "pnl_iphone"
        elif app_code in ["drip_pc", "brmods_pc"]:
            back_btn = "pnl_pc"
            
        markup.add(InlineKeyboardButton("🔙 BACK TO PANELS", callback_data=back_btn))
        bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=text, parse_mode='Markdown', reply_markup=markup)

    # 12. Individual Buy Click
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
            text=f"🛒 आपने **{app_real_name}** का **{duration_selected}** वाला पैक सेलेक्ट किया है।\n\n💰 बैलेंस एड करने या खरीदने के लिए एडमिन से संपर्क करें 👉 @Vickyseller0",
            parse_mode='Markdown'
        )

    # 13. Out of Stock Alert
    elif data.startswith("oos_"):
        bot.answer_callback_query(call.id, "⚠️ यह पैकेज अभी स्टॉक में उपलब्ध नहीं है!", show_alert=True)

print("Bot सफलतापूर्वक चालू हो गया है...")
bot.polling(none_stop=True)
