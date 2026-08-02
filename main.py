import telebot
import random
import time
import os
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

TOKEN = '8407812250:AAFrAlJZuKUMRqYl4B5So31B5zc5rDqWGYY'
bot = telebot.TeleBot(TOKEN)

user_last_spin = {}

# --- सभी ऐप्स के सही दिन और उनके अपडेटेड प्राइसेज (₹20 बढ़ाकर) ---
APP_PRICES = {
    # Non Root Apps
    "drip": {"name": "Drip Client Apk", 1: 80, 3: 160, 7: 270, 15: 420, 30: 620},
    "drip_proxy": {"name": "Drip Client Proxy Apk", 1: 80, 3: 160, 7: 270, 30: 620},
    "prime": {"name": "Prime Hook Apk", 1: 95, 3: 160, 7: 315},
    "hg_proxy": {"name": "Hg Proxy Apk", 1: 100, 7: 240, 10: 310, 30: 605},
    "patorange": {"name": "Patoteam Orange", 3: 230, 7: 370, 15: 605, 30: 960},
    "patblue": {"name": "Patoteam Blue", 3: 265, 7: 440, 15: 640, 30: 1020},
    "brmods_nr": {"name": "Br Mods Non Root", 1: 90, 7: 270, 15: 460, 30: 640},
    "reaper_nr": {"name": "Reaper xPro Apk", 10: 365, 30: 900},
    "silent_nr": {"name": "Silent Cheats Apkmod", 1: 110, 3: 200, 7: 370, 14: 620, 28: 920},

    # Root Apps
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

    # iPhone Apps
    "gbox": {"name": "Gbox Certificate", "1 year validity": 1000},
    "esing": {"name": "Esing Certificate", "1 year validity": 500},
    "fluorite": {"name": "Fluorite Ios", 1: 390, 7: 1240, 31: 2000},
    "migul_pro": {"name": "Migul ~ Pro", 1: 300, 7: 890, 31: 1700},
    "migul_basic": {"name": "Migul ~ Basic", 1: 220, 7: 530, 31: 1320},

    # PC Apps
    "drip_pc": {"name": "Drip Client Pc", 1: 150, 7: 360, 15: 650, 30: 1020},
    "brmods_pc": {"name": "Br Mods Pc", 1: 85, 10: 350, 30: 690},
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

@bot.message_handler(commands=['start'])
def send_welcome(message):
    text = """✨ *WELCOME TO THE STORE*

🛒 Product Store : all key purchase & instantly delivery
👤 My Profile : check your account information
💰 Add Balance : deposit balance & secure service
🔑 All History : check all key purchase history
👥 Referral : invite friends & earn rewards
🛟 Support : bot problem fixed for support admin
🎁 Ludo Spin : play game and win balance
📥 Download Files : download latest apk for safety."""

    markup = InlineKeyboardMarkup()
    btn_store = InlineKeyboardButton("🛒 Product Store", callback_data="store")
    btn_profile = InlineKeyboardButton("👤 My Profile", callback_data="profile")
    btn_balance = InlineKeyboardButton("💰 Add Balance", callback_data="balance")
    btn_history = InlineKeyboardButton("🔑 All History", callback_data="history")
    btn_referral = InlineKeyboardButton("👥 Referral", callback_data="referral")
    btn_support = InlineKeyboardButton("🛟 Support", callback_data="support")
    btn_ludo = InlineKeyboardButton("🎁 Ludo Spin", callback_data="ludo_spin")
    btn_download = InlineKeyboardButton("📥 Download Files", callback_data="download")

    markup.add(btn_store) 
    markup.row(btn_profile, btn_balance) 
    markup.row(btn_history, btn_referral)
    markup.row(btn_support, btn_ludo)
    markup.add(btn_download)

    bot.send_message(message.chat.id, text, reply_markup=markup, parse_mode='Markdown')

@bot.callback_query_handler(func=lambda call: True)
def callback_listener(call):
    
    user_id = call.from_user.id
    back_markup = InlineKeyboardMarkup()
    back_markup.add(InlineKeyboardButton("🔙 Back", callback_data="back"))
    
    if call.data == "back":
        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
        send_welcome(call.message)

    elif call.data == "profile":
        user_name = call.from_user.first_name
        text = f"👤 *MY PROFILE*\n\n*Name:* {user_name}\n*User ID:* `{user_id}`\n*Wallet Balance:* ₹0.00\n*Total Referrals:* 0"
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=text, parse_mode='Markdown', reply_markup=back_markup)

    elif call.data == "support":
        text = "🛟 *SUPPORT*\n\nअगर कोई समस्या है तो एडमिन से संपर्क करें:\n👉 @Vickyseller0"
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=text, parse_mode='Markdown', reply_markup=back_markup)

    elif call.data == "download":
        text = "📥 *DOWNLOAD FILES*\n\nलेटेस्ट फाइल्स यहाँ से डाउनलोड करें:\n🔗 [All File Update](https://t.me/allfileupdate2)"
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=text, parse_mode='Markdown', disable_web_page_preview=True, reply_markup=back_markup)
        
    elif call.data == "balance":
        upi_id = "vicky3198737@axl" 
        qr_url = f"https://api.qrserver.com/v1/create-qr-code/?size=300x300&data=upi://pay?pa={upi_id}%26pn=Vicky%20Store"
        text = f"💰 *ADD BALANCE*\n\nपेमेंट करने के लिए नीचे दिए गए QR Code को स्कैन करें या UPI ID इस्तेमाल करें:\n\n💳 *UPI ID:* `{upi_id}`\n\nपेमेंट का स्क्रीनशॉट यहाँ भेजें 👉 @Vickyseller0"
        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
        bot.send_photo(chat_id=call.message.chat.id, photo=qr_url, caption=text, parse_mode='Markdown', reply_markup=back_markup)

    elif call.data == "referral":
        bot_username = bot.get_me().username
        ref_link = f"https://t.me/{bot_username}?start={user_id}"
        text = f"👥 *REFERRAL SYSTEM*\n\nदोस्तों को इनवाइट करें और हर रेफरल पर ₹5 कमाएं!\n\n🔗 *आपका रेफरल लिंक:*\n`{ref_link}`"
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=text, parse_mode='Markdown', reply_markup=back_markup)

    elif call.data == "ludo_spin":
        text = "🎁 *LUDO SPIN & WIN*\n\nचक्र घुमाएं और पुरस्कार जीतें!\n⏳ *नियम:* आप इसे 24 घंटे में सिर्फ 1 बार घुमा सकते हैं।"
        spin_markup = InlineKeyboardMarkup()
        spin_markup.add(InlineKeyboardButton("🎲 Spin Now", callback_data="do_spin"))
        spin_markup.add(InlineKeyboardButton("🔙 Back", callback_data="back"))
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=text, parse_mode='Markdown', reply_markup=spin_markup)

    elif call.data == "do_spin":
        current_time = time.time()
        cooldown_period = 86400  
        
        if user_id in user_last_spin:
            elapsed_time = current_time - user_last_spin[user_id]
            if elapsed_time < cooldown_period:
                remaining_hours = int((cooldown_period - elapsed_time) / 3600)
                bot.answer_callback_query(call.id, f"⚠️ आप 24 घंटे में सिर्फ 1 बार स्पिन कर सकते हैं! लगभग {remaining_hours} घंटे बाद दोबारा कोशिश करें.", show_alert=True)
                return

        user_last_spin[user_id] = current_time
        win_amount = random.choice([0.10, 0.30, 0.60, 1.00, 2.00])
        spin_text = f"🎉 बधाई हो! आपने Ludo Spin में **₹{win_amount}** जीत लिया है!\n\nइसे क्लेम करने के लिए स्क्रीनशॉट भेजें 👉 @Vickyseller0"
            
        spin_markup = InlineKeyboardMarkup()
        spin_markup.add(InlineKeyboardButton("🔙 Back", callback_data="back"))
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=spin_text, parse_mode='Markdown', reply_markup=spin_markup)

    elif call.data == "store":
        text = "🛒 *SELECT PRODUCT PANEL*\n\n✅ Choose a panel to view its packages:"
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("🤖 ANDROID NON ROOT PANEL", callback_data="panel_nonroot"))
        markup.add(InlineKeyboardButton("🤖 ANDROID ROOT PANEL", callback_data="panel_root"))
        markup.add(InlineKeyboardButton("🍎 IPHONE PANEL", callback_data="panel_iphone"))
        markup.add(InlineKeyboardButton("💻 PC PANEL", callback_data="panel_pc"))
        markup.add(InlineKeyboardButton("🔙 BACK", callback_data="back"))
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=text, parse_mode='Markdown', reply_markup=markup)

    elif call.data == "panel_nonroot":
        text = "🛒 *ANDROID NON ROOT PANELS*\n\n✅ Choose an app:"
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("📱 Drip Client Apk", callback_data="app_drip"))
        markup.add(InlineKeyboardButton("📱 Drip Client Proxy Apk", callback_data="app_drip_proxy"))
        markup.add(InlineKeyboardButton("📱 Prime Hook Apk", callback_data="app_prime"))
        markup.add(InlineKeyboardButton("📱 HG Proxy Apk", callback_data="app_hg_proxy"))
        markup.add(InlineKeyboardButton("📱 Patoteam Orange", callback_data="app_patorange"))
        markup.add(InlineKeyboardButton("📱 Patoteam Blue", callback_data="app_patblue"))
        markup.add(InlineKeyboardButton("📱 Br Mods Non Root", callback_data="app_brmods_nr"))
        markup.add(InlineKeyboardButton("📱 Reaper xPro Apk", callback_data="app_reaper_nr"))
        markup.add(InlineKeyboardButton("📱 Silent Cheats Apkmod", callback_data="app_silent_nr"))
        markup.add(InlineKeyboardButton("🔙 BACK TO PANELS", callback_data="store"))
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=text, parse_mode='Markdown', reply_markup=markup)

    elif call.data == "panel_root":
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
        markup.add(InlineKeyboardButton("🔙 BACK TO PANELS", callback_data="store"))
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=text, parse_mode='Markdown', reply_markup=markup)

    elif call.data == "panel_iphone":
        text = "🛒 *IPHONE PANELS*\n\n✅ Choose an app:"
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("🍏 Gbox Certificate", callback_data="app_gbox"))
        markup.add(InlineKeyboardButton("🍏 Esing Certificate", callback_data="app_esing"))
        markup.add(InlineKeyboardButton("🍏 Fluorite Ios", callback_data="app_fluorite"))
        markup.add(InlineKeyboardButton("🍏 Migul ~ Pro", callback_data="app_migul_pro"))
        markup.add(InlineKeyboardButton("🍏 Migul ~ Basic", callback_data="app_migul_basic"))
        markup.add(InlineKeyboardButton("🔙 BACK TO PANELS", callback_data="store"))
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=text, parse_mode='Markdown', reply_markup=markup)

    elif call.data == "panel_pc":
        text = "💻 *PC PANELS*\n\n✅ Choose an app:"
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("💻 Drip Client Pc", callback_data="app_drip_pc"))
        markup.add(InlineKeyboardButton("💻 Br Mods Pc", callback_data="app_brmods_pc"))
        markup.add(InlineKeyboardButton("🔙 BACK TO PANELS", callback_data="store"))
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=text, parse_mode='Markdown', reply_markup=markup)

    elif call.data.startswith("app_"):
        app_code = call.data.replace("app_", "")
        filename = f"{app_code}_keys.txt"
        stock = get_stock_count(filename)
        stock_status = "📦 ✅ In Stock" if stock > 0 else "📦 ❌ Out of Stock"

        default_app = {"name": app_code.upper(), 1: 80, 7: 300, 30: 700}
        app_data = APP_PRICES.get(app_code, default_app)
        
        app_title = app_data["name"]

        text = f"🛒 *PANEL - {app_title.upper()} PACKAGES*\n"
        text += "━━━━━━━━━━━━━━━━━━\n\n"
        
        for days, price in app_data.items():
            if days != "name":
                usd_price = round(price / 90.0, 2)
                text += f"🛒 ⏱️ **Validity: {days}**\n💰 Price: ₹{price}.00 (~ ${usd_price})\n📱 Limit: 1 Device | {stock_status}\n\n"
        
        text += "✅ *Select package below to instantly purchase:*"

        markup = InlineKeyboardMarkup()
        for days, price in app_data.items():
            if days != "name":
                usd_price = round(price / 90.0, 2)
                if stock > 0:
                    markup.add(InlineKeyboardButton(f"🛒 Buy {days} - ₹{price}.00 (~ ${usd_price})", callback_data="balance"))
                else:
                    markup.add(InlineKeyboardButton(f"❌ {days} (Out of Stock)", callback_data="oos"))

        back_btn = "store"
        if app_code in ["drip", "drip_proxy", "prime", "hg_proxy", "patorange", "patblue", "brmods_nr", "reaper_nr", "silent_nr"]:
            back_btn = "panel_nonroot"
        elif app_code in ["brmods_root", "reaper_root", "drip_root", "hg_root", "stricks", "xyz", "hikari", "lk", "safe", "brutal", "xreg", "rapid", "haxx", "zytron", "angry", "scorpio_lite", "scorpio_brutal"]:
            back_btn = "panel_root"
        elif app_code in ["gbox", "esing", "fluorite", "migul_pro", "migul_basic"]:
            back_btn = "panel_iphone"
        elif app_code in ["drip_pc", "brmods_pc"]:
            back_btn = "panel_pc"
            
        markup.add(InlineKeyboardButton("🔙 BACK TO PANELS", callback_data=back_btn))
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=text, parse_mode='Markdown', reply_markup=markup)

    elif call.data == "oos":
        bot.answer_callback_query(call.id, "⚠️ यह पैकेज अभी स्टॉक में नहीं है!", show_alert=True)
        
    else:
        bot.answer_callback_query(call.id, "यह फीचर जल्द ही आएगा!")

print("Bot सफलतापूर्वक चालू हो गया है! Telegram पर जाकर चेक करें...")
bot.polling(none_stop=True)
