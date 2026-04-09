# 🧵 TIKUVCHI BOT — O'RNATISH YO'RIQNOMASI

## 1-QADAM: Bot yaratish (@BotFather orqali)
1. Telegramda @BotFather ga yozing
2. /newbot buyrug'ini yuboring
3. Botga nom bering (masalan: Nilufar Tikuvchi)
4. Username bering (masalan: @nilufar_tikuvchi_bot)
5. **TOKEN** ni nusxalab oling ✅

## 2-QADAM: Telegram ID olish
1. @userinfobot ga /start yuboring
2. **ID raqamingizni** nusxalab oling ✅

## 3-QADAM: bot.py faylini tahrirlash
Faylda quyidagi 2 qatorni o'zgartiring:

```python
BOT_TOKEN = "SIZNING_BOT_TOKENINGIZ"   # ← BotFather dan olgan tokenni yozing
ADMIN_ID = 123456789                    # ← O'zingizning Telegram ID raqamingiz
```

## 4-QADAM: Python va kutubxona o'rnatish

**Windows uchun:**
```
pip install python-telegram-bot==20.7
```

**Mac/Linux uchun:**
```
pip3 install python-telegram-bot==20.7
```

## 5-QADAM: Botni ishga tushirish
```
python bot.py
```
yoki
```
python3 bot.py
```

Konsolda **"🤖 Bot ishga tushdi!"** yozuvi chiqsa — muvaffaqiyat! ✅

---

## 📱 BOT QANDAY ISHLAYDI?

Buyurtmachi:
1. /start → Bosh menyu
2. 🛍 Buyurtma berish → boshlaydi
3. Ism → Telefon → Razmer → Bezak → Dizayn → Dedlayn → Narx
4. ✅ Tasdiqlaydi

**Sizga:**
- Yangi buyurtma kelganda Telegramga to'liq xabar keladi 📲
- Buyurtmachi ismi, telefoni, razmeri, dizayni, narxi — barchasi!

---

## 🌐 24/7 ISHLATISH (Ixtiyoriy)

Botni doim yoqiq ushlab turish uchun:
- **Railway.app** (bepul hosting) — https://railway.app
- **Render.com** (bepul) — https://render.com
- VPS server (oylik ~$5)

---

## ❓ Muammo bo'lsa:
- Token noto'g'ri bo'lsa: **BotFather** dan qayta oling
- ID noto'g'ri bo'lsa: **@userinfobot** dan tekshiring
