# 🧵 TIKUVCHI BOT v2.0 — ADMIN QO'LLANMASI

## 🚀 Railway Deploy

### Environment Variables (Railway → Variables bo'limi):
```
BOT_TOKEN = 7xxxxxxxxx:AAxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
ADMIN_ID  = 123456789
```

### Deploy qilish:
1. Railway.app da yangi project oching
2. GitHub repo ga yuklang yoki "Deploy from template" → Python
3. Variables ga BOT_TOKEN va ADMIN_ID kiriting
4. Deploy!

---

## 👑 ADMIN BUYRUQLARI

| Buyruq | Nima qiladi |
|--------|-------------|
| `/admin` | Admin panelni ochadi |
| `/buyurtmalar` | Barcha buyurtmalar ro'yxati |

---

## 🔄 7 BOSQICH TIZIMI

```
📥 1. Qabul qilindi
    ↓
🧵 2. Mato tanlash
    ↓
✂️ 3. Kesish
    ↓
🪡 4. Tikish jarayoni
    ↓
👗 5. Примерка (Qiyish)
    ↓
✨ 6. Bezak & Tugallash
    ↓
✅ 7. Tayyor & Topshirildi
```

### Har bosqichda admin nima ko'radi:
- ✅ Joriy holatni ko'radi
- ➡️ Keyingi bosqichga o'tkazadi (1 tugma!)
- 💡 O'sha bosqich uchun maslahat oladi (milliy libos/to'y uchun maxsus)
- 📲 Mijozga avtomatik xabar yuboradi

---

## 📲 AVTOMATIK XABARLAR

Bosqich o'tganda mijoz Telegramga xabar oladi:
- Bosqich 1 → "Buyurtmangiz qabul qilindi ✅"
- Bosqich 5 → "Примеrkaga taklif qilamiz 👗"
- Bosqich 7 → "Buyurtmangiz tayyor! 🎉"

---

## 💡 MASLAHATLAR TIZIMI

Har bosqich uchun O'zbekiston tikuvchiligiga moslashtirilgan maslahatlar:

**Milliy libos uchun:**
- Atlas, Adras, Banoras, Xan atlas mato tavsiyalari
- Yoqa, yeng, etakka chok o'lchami
- Zardozi kashta uchun vaqt hisoblash

**To'y sarpolari uchun:**
- Fatin + atlas kombinatsiyasi
- Krep-satin, Organza tavsiyalari
- Strazlar va gul bezaklar joylashuvi
- Примерka oldidan tekshirish ro'yxati

---

## 📊 STATISTIKA

`/admin` → "📊 Statistika" tugmasi:
- Har bosqichdagi buyurtmalar soni
- Jami va tayyor buyurtmalar
