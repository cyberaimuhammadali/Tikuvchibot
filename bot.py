"""
🧵 TIKUVCHI BOT v2.0 — Milliy libos & To'y sarpolari
Admin panel + 7 bosqichli buyurtma kuzatuvi
Railway uchun ENV variables: BOT_TOKEN, ADMIN_ID
"""

import os
import json
import logging
from datetime import datetime
from telegram import (
    Update,
    ReplyKeyboardMarkup,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    ReplyKeyboardRemove,
)
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ConversationHandler,
    filters,
    ContextTypes,
)

# ==================== SOZLAMALAR ====================
BOT_TOKEN = os.environ.get("BOT_TOKEN", "SIZNING_TOKENINGIZ")
ADMIN_ID   = int(os.environ.get("ADMIN_ID", "123456789"))
ORDERS_FILE = "orders.json"

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# ==================== 7 BOSQICH TIZIMI ====================
BOSQICHLAR = {
    1: {
        "nomi": "📥 Qabul qilindi",
        "rang": "🟡",
        "maslahat": (
            "✅ *Buyurtma qabul qilindi!*\n\n"
            "📌 *Keyingi qadamlar:*\n"
            "• Mijoz bilan qo'ng'iroq qiling va o'lchovlarni tasdiqlang\n"
            "• Ko'krak — Bel — Son — Bo'y — Yelka kengligi\n"
            "• To'y sarpolari uchun: yana qo'lning uzunligini oling\n"
            "• Milliy libos uchun: yoqa turi va yeng kengligi muhim\n\n"
            "⏱ *Odatiy vaqt:* 1 kun"
        )
    },
    2: {
        "nomi": "🧵 Mato tanlash",
        "rang": "🟠",
        "maslahat": (
            "🧵 *Mato tanlash bosqichi*\n\n"
            "📌 *Tavsiya etiladigan matolar:*\n"
            "👗 *Milliy libos uchun:*\n"
            "• Atlas — eng mashhur, yaltiroq, bayramona\n"
            "• Adras — qo'lda to'qilgan, milliy naqsh\n"
            "• Banoras — ipak, to'y uchun ideal\n"
            "• Xan atlas — qimmat, sifatli\n\n"
            "👰 *To'y sarpolari uchun:*\n"
            "• Fatin + atlas kombinatsiyasi\n"
            "• Krep-satin — silliq, chiroyli oqadi\n"
            "• Organza — engil, shaffof qatlamlar uchun\n\n"
            "⚠️ Matoni 10-15% ko'proq oling — kesishda isrof bo'ladi!\n\n"
            "⏱ *Odatiy vaqt:* 1-2 kun"
        )
    },
    3: {
        "nomi": "✂️ Kesish",
        "rang": "🟠",
        "maslahat": (
            "✂️ *Kesish bosqichi*\n\n"
            "📌 *Muhim qoidalar:*\n"
            "• Matoni kesishdan oldin bir sutkaga yoying (cho'zilmasin)\n"
            "• Atlas/ipak matoni qog'oz ustiga yoyib kesingу\n"
            "• Naqshli mato (adras)da naqshni to'g'rilab kesingу\n\n"
            "👗 *Milliy libos uchun:*\n"
            "• Yoqa atrofiga 1.5 sm chok qoldiring\n"
            "• Yeng uchi uchun 2 sm qoldiring\n"
            "• Etakka 3-4 sm hem (podgibka)\n\n"
            "👰 *To'y libosi uchun:*\n"
            "• Fatin qatlamlarini alohida kesingу\n"
            "• Korsaj qismini qat-qat astar bilan kesingу\n\n"
            "⏱ *Odatiy vaqt:* 1 kun"
        )
    },
    4: {
        "nomi": "🪡 Tikish jarayoni",
        "rang": "🔵",
        "maslahat": (
            "🪡 *Tikish bosqichi*\n\n"
            "📌 *Professional maslahatlar:*\n"
            "• Atlas va ipak uchun — ingichka igna (70-80 nomеr)\n"
            "• Ip rengini matoga mos tanlang\n"
            "• Yengilroq matolar uchun ipni 2 qavatlamang\n\n"
            "🌸 *Kashta (zardozi) bor bo'lsa:*\n"
            "• Kashtani tikilgan libosga qo'shish osonroq\n"
            "• Avval eskizni qog'ozga tushing\n"
            "• Zardozi iplari: oltin/kumush rang keng qo'llaniladi\n\n"
            "👗 *Milliy ko'ylak uchun:*\n"
            "• Yoqa atrofini qo'lda tikish sifatli chiqadi\n"
            "• Yon tikuvlar kengini tekshiring\n\n"
            "⏱ *Odatiy vaqt:* 2-4 kun"
        )
    },
    5: {
        "nomi": "👗 Примерка (Qiyish)",
        "rang": "🔵",
        "maslahat": (
            "👗 *Примерка bosqichi*\n\n"
            "📌 *Mijozni chaqirishdan oldin:*\n"
            "• Asosiy tikuvlarni tekshiring\n"
            "• Simmetrikligini ko'zguda tekshiring\n"
            "• Fermuarni tekshiring (ishlayaptimi?)\n\n"
            "📋 *Примеrkada tekshiriladigan narsalar:*\n"
            "• Bel — bo'sh yoki qattiqmi?\n"
            "• Yelka chizig'i — to'g'rimi?\n"
            "• Uzunlik — kerakmi qisqartirish?\n"
            "• Yoqa — bo'yinga yaqinmi?\n"
            "• Ko'krak qismi — keng yoki tor?\n\n"
            "📲 *Mijozga SMS yuboring:*\n"
            "\"Assalomu alaykum! Buyurtmangiz примеркaga tayyor. Qulay vaqtda keling 🙏\"\n\n"
            "⏱ *Odatiy vaqt:* 1 kun"
        )
    },
    6: {
        "nomi": "✨ Bezak & Tugallash",
        "rang": "🟣",
        "maslahat": (
            "✨ *Bezak va tugallash bosqichi*\n\n"
            "📌 *Bezak turlari bo'yicha vaqt:*\n"
            "• 💎 Strazlar — 4-8 soat (yopishtirilsa tez)\n"
            "• 🪡 Qo'lda kashta — 2-5 kun\n"
            "• 🌸 Applikatsiya — 1-2 kun\n"
            "• 🎀 Bantlar va lentalar — 2-4 soat\n\n"
            "🎨 *Milliy libos uchun:*\n"
            "• Yoqa atrofi + yeng uchiga kashta eng chiroyli ko'rinadi\n"
            "• Oltin rangdagi zardozi atlas bilan ajoyib uyg'unlashadi\n\n"
            "👰 *To'y sarpolari uchun:*\n"
            "• Strazlarni fatin ustiga yopishtirsangiz — yaltiroq effekt\n"
            "• Gul bezaklarini bel qismida konsentratsiya qiling\n\n"
            "✅ *Tugallanganidan keyin:*\n"
            "• Barcha erkin iplarni qirqing\n"
            "• Libosni bug'li dazmol qiling\n"
            "• Paketga o'rang\n\n"
            "⏱ *Odatiy vaqt:* 1-3 kun"
        )
    },
    7: {
        "nomi": "✅ Tayyor & Topshirildi",
        "rang": "🟢",
        "maslahat": (
            "🎉 *Buyurtma tayyor!*\n\n"
            "📌 *Topshirishdan oldin:*\n"
            "• Yana bir bor butun libosni ko'zdan kechiring\n"
            "• Barcha bezaklar mahkammi? (tosh, bant)\n"
            "• Fermuarni sinab ko'ring\n"
            "• Chiroyli paketlang 🎀\n\n"
            "📲 *Mijozga xabar yuboring:*\n"
            "\"Assalomu alaykum! Buyurtmangiz tayyor! Istalgan vaqtda olib ketishingiz mumkin ✅\"\n\n"
            "💰 *To'lov eslatmasi:*\n"
            "• Oldindan to'langan summani tekshiring\n"
            "• Qolgan summani oling\n\n"
            "⭐ *Mijozdan fikr so'rang — keyingi buyurtma uchun!*\n\n"
            "⏱ *Buyurtma yakunlandi!* 🎊"
        )
    }
}

# ==================== DIZAYN VA BEZAK VARIANTLARI ====================
DIZAYNLAR = {
    "1": "👗 Milliy ko'ylak (atlas/adras)",
    "2": "🌸 Gullli milliy ko'ylak",
    "3": "✨ To'y kelin ko'ylagi",
    "4": "🎀 To'y sarpolasi (to'liq)",
    "5": "👚 Kundalik zamonaviy libos",
    "6": "🏆 Maxsus tantana libosi",
}

BEZAKLAR = {
    "1": "🪡 Kashta (zardozi)",
    "2": "💎 Toshlar (strazlar)",
    "3": "🎀 Bantlar va lentalar",
    "4": "🌸 Applikatsiya",
    "5": "✂️ Bezaksiz (soda)",
}

# ==================== JSON MA'LUMOTLAR BAZASI ====================

def orders_load() -> dict:
    try:
        with open(ORDERS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

def orders_save(orders: dict):
    with open(ORDERS_FILE, "w", encoding="utf-8") as f:
        json.dump(orders, f, ensure_ascii=False, indent=2)

def order_id_new() -> str:
    now = datetime.now()
    orders = orders_load()
    n = len(orders) + 1
    return f"{now.strftime('%d%m%y')}-{n:03d}"

# ==================== BOSQICHLAR (CONVERSATION) ====================
(
    ISM, TEL, RAZMER_TURI, RAZMER, BEZAK, BEZAK_CUSTOM,
    DIZAYN, DIZAYN_CUSTOM, DEDLAYN, NARX, TASDIQ
) = range(11)

# ==================== FORMATLOVCHI FUNKSIYALAR ====================

def order_text(data: dict, show_id=True) -> str:
    bezaklar = ", ".join(data.get("bezaklar", [])) or "Yo'q"
    bosqich_n = data.get("bosqich", 1)
    bosqich = BOSQICHLAR[bosqich_n]
    id_line = f"🔖 *ID:* `{data.get('order_id', '?')}`\n" if show_id else ""
    return (
        f"━━━━━━━━━━━━━━━━━━━━━━\n"
        f"{id_line}"
        f"👤 *Ism:* {data.get('ism', '-')}\n"
        f"📞 *Telefon:* {data.get('tel', '-')}\n"
        f"📏 *Razmer turi:* {data.get('razmer_turi', '-')}\n"
        f"📐 *Razmer:* {data.get('razmer', '-')}\n"
        f"🎨 *Dizayn:* {data.get('dizayn', '-')}\n"
        f"💫 *Bezaklar:* {bezaklar}\n"
        f"📅 *Qabul sanasi:* {data.get('sana', '-')}\n"
        f"⏰ *Dedlayn:* {data.get('dedlayn', '-')}\n"
        f"💰 *Narx:* {data.get('narx', '-')}\n"
        f"{bosqich['rang']} *Bosqich:* {bosqich['nomi']}\n"
        f"━━━━━━━━━━━━━━━━━━━━━━"
    )

def bosqich_progress(n: int) -> str:
    emojis = []
    for i in range(1, 8):
        b = BOSQICHLAR[i]
        if i < n:
            emojis.append("✅")
        elif i == n:
            emojis.append("👉")
        else:
            emojis.append("⬜")
    lines = [f"{emojis[i-1]} {BOSQICHLAR[i]['nomi']}" for i in range(1, 8)]
    return "\n".join(lines)

# ==================== BOSHLASH ====================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data.clear()
    keyboard = [
        ["🛍 Buyurtma berish"],
        ["📦 Buyurtmalarim", "❓ Yordam"],
        ["📞 Bog'lanish"]
    ]
    markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text(
        "👗 *Assalomu alaykum!*\n"
        "Milliy liboslar & To'y sarpolari — buyurtma botiga xush kelibsiz!\n\n"
        "Quyidagi tugmalardan birini tanlang 👇",
        reply_markup=markup,
        parse_mode="Markdown"
    )

async def yordam(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "❓ *Yordam*\n\n"
        "🛍 *Buyurtma berish* — yangi buyurtma qoldirish\n"
        "📦 *Buyurtmalarim* — buyurtma holatini bilish\n"
        "📞 *Bog'lanish* — tikuvchi bilan to'g'ridan-to'g'ri\n\n"
        "Savol bo'lsa: @tikuvchi_username ✉️",
        parse_mode="Markdown"
    )

async def boglanish(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📞 *Bog'lanish*\n\n"
        "📱 Telefon: +998 XX XXX XX XX\n"
        "💬 Telegram: @tikuvchi_username\n"
        "📍 Manzil: Toshkent sh.\n\n"
        "🕘 Ish vaqti: 9:00 — 19:00",
        parse_mode="Markdown"
    )

async def mening_buyurtmam(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = str(update.effective_user.id)
    orders = orders_load()
    user_orders = [o for o in orders.values() if str(o.get("user_id")) == uid]
    if not user_orders:
        await update.message.reply_text(
            "📦 Hozircha buyurtmangiz yo'q.\n\n🛍 Buyurtma berish uchun tugmani bosing!"
        )
        return
    last = sorted(user_orders, key=lambda x: x.get("sana", ""))[-1]
    bosqich_n = last.get("bosqich", 1)
    await update.message.reply_text(
        "📦 *Oxirgi buyurtmangiz:*\n\n" +
        order_text(last) + "\n\n" +
        f"📊 *Jarayon holati:*\n{bosqich_progress(bosqich_n)}",
        parse_mode="Markdown"
    )

# ==================== BUYURTMA JARAYONI ====================

async def buyurtma_boshlash(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["buyurtma"] = {"bezaklar": []}
    await update.message.reply_text(
        "🛍 *Buyurtma jarayoni boshlandi!*\n\n"
        "━━━━━━━━━━━━━━━━━━━━━━\n"
        "👤 *1-qadam:* Ismingizni kiriting\n"
        "_(Masalan: Nilufar Karimova)_",
        reply_markup=ReplyKeyboardRemove(),
        parse_mode="Markdown"
    )
    return ISM

async def ism_olish(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["buyurtma"]["ism"] = update.message.text.strip()
    await update.message.reply_text(
        "✅ Ism saqlandi!\n\n"
        "📞 *2-qadam:* Telefon raqamingizni kiriting\n"
        "_(Masalan: +998901234567)_",
        parse_mode="Markdown"
    )
    return TEL

async def tel_olish(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.contact:
        tel = update.message.contact.phone_number
    else:
        tel = update.message.text.strip()
    context.user_data["buyurtma"]["tel"] = tel
    keyboard = [
        [InlineKeyboardButton("📏 Standart (XS/S/M/L/XL/XXL)", callback_data="razmer_standart")],
        [InlineKeyboardButton("📐 O'lchamli (sm hisobida)", callback_data="razmer_olchamli")],
    ]
    await update.message.reply_text(
        "✅ Telefon saqlandi!\n\n📏 *3-qadam:* Razmer turini tanlang",
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode="Markdown"
    )
    return RAZMER_TURI

async def razmer_turi_tanlash(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    if query.data == "razmer_standart":
        context.user_data["buyurtma"]["razmer_turi"] = "Standart"
        keyboard = [
            [InlineKeyboardButton("XS", callback_data="r_XS"),
             InlineKeyboardButton("S",  callback_data="r_S"),
             InlineKeyboardButton("M",  callback_data="r_M")],
            [InlineKeyboardButton("L",  callback_data="r_L"),
             InlineKeyboardButton("XL", callback_data="r_XL"),
             InlineKeyboardButton("XXL",callback_data="r_XXL")],
        ]
        await query.edit_message_text(
            "📏 *4-qadam:* Razmeringizni tanlang",
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode="Markdown"
        )
        return RAZMER
    else:
        context.user_data["buyurtma"]["razmer_turi"] = "O'lchamli (sm)"
        await query.edit_message_text(
            "📐 *4-qadam:* O'lchamlaringizni kiriting\n\n"
            "_Ko'krak — Bel — Son — Bo'y (sm)\n"
            "Masalan: 88-68-96-165_",
            parse_mode="Markdown"
        )
        return RAZMER

async def razmer_standart_tanlash(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    context.user_data["buyurtma"]["razmer"] = query.data.replace("r_", "")
    return await bezak_savol(query)

async def razmer_text_olish(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["buyurtma"]["razmer"] = update.message.text.strip()
    return await bezak_savol(update.message)

async def bezak_savol(msg):
    keyboard = [
        [InlineKeyboardButton("🪡 Kashta (zardozi)", callback_data="b_1"),
         InlineKeyboardButton("💎 Strazlar",         callback_data="b_2")],
        [InlineKeyboardButton("🎀 Bantlar",          callback_data="b_3"),
         InlineKeyboardButton("🌸 Applikatsiya",     callback_data="b_4")],
        [InlineKeyboardButton("✂️ Bezaksiz",          callback_data="b_5")],
        [InlineKeyboardButton("✏️ O'zim yozaman",    callback_data="b_custom")],
        [InlineKeyboardButton("✅ Tayyor, davom etish", callback_data="bezak_done")],
    ]
    text = "✅ Razmer saqlandi!\n\n💫 *5-qadam:* Bezaklarni tanlang _(bir nechta mumkin)_"
    if hasattr(msg, 'edit_message_text'):
        await msg.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="Markdown")
    else:
        await msg.reply_text(text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="Markdown")
    return BEZAK

async def bezak_tanlash(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    if query.data == "bezak_done":
        if not context.user_data["buyurtma"]["bezaklar"]:
            context.user_data["buyurtma"]["bezaklar"] = ["Bezaksiz"]
        return await dizayn_savol(query)
    if query.data == "b_custom":
        await query.edit_message_text(
            "✏️ Bezak haqida o'zingiz yozing:\n_(Masalan: Yoqa atrofiga oltin kashta)_",
            parse_mode="Markdown"
        )
        return BEZAK_CUSTOM
    kod = query.data.replace("b_", "")
    bezak = BEZAKLAR.get(kod, "")
    bezaklar = context.user_data["buyurtma"]["bezaklar"]
    if bezak not in bezaklar:
        bezaklar.append(bezak)
    tanlangan = ", ".join(bezaklar)
    keyboard = [
        [InlineKeyboardButton("🪡 Kashta",       callback_data="b_1"),
         InlineKeyboardButton("💎 Strazlar",     callback_data="b_2")],
        [InlineKeyboardButton("🎀 Bantlar",      callback_data="b_3"),
         InlineKeyboardButton("🌸 Applikatsiya", callback_data="b_4")],
        [InlineKeyboardButton("✂️ Bezaksiz",      callback_data="b_5")],
        [InlineKeyboardButton("✏️ O'zim yozaman", callback_data="b_custom")],
        [InlineKeyboardButton("✅ Tayyor, davom etish", callback_data="bezak_done")],
    ]
    await query.edit_message_text(
        f"✅ *Tanlangan:* {tanlangan}\n\nYana qo'shasizmi yoki davom etasizmi?",
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode="Markdown"
    )
    return BEZAK

async def bezak_custom_olish(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["buyurtma"]["bezaklar"].append(f"✏️ {update.message.text.strip()}")
    return await dizayn_savol(update.message)

async def dizayn_savol(msg):
    keyboard = [
        [InlineKeyboardButton("👗 Milliy ko'ylak",     callback_data="d_1"),
         InlineKeyboardButton("🌸 Gulli milliy",       callback_data="d_2")],
        [InlineKeyboardButton("✨ Kelin ko'ylagi",     callback_data="d_3"),
         InlineKeyboardButton("🎀 To'y sarpolasi",     callback_data="d_4")],
        [InlineKeyboardButton("👚 Kundalik libos",     callback_data="d_5"),
         InlineKeyboardButton("🏆 Tantana libosi",     callback_data="d_6")],
        [InlineKeyboardButton("✏️ O'z dizaynim bor",  callback_data="d_custom")],
    ]
    text = "🎨 *6-qadam:* Libos turini tanlang"
    if hasattr(msg, 'edit_message_text'):
        await msg.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="Markdown")
    else:
        await msg.reply_text(text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="Markdown")
    return DIZAYN

async def dizayn_tanlash(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    if query.data == "d_custom":
        await query.edit_message_text(
            "✏️ Dizayningizni tasvirlab bering yoki rasm yuboring:",
            parse_mode="Markdown"
        )
        return DIZAYN_CUSTOM
    kod = query.data.replace("d_", "")
    context.user_data["buyurtma"]["dizayn"] = DIZAYNLAR.get(kod, "")
    context.user_data["buyurtma"]["sana"] = datetime.now().strftime("%d.%m.%Y")
    await query.edit_message_text(
        f"✅ *{context.user_data['buyurtma']['dizayn']}* tanlandi!\n\n"
        "⏰ *7-qadam:* Tayyor bo'lish sanasini (deadlineni) kiriting\n"
        "_(Masalan: 25.04.2025 yoki 2 hafta ichida)_",
        parse_mode="Markdown"
    )
    return DEDLAYN

async def dizayn_custom_olish(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.photo:
        context.user_data["buyurtma"]["dizayn"] = "✏️ Maxsus dizayn (rasm yuborildi)"
        context.user_data["buyurtma"]["dizayn_photo_id"] = update.message.photo[-1].file_id
    else:
        context.user_data["buyurtma"]["dizayn"] = f"✏️ {update.message.text.strip()}"
    context.user_data["buyurtma"]["sana"] = datetime.now().strftime("%d.%m.%Y")
    await update.message.reply_text(
        "✅ Dizayn saqlandi!\n\n"
        "⏰ *7-qadam:* Deadlineni kiriting\n_(Masalan: 25.04.2025)_",
        parse_mode="Markdown"
    )
    return DEDLAYN

async def dedlayn_olish(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["buyurtma"]["dedlayn"] = update.message.text.strip()
    await update.message.reply_text(
        "✅ Dedlayn saqlandi!\n\n"
        "💰 *8-qadam:* Narxni kiriting\n_(Masalan: 350,000 so'm yoki Kelishiladi)_",
        parse_mode="Markdown"
    )
    return NARX

async def narx_olish(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["buyurtma"]["narx"] = update.message.text.strip()
    buyurtma = context.user_data["buyurtma"]
    keyboard = [
        [InlineKeyboardButton("✅ Tasdiqlash",       callback_data="tasdiq_ha"),
         InlineKeyboardButton("✏️ Qayta to'ldirish", callback_data="tasdiq_yoq")]
    ]
    await update.message.reply_text(
        "📋 *BUYURTMANGIZNI TEKSHIRING:*\n\n" + order_text(buyurtma, show_id=False) +
        "\n\nMa'lumotlar to'g'rimi?",
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode="Markdown"
    )
    return TASDIQ

async def tasdiq(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    if query.data == "tasdiq_ha":
        buyurtma = context.user_data["buyurtma"]
        buyurtma["bosqich"]  = 1
        buyurtma["user_id"]  = query.from_user.id
        buyurtma["username"] = query.from_user.username or ""
        buyurtma["order_id"] = order_id_new()

        orders = orders_load()
        orders[buyurtma["order_id"]] = buyurtma
        orders_save(orders)

        # Adminga xabar
        try:
            admin_msg = (
                f"🔔 *YANGI BUYURTMA!*\n\n" + order_text(buyurtma) +
                f"\n\n💬 *Telegram:* @{buyurtma['username'] or 'username yo`q'}"
                f"\n🆔 *User ID:* `{query.from_user.id}`"
            )
            keyboard_admin = [
                [InlineKeyboardButton("📋 Batafsil ko'rish", callback_data=f"admin_view_{buyurtma['order_id']}")]
            ]
            await context.bot.send_message(
                ADMIN_ID, admin_msg,
                parse_mode="Markdown",
                reply_markup=InlineKeyboardMarkup(keyboard_admin)
            )
            if buyurtma.get("dizayn_photo_id"):
                await context.bot.send_photo(
                    ADMIN_ID,
                    photo=buyurtma["dizayn_photo_id"],
                    caption=f"🖼 {buyurtma['order_id']} buyurtma dizayni"
                )
        except Exception as e:
            logger.error(f"Admin xabar xatosi: {e}")

        keyboard = [["🛍 Yangi buyurtma"], ["📦 Buyurtmalarim", "📞 Bog'lanish"]]
        await query.edit_message_text(
            f"✅ *Buyurtmangiz qabul qilindi!*\n\n"
            f"🔖 Buyurtma ID: `{buyurtma['order_id']}`\n\n"
            f"📲 Tikuvchi tez orada siz bilan bog'lanadi.\n"
            f"🙏 Ishonganingiz uchun rahmat!",
            parse_mode="Markdown"
        )
        await context.bot.send_message(
            query.from_user.id,
            "Bosh menyuga qaytish 👇",
            reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
        )
    else:
        keyboard = [["🛍 Buyurtma berish"]]
        await query.edit_message_text("✏️ Buyurtma bekor qilindi. Qaytadan to'ldiring 👇")
        await context.bot.send_message(
            query.from_user.id, "Qayta boshlash:",
            reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
        )
    return ConversationHandler.END

async def bekor_qilish(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [["🛍 Buyurtma berish"], ["📦 Buyurtmalarim", "📞 Bog'lanish"]]
    await update.message.reply_text(
        "❌ Bekor qilindi. Bosh menyu 👇",
        reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    )
    return ConversationHandler.END

# ==================== ADMIN PANEL ====================

async def admin_panel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        await update.message.reply_text("❌ Ruxsat yo'q.")
        return
    orders = orders_load()
    if not orders:
        await update.message.reply_text("📭 Hozircha buyurtmalar yo'q.")
        return

    # Bosqich bo'yicha saralash
    active = [o for o in orders.values() if o.get("bosqich", 1) < 7]
    done   = [o for o in orders.values() if o.get("bosqich", 1) == 7]

    text = f"🗂 *ADMIN PANEL*\n\n📊 Jami: {len(orders)} ta\n✅ Tayyor: {len(done)} ta\n🔄 Jarayonda: {len(active)} ta\n\nBuyurtmani tanlang 👇"
    sorted_orders = sorted(orders.values(), key=lambda x: x.get("bosqich", 1))
    buttons = []
    for o in sorted_orders[:20]:
        b = o.get("bosqich", 1)
        rang = BOSQICHLAR[b]["rang"]
        label = f"{rang} {o['order_id']} — {o.get('ism','?')[:12]}"
        buttons.append([InlineKeyboardButton(label, callback_data=f"admin_view_{o['order_id']}")])
    buttons.append([InlineKeyboardButton("📊 Statistika", callback_data="admin_stats")])
    await update.message.reply_text(
        text,
        reply_markup=InlineKeyboardMarkup(buttons),
        parse_mode="Markdown"
    )

async def admin_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    if query.from_user.id != ADMIN_ID:
        await query.answer("❌ Ruxsat yo'q!", show_alert=True)
        return
    await query.answer()
    data = query.data

    # === STATISTIKA ===
    if data == "admin_stats":
        orders = orders_load()
        stats = {i: 0 for i in range(1, 8)}
        for o in orders.values():
            b = o.get("bosqich", 1)
            stats[b] = stats.get(b, 0) + 1
        text = "📊 *STATISTIKA*\n\n"
        for i in range(1, 8):
            text += f"{BOSQICHLAR[i]['rang']} {BOSQICHLAR[i]['nomi']}: {stats[i]} ta\n"
        text += f"\n📦 *Jami:* {len(orders)} ta buyurtma"
        await query.edit_message_text(text, parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⬅️ Ortga", callback_data="admin_back")]]))
        return

    # === ORTGA ===
    if data == "admin_back":
        orders = orders_load()
        sorted_orders = sorted(orders.values(), key=lambda x: x.get("bosqich", 1))
        buttons = []
        for o in sorted_orders[:20]:
            b = o.get("bosqich", 1)
            rang = BOSQICHLAR[b]["rang"]
            label = f"{rang} {o['order_id']} — {o.get('ism','?')[:12]}"
            buttons.append([InlineKeyboardButton(label, callback_data=f"admin_view_{o['order_id']}")])
        buttons.append([InlineKeyboardButton("📊 Statistika", callback_data="admin_stats")])
        await query.edit_message_text(
            f"🗂 *ADMIN PANEL* — Buyurtmani tanlang 👇",
            reply_markup=InlineKeyboardMarkup(buttons),
            parse_mode="Markdown"
        )
        return

    # === BUYURTMA KO'RISH ===
    if data.startswith("admin_view_"):
        order_id = data.replace("admin_view_", "")
        orders = orders_load()
        o = orders.get(order_id)
        if not o:
            await query.edit_message_text("❌ Buyurtma topilmadi.")
            return
        bosqich_n = o.get("bosqich", 1)
        text = order_text(o) + "\n\n📊 *Jarayon:*\n" + bosqich_progress(bosqich_n)
        keyboard = []
        # Bosqich almashtirish tugmalari
        if bosqich_n < 7:
            keyboard.append([
                InlineKeyboardButton(
                    f"➡️ Keyingi bosqich: {BOSQICHLAR[bosqich_n+1]['nomi']}",
                    callback_data=f"admin_next_{order_id}"
                )
            ])
        if bosqich_n > 1:
            keyboard.append([
                InlineKeyboardButton("⬅️ Oldingi bosqichga", callback_data=f"admin_prev_{order_id}")
            ])
        keyboard.append([
            InlineKeyboardButton("💡 Maslahat ko'rish", callback_data=f"admin_tip_{order_id}"),
            InlineKeyboardButton("📲 Mijozga xabar", callback_data=f"admin_notify_{order_id}"),
        ])
        keyboard.append([InlineKeyboardButton("⬅️ Ro'yxatga qaytish", callback_data="admin_back")])
        await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="Markdown")
        return

    # === KEYINGI BOSQICH ===
    if data.startswith("admin_next_"):
        order_id = data.replace("admin_next_", "")
        orders = orders_load()
        o = orders.get(order_id)
        if not o:
            return
        old_b = o.get("bosqich", 1)
        if old_b < 7:
            o["bosqich"] = old_b + 1
            orders[order_id] = o
            orders_save(orders)
            new_b = o["bosqich"]
            # Mijozga avtomatik xabar
            try:
                user_msg = (
                    f"📲 *Buyurtmangiz holati yangilandi!*\n\n"
                    f"🔖 ID: `{order_id}`\n"
                    f"{BOSQICHLAR[new_b]['rang']} *Yangi bosqich:* {BOSQICHLAR[new_b]['nomi']}\n\n"
                    f"📊 Jarayon:\n{bosqich_progress(new_b)}"
                )
                await context.bot.send_message(o["user_id"], user_msg, parse_mode="Markdown")
            except Exception as e:
                logger.error(f"Mijozga xabar xatosi: {e}")
            # Adminga maslahat
            text = (
                f"✅ *Bosqich o'zgartirildi!*\n\n"
                f"🔖 {order_id} | {o.get('ism','?')}\n"
                f"{BOSQICHLAR[old_b]['rang']} {BOSQICHLAR[old_b]['nomi']} → "
                f"{BOSQICHLAR[new_b]['rang']} {BOSQICHLAR[new_b]['nomi']}\n\n"
                f"📊 *Jarayon:*\n{bosqich_progress(new_b)}\n\n"
                + BOSQICHLAR[new_b]["maslahat"]
            )
            keyboard = []
            if new_b < 7:
                keyboard.append([InlineKeyboardButton(
                    f"➡️ Keyingi: {BOSQICHLAR[new_b+1]['nomi']}",
                    callback_data=f"admin_next_{order_id}"
                )])
            keyboard.append([
                InlineKeyboardButton("📲 Mijozga xabar", callback_data=f"admin_notify_{order_id}"),
            ])
            keyboard.append([InlineKeyboardButton("⬅️ Ro'yxatga", callback_data="admin_back")])
            await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="Markdown")
        return

    # === OLDINGI BOSQICH ===
    if data.startswith("admin_prev_"):
        order_id = data.replace("admin_prev_", "")
        orders = orders_load()
        o = orders.get(order_id)
        if not o:
            return
        old_b = o.get("bosqich", 1)
        if old_b > 1:
            o["bosqich"] = old_b - 1
            orders[order_id] = o
            orders_save(orders)
        await query.edit_message_text(
            f"✅ Bosqich {old_b} → {o['bosqich']} ga qaytarildi.\n\n" +
            bosqich_progress(o["bosqich"]),
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("📋 Buyurtmaga qaytish", callback_data=f"admin_view_{order_id}")]
            ]),
            parse_mode="Markdown"
        )
        return

    # === MASLAHAT KO'RISH ===
    if data.startswith("admin_tip_"):
        order_id = data.replace("admin_tip_", "")
        orders = orders_load()
        o = orders.get(order_id)
        if not o:
            return
        bosqich_n = o.get("bosqich", 1)
        text = f"💡 *{BOSQICHLAR[bosqich_n]['nomi']} uchun maslahat:*\n\n" + BOSQICHLAR[bosqich_n]["maslahat"]
        keyboard = [[InlineKeyboardButton("⬅️ Buyurtmaga qaytish", callback_data=f"admin_view_{order_id}")]]
        await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="Markdown")
        return

    # === MIJOZGA XABAR ===
    if data.startswith("admin_notify_"):
        order_id = data.replace("admin_notify_", "")
        orders = orders_load()
        o = orders.get(order_id)
        if not o:
            return
        bosqich_n = o.get("bosqich", 1)
        # Bosqichga mos tayyor xabar variantlari
        xabarlar = {
            1: f"Assalomu alaykum, {o.get('ism','').split()[0] if o.get('ism') else 'hurmatli mijoz'}! Buyurtmangiz qabul qilindi ✅",
            2: f"Assalomu alaykum! Matoni tanlash bosqichiga keldik. Siz bilan bog'lanaman 📞",
            3: f"Buyurtmangiz mato kesish bosqichida ✂️",
            4: f"Buyurtmangiz tikish jarayonida 🪡 Tez orada tayyor bo'ladi!",
            5: f"Assalomu alaykum! Примерkaga kelishingizni so'raymiz 👗 Qulay vaqtingizni ayting.",
            6: f"Buyurtmangizga bezaklar qo'shilmoqda ✨ Deyarli tayyor!",
            7: f"🎉 Buyurtmangiz tayyor! Istalgan vaqtda olib ketishingiz mumkin.",
        }
        default_msg = xabarlar.get(bosqich_n, "Buyurtmangiz holati yangilandi.")
        try:
            await context.bot.send_message(
                o["user_id"],
                f"📲 *Tikuvchidan xabar:*\n\n{default_msg}",
                parse_mode="Markdown"
            )
            await query.answer("✅ Xabar yuborildi!", show_alert=True)
        except Exception as e:
            await query.answer(f"❌ Xabar yuborilmadi: {e}", show_alert=True)
        return

async def admin_orders_list(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Barcha faol buyurtmalar"""
    if update.effective_user.id != ADMIN_ID:
        return
    await admin_panel(update, context)

# ==================== ASOSIY ====================

def main():
    app = Application.builder().token(BOT_TOKEN).build()

    conv = ConversationHandler(
        entry_points=[
            MessageHandler(filters.Regex("^🛍 (Buyurtma berish|Yangi buyurtma)$"), buyurtma_boshlash)
        ],
        states={
            ISM:        [MessageHandler(filters.TEXT & ~filters.COMMAND, ism_olish)],
            TEL:        [MessageHandler(filters.CONTACT | (filters.TEXT & ~filters.COMMAND), tel_olish)],
            RAZMER_TURI:[CallbackQueryHandler(razmer_turi_tanlash, pattern="^razmer_")],
            RAZMER:     [
                CallbackQueryHandler(razmer_standart_tanlash, pattern="^r_"),
                MessageHandler(filters.TEXT & ~filters.COMMAND, razmer_text_olish),
            ],
            BEZAK:      [CallbackQueryHandler(bezak_tanlash, pattern="^(b_|bezak_done)")],
            BEZAK_CUSTOM:[MessageHandler(filters.TEXT & ~filters.COMMAND, bezak_custom_olish)],
            DIZAYN:     [CallbackQueryHandler(dizayn_tanlash, pattern="^d_")],
            DIZAYN_CUSTOM:[MessageHandler(filters.PHOTO | (filters.TEXT & ~filters.COMMAND), dizayn_custom_olish)],
            DEDLAYN:    [MessageHandler(filters.TEXT & ~filters.COMMAND, dedlayn_olish)],
            NARX:       [MessageHandler(filters.TEXT & ~filters.COMMAND, narx_olish)],
            TASDIQ:     [CallbackQueryHandler(tasdiq, pattern="^tasdiq_")],
        },
        fallbacks=[
            CommandHandler("bekor", bekor_qilish),
        ],
    )

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("admin", admin_panel))
    app.add_handler(CommandHandler("buyurtmalar", admin_orders_list))
    app.add_handler(conv)
    app.add_handler(CallbackQueryHandler(admin_callback, pattern="^admin_"))
    app.add_handler(MessageHandler(filters.Regex("^📦 Buyurtmalarim$"), mening_buyurtmam))
    app.add_handler(MessageHandler(filters.Regex("^❓ Yordam$"), yordam))
    app.add_handler(MessageHandler(filters.Regex("^📞 Bog'lanish$"), boglanish))

    print("🤖 Tikuvchi Bot v2.0 ishga tushdi!")
    app.run_polling()

if __name__ == "__main__":
    main()
