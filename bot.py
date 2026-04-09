"""
🧵 TIKUVCHI BOT - Buyurtma qabul qilish boti
Yaratuvchi: Sizning shaxsiy yordamchingiz
"""

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
BOT_TOKEN = "SIZNING_BOT_TOKENINGIZ"   # @BotFather dan oling
ADMIN_ID = 123456789                    # Sizning Telegram ID raqamingiz

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# ==================== BOSQICHLAR ====================
(
    ISM, TEL, RAZMER_TURI, RAZMER, BEZAK, BEZAK_CUSTOM,
    DIZAYN, DIZAYN_CUSTOM, SANA, DEDLAYN, NARX, TASDIQ
) = range(12)

# ==================== DIZAYN VARIANTLARI ====================
DIZAYNLAR = {
    "1": "👗 Klassik ko'ylak",
    "2": "🌸 Gulли ko'ylak",
    "3": "✨ Ziyofat libosi",
    "4": "👚 Kundalik libos",
    "5": "💍 To'y libosi",
    "6": "🎀 Bolalar libosi",
}

BEZAKLAR = {
    "1": "🪡 Kashta (вышивка)",
    "2": "💎 Toshlar (стразы)",
    "3": "🎀 Bantlar",
    "4": "🌸 Applikatsiya",
    "5": "✂️ Bezaksiz (soda)",
}

# ==================== YORDAMCHI FUNKSIYALAR ====================

def order_text(data: dict) -> str:
    """Buyurtma matnini chiroyli formatlash"""
    bezaklar = ", ".join(data.get("bezaklar", []))
    return (
        f"━━━━━━━━━━━━━━━━━━━━━━\n"
        f"📋 *YANGI BUYURTMA*\n"
        f"━━━━━━━━━━━━━━━━━━━━━━\n"
        f"👤 *Ism:* {data.get('ism', '-')}\n"
        f"📞 *Telefon:* {data.get('tel', '-')}\n"
        f"📏 *Razmer turi:* {data.get('razmer_turi', '-')}\n"
        f"📐 *Razmer:* {data.get('razmer', '-')}\n"
        f"🎨 *Dizayn:* {data.get('dizayn', '-')}\n"
        f"💫 *Bezaklar:* {bezaklar or 'Yo`q'}\n"
        f"📅 *Buyurtma sanasi:* {data.get('sana', '-')}\n"
        f"⏰ *Dedlayn:* {data.get('dedlayn', '-')}\n"
        f"💰 *Narx:* {data.get('narx', '-')}\n"
        f"━━━━━━━━━━━━━━━━━━━━━━"
    )

# ==================== BOSHLASH ====================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data.clear()
    keyboard = [
        ["🛍 Buyurtma berish"],
        ["📦 Buyurtmalarim", "❓ Yordam"],
        ["📞 Bog'lanish"]
    ]
    await update.message.reply_text(
        "👗 *Assalomu alaykum! Tikuvchi botiga xush kelibsiz!*\n\n"
        "Men sizga qulay tarzda buyurtma berishga yordam beraman.\n"
        "Quyidagi tugmalardan birini tanlang 👇",
        reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True),
        parse_mode="Markdown"
    )

# ==================== YORDAM ====================

async def yordam(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "❓ *Yordam*\n\n"
        "🛍 *Buyurtma berish* — yangi buyurtma qoldirish\n"
        "📦 *Buyurtmalarim* — oxirgi buyurtmangiz\n"
        "📞 *Bog'lanish* — tikuvchi bilan to'g'ridan-to'g'ri bog'lanish\n\n"
        "Savol bo'lsa: @tikuvchi_username ga yozing ✉️",
        parse_mode="Markdown"
    )

async def boglanish(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📞 *Bog'lanish*\n\n"
        "📱 Telefon: +998 XX XXX XX XX\n"
        "💬 Telegram: @tikuvchi_username\n"
        "📍 Manzil: Toshkent sh., ...\n\n"
        "Ish vaqti: 9:00 — 19:00 🕘",
        parse_mode="Markdown"
    )

async def mening_buyurtmam(update: Update, context: ContextTypes.DEFAULT_TYPE):
    last = context.user_data.get("last_order")
    if last:
        await update.message.reply_text(
            "📦 *Oxirgi buyurtmangiz:*\n\n" + order_text(last),
            parse_mode="Markdown"
        )
    else:
        await update.message.reply_text(
            "📦 Hozircha buyurtmangiz yo'q.\n\n"
            "🛍 Buyurtma berish uchun tugmani bosing!",
            parse_mode="Markdown"
        )

# ==================== BUYURTMA JARAYONI ====================

async def buyurtma_boshlash(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["buyurtma"] = {"bezaklar": []}
    await update.message.reply_text(
        "🛍 *Buyurtma jarayoni boshlandi!*\n\n"
        "Qadamma-qadam ma'lumot to'ldiramiz.\n\n"
        "━━━━━━━━━━━━━━━━━━━━━━\n"
        "👤 *1-qadam:* Ismingizni kiriting\n"
        "_(Masalan: Nilufar Karimova)_",
        reply_markup=ReplyKeyboardRemove(),
        parse_mode="Markdown"
    )
    return ISM

async def ism_olish(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["buyurtma"]["ism"] = update.message.text.strip()
    keyboard = [[InlineKeyboardButton("📱 Raqamimni yuborish", callback_data="tel_skip")]]
    await update.message.reply_text(
        "✅ Ism saqlandi!\n\n"
        "📞 *2-qadam:* Telefon raqamingizni kiriting\n"
        "_(Masalan: +998901234567)_\n\n"
        "_Yoki pastdagi tugma orqali avtomatik yuboring:_",
        reply_markup=InlineKeyboardMarkup(keyboard),
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
        "✅ Telefon saqlandi!\n\n"
        "📏 *3-qadam:* Razmer turini tanlang",
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode="Markdown"
    )
    return RAZMER_TURI

async def tel_skip(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    keyboard = [
        [InlineKeyboardButton("📏 Standart (XS/S/M/L/XL/XXL)", callback_data="razmer_standart")],
        [InlineKeyboardButton("📐 O'lchamli (sm hisobida)", callback_data="razmer_olchamli")],
    ]
    await query.edit_message_text(
        "📞 Telefon raqamingizni matn ko'rinishida yozing:\n"
        "_(Masalan: +998901234567)_",
        parse_mode="Markdown"
    )
    return TEL

async def razmer_turi_tanlash(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    tur = query.data

    if tur == "razmer_standart":
        context.user_data["buyurtma"]["razmer_turi"] = "Standart"
        keyboard = [
            [InlineKeyboardButton("XS", callback_data="r_XS"),
             InlineKeyboardButton("S", callback_data="r_S"),
             InlineKeyboardButton("M", callback_data="r_M")],
            [InlineKeyboardButton("L", callback_data="r_L"),
             InlineKeyboardButton("XL", callback_data="r_XL"),
             InlineKeyboardButton("XXL", callback_data="r_XXL")],
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
            "_Ko'krak — Bel — Son (sm)\n"
            "Masalan: 88-72-96_",
            parse_mode="Markdown"
        )
        return RAZMER

async def razmer_standart_tanlash(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    razmer = query.data.replace("r_", "")
    context.user_data["buyurtma"]["razmer"] = razmer
    return await bezak_savol(query)

async def razmer_text_olish(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["buyurtma"]["razmer"] = update.message.text.strip()
    return await bezak_savol(update.message)

async def bezak_savol(msg):
    keyboard = [
        [InlineKeyboardButton("🪡 Kashta", callback_data="b_1"),
         InlineKeyboardButton("💎 Toshlar", callback_data="b_2")],
        [InlineKeyboardButton("🎀 Bantlar", callback_data="b_3"),
         InlineKeyboardButton("🌸 Applikatsiya", callback_data="b_4")],
        [InlineKeyboardButton("✂️ Bezaksiz", callback_data="b_5")],
        [InlineKeyboardButton("✏️ O'zim yozaman", callback_data="b_custom")],
        [InlineKeyboardButton("✅ Tayyor, davom etish", callback_data="bezak_done")],
    ]
    text = (
        "✅ Razmer saqlandi!\n\n"
        "💫 *5-qadam:* Bezaklarni tanlang\n"
        "_(Bir nechta tanlash mumkin)_"
    )
    if hasattr(msg, 'edit_message_text'):
        await msg.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="Markdown")
    else:
        await msg.reply_text(text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="Markdown")
    return BEZAK

async def bezak_tanlash(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "bezak_done":
        bezaklar = context.user_data["buyurtma"].get("bezaklar", [])
        if not bezaklar:
            context.user_data["buyurtma"]["bezaklar"] = ["Bezaksiz"]
        return await dizayn_savol(query)

    if query.data == "b_custom":
        await query.edit_message_text(
            "✏️ Bezak haqida o'zingiz yozing:\n"
            "_(Masalan: Yoqa atrofiga oltin kashta)_",
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
        [InlineKeyboardButton("🪡 Kashta", callback_data="b_1"),
         InlineKeyboardButton("💎 Toshlar", callback_data="b_2")],
        [InlineKeyboardButton("🎀 Bantlar", callback_data="b_3"),
         InlineKeyboardButton("🌸 Applikatsiya", callback_data="b_4")],
        [InlineKeyboardButton("✂️ Bezaksiz", callback_data="b_5")],
        [InlineKeyboardButton("✏️ O'zim yozaman", callback_data="b_custom")],
        [InlineKeyboardButton("✅ Tayyor, davom etish", callback_data="bezak_done")],
    ]
    await query.edit_message_text(
        f"✅ *Tanlangan:* {tanlangan}\n\n"
        f"💫 Yana bezak qo'shasizmi yoki davom etasizmi?",
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode="Markdown"
    )
    return BEZAK

async def bezak_custom_olish(update: Update, context: ContextTypes.DEFAULT_TYPE):
    matn = update.message.text.strip()
    context.user_data["buyurtma"]["bezaklar"].append(f"✏️ {matn}")
    return await dizayn_savol(update.message)

async def dizayn_savol(msg):
    keyboard = [
        [InlineKeyboardButton("👗 Klassik ko'ylak", callback_data="d_1"),
         InlineKeyboardButton("🌸 Gulли ko'ylak", callback_data="d_2")],
        [InlineKeyboardButton("✨ Ziyofat libosi", callback_data="d_3"),
         InlineKeyboardButton("👚 Kundalik libos", callback_data="d_4")],
        [InlineKeyboardButton("💍 To'y libosi", callback_data="d_5"),
         InlineKeyboardButton("🎀 Bolalar libosi", callback_data="d_6")],
        [InlineKeyboardButton("✏️ O'z dizaynim bor", callback_data="d_custom")],
    ]
    text = "🎨 *6-qadam:* Dizayn turini tanlang"
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
            "✏️ Dizayningizni tasvirlab bering yoki rasm yuboring:\n"
            "_(Keyingi qadamda rasm yuborish imkoni ham bo'ladi)_",
            parse_mode="Markdown"
        )
        return DIZAYN_CUSTOM

    kod = query.data.replace("d_", "")
    context.user_data["buyurtma"]["dizayn"] = DIZAYNLAR.get(kod, "")
    await query.edit_message_text(
        f"✅ Dizayn tanlandi: *{context.user_data['buyurtma']['dizayn']}*\n\n"
        f"📅 *7-qadam:* Bugungi sana avtomatik saqlanmoqda\n\n"
        f"⏰ *8-qadam:* Tayyor bo'lish *deadlineni* kiriting\n"
        f"_(Masalan: 25.04.2025 yoki 2 hafta)_",
        parse_mode="Markdown"
    )
    context.user_data["buyurtma"]["sana"] = datetime.now().strftime("%d.%m.%Y")
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
        "⏰ *8-qadam:* Tayyor bo'lish *deadlineni* kiriting\n"
        "_(Masalan: 25.04.2025 yoki 2 hafta ichida)_",
        parse_mode="Markdown"
    )
    return DEDLAYN

async def dedlayn_olish(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["buyurtma"]["dedlayn"] = update.message.text.strip()
    await update.message.reply_text(
        "✅ Dedlayn saqlandi!\n\n"
        "💰 *9-qadam:* Narxni kiriting\n"
        "_(Masalan: 150,000 so'm yoki 'Kelishiladi')_",
        parse_mode="Markdown"
    )
    return NARX

async def narx_olish(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["buyurtma"]["narx"] = update.message.text.strip()

    # Tasdiqlash sahifasi
    buyurtma = context.user_data["buyurtma"]
    keyboard = [
        [InlineKeyboardButton("✅ Tasdiqlash", callback_data="tasdiq_ha"),
         InlineKeyboardButton("✏️ Qayta to'ldirish", callback_data="tasdiq_yoq")]
    ]
    await update.message.reply_text(
        "📋 *BUYURTMANGIZNI TEKSHIRING:*\n\n" +
        order_text(buyurtma) +
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
        context.user_data["last_order"] = buyurtma.copy()

        # Adminга xabar yuborish
        try:
            admin_msg = (
                f"🔔 *YANGI BUYURTMA KELDI!*\n\n"
                + order_text(buyurtma)
                + f"\n\n👤 *Telegram:* @{query.from_user.username or 'username yo`q'}"
                f"\n🆔 *User ID:* `{query.from_user.id}`"
            )
            await context.bot.send_message(
                ADMIN_ID,
                admin_msg,
                parse_mode="Markdown"
            )
            # Agar dizayn rasm yuborilgan bo'lsa
            if buyurtma.get("dizayn_photo_id"):
                await context.bot.send_photo(
                    ADMIN_ID,
                    photo=buyurtma["dizayn_photo_id"],
                    caption="🖼 Yuqoridagi buyurtma uchun dizayn rasmi"
                )
        except Exception as e:
            logger.error(f"Admin xabar yuborishda xato: {e}")

        keyboard = [["🛍 Yangi buyurtma"], ["📦 Buyurtmalarim", "📞 Bog'lanish"]]
        await query.edit_message_text(
            "✅ *Buyurtmangiz muvaffaqiyatli qabul qilindi!*\n\n"
            "📲 Tikuvchi tez orada siz bilan bog'lanadi.\n\n"
            "⏰ Ish vaqti: 9:00 — 19:00\n"
            "🙏 Bizga ishonganingiz uchun rahmat!",
            parse_mode="Markdown"
        )
        await context.bot.send_message(
            query.from_user.id,
            "Bosh menyuga qaytish uchun pastdagi tugmani bosing 👇",
            reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
        )

    else:
        keyboard = [["🛍 Buyurtma berish"]]
        await query.edit_message_text(
            "✏️ Buyurtma bekor qilindi.\n\n"
            "Qaytadan to'ldirish uchun quyidagi tugmani bosing 👇",
            parse_mode="Markdown"
        )
        await context.bot.send_message(
            query.from_user.id,
            "Qaytadan boshlash:",
            reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
        )

    return ConversationHandler.END

async def bekor_qilish(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [["🛍 Buyurtma berish"], ["📦 Buyurtmalarim", "📞 Bog'lanish"]]
    await update.message.reply_text(
        "❌ Buyurtma bekor qilindi.\n\n"
        "Bosh menyuga qaytdingiz 👇",
        reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True),
        parse_mode="Markdown"
    )
    return ConversationHandler.END

# ==================== ASOSIY ====================

def main():
    app = Application.builder().token(BOT_TOKEN).build()

    # Conversation handler
    conv = ConversationHandler(
        entry_points=[
            MessageHandler(filters.Regex("^🛍 Buyurtma berish$"), buyurtma_boshlash)
        ],
        states={
            ISM: [MessageHandler(filters.TEXT & ~filters.COMMAND, ism_olish)],
            TEL: [
                MessageHandler(filters.CONTACT | (filters.TEXT & ~filters.COMMAND), tel_olish),
                CallbackQueryHandler(tel_skip, pattern="^tel_skip$"),
            ],
            RAZMER_TURI: [CallbackQueryHandler(razmer_turi_tanlash, pattern="^razmer_")],
            RAZMER: [
                CallbackQueryHandler(razmer_standart_tanlash, pattern="^r_"),
                MessageHandler(filters.TEXT & ~filters.COMMAND, razmer_text_olish),
            ],
            BEZAK: [CallbackQueryHandler(bezak_tanlash, pattern="^(b_|bezak_done)")],
            BEZAK_CUSTOM: [MessageHandler(filters.TEXT & ~filters.COMMAND, bezak_custom_olish)],
            DIZAYN: [CallbackQueryHandler(dizayn_tanlash, pattern="^d_")],
            DIZAYN_CUSTOM: [
                MessageHandler(filters.PHOTO | (filters.TEXT & ~filters.COMMAND), dizayn_custom_olish)
            ],
            DEDLAYN: [MessageHandler(filters.TEXT & ~filters.COMMAND, dedlayn_olish)],
            NARX: [MessageHandler(filters.TEXT & ~filters.COMMAND, narx_olish)],
            TASDIQ: [CallbackQueryHandler(tasdiq, pattern="^tasdiq_")],
        },
        fallbacks=[
            CommandHandler("bekor", bekor_qilish),
            MessageHandler(filters.Regex("^❌"), bekor_qilish),
        ],
    )

    app.add_handler(CommandHandler("start", start))
    app.add_handler(conv)
    app.add_handler(MessageHandler(filters.Regex("^📦 Buyurtmalarim$"), mening_buyurtmam))
    app.add_handler(MessageHandler(filters.Regex("^❓ Yordam$"), yordam))
    app.add_handler(MessageHandler(filters.Regex("^📞 Bog'lanish$"), boglanish))
    app.add_handler(MessageHandler(filters.Regex("^🛍 Yangi buyurtma$"), buyurtma_boshlash))

    print("🤖 Bot ishga tushdi!")
    app.run_polling()

if __name__ == "__main__":
    main()
