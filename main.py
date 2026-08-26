import logging
import requests
import math
import sqlite3
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

# ----------------- CONFIGURATION -----------------
BOT_TOKEN = "8497450621:AAFAl7KrMth6mlJvHwzW5DuRDSsG8LQB0wk"      # BotFather se mila token
API_URL = "https://kissmilegi.com/api/v2"
API_KEY = "09185a642a93992b69345366dfb42e439f4891e4"        # Kissmilegi API Key

# Payment Details
MY_UPI_ID = "vickyxmodeofc@axl"             # Paytm / UPI ID
BINANCE_PAY_ID = "123456789"                # Binance Pay ID
BKASH_NUMBER = "+8801XXXXXXXXX"            # bKash Personal Number

# Support Details
WHATSAPP_NUMBER = "8303304640"
TELEGRAM_USERNAME = "VICKYXMOD"            # Without @

SERVICES_PER_PAGE = 5
# ----------------- DATABASE SETUP -----------------
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)

def init_db():
    conn = sqlite3.connect('vicky_store.db')
    cursor = conn.cursor()
    # Users & Wallet Balance Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            balance REAL DEFAULT 0.0
        )
    ''')
    # Orders History Table (Kabhi delete nahi hogi)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            order_id TEXT,
            srv_id TEXT,
            qty TEXT,
            link TEXT,
            total_charge REAL
        )
    ''')
    # Tickets Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tickets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            message TEXT
        )
    ''')
    conn.commit()
    conn.close()

init_db()

def get_user_balance(user_id):
    conn = sqlite3.connect('vicky_store.db')
    cursor = conn.cursor()
    cursor.execute('SELECT balance FROM users WHERE user_id = ?', (user_id,))
    row = cursor.fetchone()
    conn.close()
    if row is None:
        conn = sqlite3.connect('vicky_store.db')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO users (user_id, balance) VALUES (?, ?)', (user_id, 0.0))
        conn.commit()
        conn.close()
        return 0.0
    return row[0]

def update_user_balance(user_id, amount):
    conn = sqlite3.connect('vicky_store.db')
    cursor = conn.cursor()
    cursor.execute('UPDATE users SET balance = balance + ? WHERE user_id = ?', (amount, user_id))
    conn.commit()
    conn.close()

def save_order(user_id, order_id, srv_id, qty, link, charge):
    conn = sqlite3.connect('vicky_store.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO orders (user_id, order_id, srv_id, qty, link, total_charge) VALUES (?, ?, ?, ?, ?, ?)',
                   (user_id, order_id, srv_id, qty, link, charge))
    conn.commit()
    conn.close()

def get_user_orders(user_id):
    conn = sqlite3.connect('vicky_store.db')
    cursor = conn.cursor()
    cursor.execute('SELECT order_id, srv_id, qty, link, total_charge FROM orders WHERE user_id = ?', (user_id,))
    rows = cursor.fetchall()
    conn.close()
    return rows

def save_ticket(user_id, msg):
    conn = sqlite3.connect('vicky_store.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO tickets (user_id, message) VALUES (?, ?)', (user_id, msg))
    conn.commit()
    conn.close()

def get_user_tickets(user_id):
    conn = sqlite3.connect('vicky_store.db')
    cursor = conn.cursor()
    cursor.execute('SELECT message FROM tickets WHERE user_id = ?', (user_id,))
    rows = cursor.fetchall()
    conn.close()
    return [r[0] for r in rows]

# Temporary Cache for Order Steps
order_cache = {}

def call_smm_api(payload):
    payload['key'] = API_KEY
    try:
        response = requests.post(API_URL, data=payload, timeout=10)
        data = response.json()
        if payload.get('action') == 'services' and isinstance(data, list):
            for service in data:
                try:
                    if 'rate' in service:
                        service['rate'] = round(float(service['rate']) + 50.0, 2)
                except Exception:
                    pass
        return data
    except Exception as e:
        print("API Error:", e)
        return None

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    get_user_balance(user_id)  # Ensure user exists in DB

    keyboard = [
        [InlineKeyboardButton("🚀 Explore All Services", callback_data="catpage_0")],
        [InlineKeyboardButton("🎒 ADD BALANCE ☁️", callback_data="add_funds"), InlineKeyboardButton("💰 My Wallet", callback_data="check_balance")],
        [InlineKeyboardButton("👤 My Profile", callback_data="my_profile"), InlineKeyboardButton("💬 Support & Tickets", callback_data="support_menu")],
        [InlineKeyboardButton("📊 Track Order Status", callback_data="track_help"), InlineKeyboardButton("🔍 Search Service", callback_data="search_help")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    msg = (
        f"💖𝐖ᴇʟᴄᴏᴍᴇ 𝐓ᴏ 𝐏ʀᴇᴍɪᴜᴍ 𝐒ᴛᴏʀᴇ 💖\n\n"
        f"🔥 *The Ultimate, Fastest & Most Trusted Automated Digital Hub!*\n\n"
        f"💎 **AVAILABLE SERVICES & FEATURES:**\n"
        f"├ 📸 **Instagram:** Followers, Likes, Views, Comments\n"
        f"├ 🎬 **YouTube & Telegram:** Subscribers, Watchtime, Members\n"
        f"├ 🎵 **TikTok & Other Social Platforms:** Boost your reach\n"
        f"├ 🚀 **Super-Fast Instant Delivery** (Automated System)\n"
        f"└ 🛡️ **24/7 Secure Payments & Support**\n\n"
        f"━━━━━━━━━━━━━━━━━━━\n"
        f"👇 *Niche diye gaye buttons se apni service select karein:*"
    )
    
    if update.message:
        await update.message.reply_text(msg, reply_markup=reply_markup, parse_mode="Markdown")
    else:
        try:
            await update.callback_query.message.edit_text(msg, reply_markup=reply_markup, parse_mode="Markdown")
        except Exception:
            await update.callback_query.message.reply_text(msg, reply_markup=reply_markup, parse_mode="Markdown")

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data
    user_id = query.from_user.id

    if data.startswith("catpage_"):
        page = int(data.split("_")[1])
        services = call_smm_api({'action': 'services'})
        
        if not services or not isinstance(services, list):
            await query.message.reply_text("❌ Website API response me issue hai. Key check karein.")
            return

        categories = sorted(list(set([item.get('category', 'Other') for item in services])))
        cat_per_page = 8
        total_pages = math.ceil(len(categories) / cat_per_page)
        
        start_idx = page * cat_per_page
        end_idx = start_idx + cat_per_page
        current_cats = categories[start_idx:end_idx]

        keyboard = []
        for cat in current_cats:
            cat_id = categories.index(cat)
            context.user_data[f"c_{cat_id}"] = cat
            keyboard.append([InlineKeyboardButton(f"📁 {cat[:35]}", callback_data=f"srvpage_{cat_id}_0")])

        nav_buttons = []
        if page > 0:
            nav_buttons.append(InlineKeyboardButton("◀️ Prev", callback_data=f"catpage_{page-1}"))
        if page < total_pages - 1:
            nav_buttons.append(InlineKeyboardButton("Next ▶️", callback_data=f"catpage_{page+1}"))
        
        if nav_buttons:
            keyboard.append(nav_buttons)
            
        keyboard.append([InlineKeyboardButton("🔙 Main Menu", callback_data="main_menu")])
        
        text = f"📌 **Select Category** (Page {page+1}/{total_pages}):"
        try:
            await query.message.edit_text(text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="Markdown")
        except Exception:
            await query.message.reply_text(text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="Markdown")

    elif data.startswith("srvpage_"):
        parts = data.split("_")
        cat_id = int(parts[1])
        page = int(parts[2])
        
        cat_name = context.user_data.get(f"c_{cat_id}")
        services = call_smm_api({'action': 'services'})
        
        filtered = [s for s in services if s.get('category') == cat_name]
        total_pages = math.ceil(len(filtered) / SERVICES_PER_PAGE)
        
        start_idx = page * SERVICES_PER_PAGE
        end_idx = start_idx + SERVICES_PER_PAGE
        page_services = filtered[start_idx:end_idx]

        text = f"🔥 **Category:** {cat_name}\n"
        text += f"📄 **Page:** {page+1}/{total_pages}\n\n"

        keyboard = []
        for item in page_services:
            srv_id = item.get('service')
            rate = item.get('rate')
            text += f"🆔 **ID:** `{srv_id}` | 💰 **Rate:** ₹{rate}/k\n"
            text += f"📌 **Name:** {item.get('name')}\n"
            text += f"📊 **Min/Max:** {item.get('min')} - {item.get('max')}\n\n"
            
            keyboard.append([InlineKeyboardButton(f"🛒 Order ID: {srv_id} (Rate: ₹{rate}/k)", callback_data=f"calc_{srv_id}")])

        nav_buttons = []
        if page > 0:
            nav_buttons.append(InlineKeyboardButton("◀️ Prev", callback_data=f"srvpage_{cat_id}_{page-1}"))
        if page < total_pages - 1:
            nav_buttons.append(InlineKeyboardButton("Next ▶️", callback_data=f"srvpage_{cat_id}_{page+1}"))
            
        if nav_buttons:
            keyboard.append(nav_buttons)
            
        keyboard.append([InlineKeyboardButton("🔙 Back to Categories", callback_data="catpage_0")])
        
        try:
            await query.message.edit_text(text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="Markdown")
        except Exception:
            await query.message.reply_text(text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="Markdown")

    elif data.startswith("calc_"):
        srv_id = data.split("_")[1]
        services = call_smm_api({'action': 'services'})
        service_data = next((s for s in services if str(s.get('service')) == str(srv_id)), None)

        if not service_data:
            await query.message.reply_text("❌ Service detail load nahi ho saki.")
            return

        rate = float(service_data.get('rate', 0))

        text = (
            f"🧮 **Quantity & Price Calculator**\n\n"
            f"📌 **Service:** {service_data.get('name')}\n"
            f"🆔 **ID:** `{srv_id}`\n"
            f"💰 **Rate per 1000:** ₹{rate}\n\n"
            f"👇 **Niche se quantity select karein:**"
        )

        keyboard = [
            [
                InlineKeyboardButton(f"100 (₹{round(rate*0.1, 2)})", callback_data=f"setq_{srv_id}_100"),
                InlineKeyboardButton(f"500 (₹{round(rate*0.5, 2)})", callback_data=f"setq_{srv_id}_500")
            ],
            [
                InlineKeyboardButton(f"1000 (₹{round(rate*1.0, 2)})", callback_data=f"setq_{srv_id}_1000"),
                InlineKeyboardButton(f"5000 (₹{round(rate*5.0, 2)})", callback_data=f"setq_{srv_id}_5000")
            ],
            [InlineKeyboardButton("✍️ Custom Quantity", callback_data=f"customq_{srv_id}")],
            [InlineKeyboardButton("🔙 Back to Categories", callback_data="catpage_0")]
        ]
        
        try:
            await query.message.edit_text(text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="Markdown")
        except Exception:
            await query.message.reply_text(text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="Markdown")

    elif data.startswith("setq_"):
        _, srv_id, qty = data.split("_")
        order_cache[user_id] = {'srv_id': srv_id, 'qty': qty, 'state': 'WAITING_LINK'}
        await query.message.reply_text(f"✅ **Selected Quantity:** {qty}\n\n🔗 Ab apna **Target Link** text message me bhejein:")

    elif data.startswith("customq_"):
        srv_id = data.split("_")[1]
        order_cache[user_id] = {'srv_id': srv_id, 'state': 'WAITING_CUSTOM_QTY'}
        await query.message.reply_text("✍️ Aapko jitni quantity chahiye wo number text me bhejein:")

    elif data == "my_profile":
        bal = get_user_balance(user_id)
        history = get_user_orders(user_id)
        total_orders = len(history)

        text = (
            f"👤 **YOUR PROFILE & PURCHASE HISTORY** 📦\n\n"
            f"🆔 **Telegram ID:** `{user_id}`\n"
            f"💰 **Wallet Balance:** `₹{bal}`\n"
            f"🛒 **Total Orders Placed:** `{total_orders}`\n\n"
            f"━━━━━━━━━━━━━━━━━━━\n"
            f"📋 **Permanent Purchased History:**\n"
        )

        if not history:
            text += "_Aapne abhi tak koi order place nahi kiya hai._"
        else:
            for idx, ord_info in enumerate(history[-5:], 1):
                text += (
                    f"\n{idx}. 🆔 **Order ID:** `{ord_info[0]}`\n"
                    f"   🔹 **Service ID:** `{ord_info[1]}`\n"
                    f"   📊 **Quantity:** `{ord_info[2]}`\n"
                    f"   🔗 **Link:** {ord_info[3]}\n"
                    f"   💸 **Total Price:** ₹{ord_info[4]}\n"
                )

        keyboard = [[InlineKeyboardButton("🔙 Main Menu", callback_data="main_menu")]]
        try:
            await query.message.edit_text(text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="Markdown", disable_web_page_preview=True)
        except Exception:
            await query.message.reply_text(text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="Markdown", disable_web_page_preview=True)

    elif data == "support_menu":
        text = (
            "🌐💬 **PREMIUM SUPPORT CENTER**\n\n"
            "**Contact us via Telegram or WhatsApp for instant help, or open a support ticket for admin assistance.**"
        )
        
        keyboard = [
            [InlineKeyboardButton("✈️ Contact on Telegram", url=f"https://t.me/{TELEGRAM_USERNAME}")],
            [InlineKeyboardButton("💬 Contact on WhatsApp", url=f"https://wa.me/91{WHATSAPP_NUMBER}")],
            [
                InlineKeyboardButton("🎫 Open New Ticket", callback_data="open_ticket"),
                InlineKeyboardButton("📋 My Open Tickets", callback_data="view_tickets")
            ],
            [InlineKeyboardButton("🔙 BACK", callback_data="main_menu")]
        ]
        
        try:
            await query.message.edit_text(text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="Markdown")
        except Exception:
            await query.message.reply_text(text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="Markdown")

    elif data == "open_ticket":
        order_cache[user_id] = {'state': 'WAITING_TICKET_MSG'}
        keyboard = [[InlineKeyboardButton("🔙 BACK", callback_data="support_menu")]]
        await query.message.edit_text("✍️ Apni problem ya query ka message likh kar bhejein, aapka ticket open ho jayega:", reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="Markdown")

    elif data == "view_tickets":
        tickets = get_user_tickets(user_id)
        if not tickets:
            text = "📂 Aapka koi bhi open ticket nahi hai."
        else:
            text = "📂 **Aapke Open Tickets:**\n\n"
            for idx, t_msg in enumerate(tickets, 1):
                text += f"🎫 **Ticket #{idx}:** {t_msg}\n\n"
        
        keyboard = [[InlineKeyboardButton("🔙 BACK", callback_data="support_menu")]]
        try:
            await query.message.edit_text(text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="Markdown")
        except Exception:
            await query.message.reply_text(text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="Markdown")

    elif data == "add_funds":
        text = (
            "🎒 **ADD BALANCE** ☁️\n\n"
            "💭 **Select your preferred payment method.** ✅\n\n"
            "├ 💳 **UPI** — Fast Indian payments 🛑\n"
            "├ 🪙 **Binance** — Crypto payments 💳\n"
            "└ 💸 **bKash** — Bangladesh Taka payments 🇧🇩\n\n"
            "🛡️ **Payments are verified securely.** ✅"
        )
        keyboard = [
            [InlineKeyboardButton("💳 Paytm UPI", callback_data="pay_upi"), InlineKeyboardButton("🪙 Binance Pay", callback_data="pay_binance")],
            [InlineKeyboardButton("💰 bKash (taka)", callback_data="pay_bkash")],
            [InlineKeyboardButton("🔙 BACK", callback_data="main_menu")]
        ]
        try:
            await query.message.edit_text(text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="Markdown")
        except Exception:
            await query.message.reply_text(text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="Markdown")

    elif data == "pay_upi":
        order_cache[user_id] = {'state': 'WAITING_FUND_AMOUNT'}
        keyboard = [[InlineKeyboardButton("🔙 BACK", callback_data="add_funds")]]
        await query.message.edit_text("💳 **Paytm UPI Payment**\n\nKitna amount add karna chahte hain? Write amount in ₹ (Example: `100`):", reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="Markdown")

    elif data == "pay_binance":
        text = (
            "🪙 **Binance Pay (Crypto)**\n\n"
            f"🔹 **Binance Pay ID:** `{BINANCE_PAY_ID}`\n\n"
            "Payment complete karne ke baad Transaction Hash/SS admin ko bhej kar wallet top-up karayein."
        )
        keyboard = [[InlineKeyboardButton("🔙 BACK", callback_data="add_funds")]]
        await query.message.edit_text(text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="Markdown")

    elif data == "pay_bkash":
        text = (
            "🇧🇩 **bKash Payment (Bangladesh)**\n\n"
            f"🔹 **bKash Personal Number:** `{BKASH_NUMBER}`\n\n"
            "1️⃣ Send Money karke TrxID copy karein.\n"
            "2️⃣ TrxID aur Screenshot admin ko bhejein."
        )
        keyboard = [[InlineKeyboardButton("🔙 BACK", callback_data="add_funds")]]
        await query.message.edit_text(text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="Markdown")

    elif data == "check_balance":
        bal = get_user_balance(user_id)
        keyboard = [[InlineKeyboardButton("🎒 ADD BALANCE", callback_data="add_funds"), InlineKeyboardButton("🔙 Main Menu", callback_data="main_menu")]]
        await query.message.reply_text(f"💰 **Aapka Total Balance:** ₹{bal}", reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="Markdown")

    elif data == "track_help":
        msg = "📊 **Order Track Karne Ka Tarika:**\n\nMessage bhejein: `/status ORDER_ID`"
        keyboard = [[InlineKeyboardButton("🔙 Main Menu", callback_data="main_menu")]]
        await query.message.edit_text(msg, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="Markdown")

    elif data == "search_help":
        msg = "🔍 **Service Dhoondhne Ka Tarika:**\n\nMessage bhejein: `/search KEYWORD`"
        keyboard = [[InlineKeyboardButton("🔙 Main Menu", callback_data="main_menu")]]
        await query.message.edit_text(msg, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="Markdown")

    elif data == "main_menu":
        await start(update, context)

async def handle_text_messages(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    text_val = update.message.text.strip()

    if user_id in order_cache:
        state_info = order_cache[user_id]
        current_state = state_info.get('state')
        
        if current_state == 'WAITING_TICKET_MSG':
            del order_cache[user_id]
            save_ticket(user_id, text_val)
            
            keyboard = [[InlineKeyboardButton("🔙 Main Menu", callback_data="main_menu")]]
            await update.message.reply_text("✅ **Ticket Successfully Open Ho Gaya Hai!**\n\nAdmin jald hi aapse contact karega.", reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="Markdown")
            return

        elif current_state == 'WAITING_FUND_AMOUNT':
            if not text_val.isdigit() or float(text_val) <= 0:
                await update.message.reply_text("❌ Kripya sahi amount number me likhein (jaise: `100`).")
                return
            
            amount = float(text_val)
            del order_cache[user_id]

            upi_link = f"upi://pay?pa={MY_UPI_ID}&pn=VickyStore&am={amount}&cu=INR"
            qr_url = f"https://api.qrserver.com/v1/create-qr-code/?size=300x300&data={requests.utils.quote(upi_link)}"
            
            caption = (
                f"💳 **Paytm / UPI QR (Amount: ₹{amount})**\n\n"
                f"1️⃣ Is QR Code ko kisi bhi UPI app se scan karein. Amount auto **₹{amount}** set ho jayega.\n\n"
                f"2️⃣ Direct UPI ID:\n`{MY_UPI_ID}`\n\n"
                f"3️⃣ Payment ke baad Screenshot & UTR Admin ko bhejein taaki balance add ho jaye."
            )
            keyboard = [[InlineKeyboardButton("🔙 Main Menu", callback_data="main_menu")]]
            await update.message.reply_photo(photo=qr_url, caption=caption, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="Markdown")
            return

        elif current_state == 'WAITING_CUSTOM_QTY':
            if not text_val.isdigit():
                await update.message.reply_text("❌ Kripya number likhein.")
                return
            order_cache[user_id]['qty'] = text_val
            order_cache[user_id]['state'] = 'WAITING_LINK'
            await update.message.reply_text(f"✅ Quantity set: {text_val}\n\n🔗 Ab apna **Link** bhejein:")
            return

        elif current_state == 'WAITING_LINK':
            srv_id = state_info.get('srv_id')
            qty = int(state_info.get('qty'))
            link = text_val
            
            # Service ki current price nikalna
            services = call_smm_api({'action': 'services'})
            service_data = next((s for s in services if str(s.get('service')) == str(srv_id)), None)
            
            if not service_data:
                del order_cache[user_id]
                await update.message.reply_text("❌ Service fetch nahi ho saki. Dobara try karein.")
                return

            rate_per_k = float(service_data.get('rate', 0))
            total_price = round((rate_per_k * qty) / 1000, 2)
            
            # User ka balance check karna
            user_bal = get_user_balance(user_id)
            if user_bal < total_price:
                del order_cache[user_id]
                keyboard = [
                    [InlineKeyboardButton("🎒 ADD BALANCE NOW", callback_data="add_funds")],
                    [InlineKeyboardButton("🔙 Main Menu", callback_data="main_menu")]
                ]
                await update.message.reply_text(
                    f"❌ **Insufficient Balance!**\n\n"
                    f"💰 Is order ke liye aapko **₹{total_price}** chahiye, lekin aapke wallet me **₹{user_bal}** hain.\n\n"
                    f"Kripya pehle balance add karein:",
                    reply_markup=InlineKeyboardMarkup(keyboard),
                    parse_mode="Markdown"
                )
                return

            del order_cache[user_id]
            await update.message.reply_text("⏳ Processing Order & Deducting Balance...")

            # API Call to Kissmilegi (Original Rate kat jayega, profit bot owner ke paas rahega)
            res = call_smm_api({'action': 'add', 'service': srv_id, 'link': link, 'quantity': qty})
            
            if res and "order" in res:
                order_id = res['order']
                
                # Deduct balance from user wallet
                update_user_balance(user_id, -total_price)
                
                # Save order permanently in database
                save_order(user_id, order_id, srv_id, str(qty), link, total_price)

                await update.message.reply_text(
                    f"✅ **Order Successfully Placed!**\n\n"
                    f"🆔 **Order ID:** `{order_id}`\n"
                    f"🔹 **Service ID:** {srv_id}\n"
                    f"📊 **Quantity:** {qty}\n"
                    f"🔗 **Link:** {link}\n"
                    f"💸 **Deducted From Wallet:** ₹{total_price}", 
                    parse_mode="Markdown"
                )
            else:
                err = res.get("error", "Failed") if res else "API Error"
                await update.message.reply_text(f"❌ **Order Failed:** {err}")
            return

async def check_status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    args = context.args
    if not args:
        await update.message.reply_text("❌ Format: `/status ORDER_ID`", parse_mode="Markdown")
        return

    order_id = args[0]
    res = call_smm_api({'action': 'status', 'order': order_id})
    
    if res and "status" in res:
        msg = (
            f"📊 **Order Status:**\n\n"
            f"🆔 **Order ID:** `{order_id}`\n"
            f"📌 **Status:** {res.get('status')}\n"
            f"💰 **Charge:** ₹{res.get('charge')}\n"
            f"🔄 **Remains:** {res.get('remains')}"
        )
        await update.message.reply_text(msg, parse_mode="Markdown")
    else:
        await update.message.reply_text("❌ Order ID nahi mili ya API error aaya.")

async def search_service(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = " ".join(context.args).lower()
    if not query:
        await update.message.reply_text("❌ Example: `/search instagram`", parse_mode="Markdown")
        return

    services = call_smm_api({'action': 'services'})
    if not services:
        await update.message.reply_text("❌ Error fetching services.")
        return

    results = [s for s in services if query in s.get('name', '').lower() or query in s.get('category', '').lower()]
    if not results:
        await update.message.reply_text("❌ Koi service nahi mili.")
        return

    text = f"🔍 **Search Results for '{query}':**\n\n"
    for item in results[:8]:
        text += f"🆔 `{item.get('service')}` - {item.get('name')}\n💰 Rate: ₹{item.get('rate')}/k\n\n"

    await update.message.reply_text(text, parse_mode="Markdown")

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("status", check_status))
    app.add_handler(CommandHandler("search", search_service))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text_messages))
    
    print("Bot with Permanent SQLite DB & Wallet/Profit Deductor is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
