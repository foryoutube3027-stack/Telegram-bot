import asyncio
import os

from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart
from aiogram.types import KeyboardButton, Message, ReplyKeyboardMarkup

TOKEN = os.getenv("BOT_TOKEN")  # tokenni kodga yozmang, muhit o'zgaruvchisida saqlang
LAT, LON = 40.453972, 71.663417

PRICE = (
    "💰 Narxlar:\n"
    "• Xitoy (Changan) karburatori: 350 000 so'm\n"
    "• O'rnatib berish (ustanovka): 150 000 so'm\n"
    "• Svecha almashtirish: narxi kelishiladi"
)
CHANGAN = (
    "🛠 Changan (Xitoy) karburatorini o'rnatish — Damas va Labo uchun eng samarali yechim.\n\n"
    + PRICE
)
FUEL = (
    "⛽ To'g'ri o'rnatilgan Xitoy karburatori 100 km ga 5.5–6 litr benzin sarflaydi.\n"
    "Amaliy testimizda 1 litr benzin bilan 17 km yurildi."
)
SERVICES = (
    "🔧 Xizmatlarimiz:\n"
    "• Karburator tozalash (to'liq demontaj bilan)\n"
    "• Igna-klapan almashtirish\n"
    "• Svecha almashtirish\n"
    "• Avto elektrik xizmatlari\n"
    "• Xolostoy yurishni sozlash\n"
    "• Umumiy texnik ko'rik"
)
ADDRESS = "📍 Manzil: Marg'ilon shahri, Qumtepa bozori oldida.\nLokatsiyani pastda yuboraman 👇"
HOURS = "⏰ Ish vaqti: 08:00 – 19:00\n❌ Dam olish kuni: Payshanba"
CONTACT = (
    "📞 Murojaat va navbatga yozilish uchun:\n"
    "• Tel: +998 93 611 85 85\n"
    "• Telegram: @Qumtepa_karburator"
)

# (kalit so'zlar, javob, lokatsiya yuborilsinmi)
# Kalit so'zlar apostrofsiz va kichik harfda yoziladi.
FAQ = [
    (["narx", "qancha", "necha", "pul", "somi", "tur"], PRICE, False),
    (["damas", "labo", "changan", "xitoy", "ornat", "ustanovka", "qoyib"], CHANGAN, False),
    (["rasxod", "sarf", "yoqilgi", "benzin", "litr", "tejam", "yeydi", "yeyap"], FUEL, False),
    (["xizmat", "tozalash", "igna", "klapan", "svecha", "elektrik", "xolostoy", "korik", "nima qil"], SERVICES, False),
    (["manzil", "qayer", "adres", "joylash", "lokatsiya", "location", "borish", "yol"], ADDRESS, True),
    (["ish vaqti", "soat", "qachon", "ochiq", "dam olish", "payshanba", "yopiq", "vaqt"], HOURS, False),
    (["tel", "raqam", "nomer", "aloqa", "boglan", "navbat", "yozil", "telegram"], CONTACT, False),
]

FALLBACK = "Bu savolga aniq javobim yo'q 😔\n\n" + CONTACT

KEYBOARD = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="💰 Narxlar"), KeyboardButton(text="🔧 Xizmatlar")],
        [KeyboardButton(text="📍 Manzil"), KeyboardButton(text="⏰ Ish vaqti")],
        [KeyboardButton(text="📞 Aloqa")],
    ],
    resize_keyboard=True,
)


def normalize(text: str) -> str:
    text = text.lower()
    for ch in "'‘’ʻʼ`":
        text = text.replace(ch, "")
    return text


def find_answer(text: str):
    text = normalize(text)
    best, best_score = None, 0
    for keywords, answer, send_loc in FAQ:
        score = sum(1 for k in keywords if k in text)
        if score > best_score:
            best, best_score = (answer, send_loc), score
    return best


dp = Dispatcher()


@dp.message(CommandStart())
async def start(message: Message):
    await message.answer(
        "Assalomu alaykum! 👋\n"
        "«Qumtepa Karburator» avto ustaxonasi botiga xush kelibsiz.\n"
        "Savolingizni yozing yoki pastdagi tugmalardan foydalaning.",
        reply_markup=KEYBOARD,
    )


@dp.message(F.text)
async def answer(message: Message):
    result = find_answer(message.text)
    if not result:
        await message.answer(FALLBACK, reply_markup=KEYBOARD)
        return
    text, send_loc = result
    await message.answer(text, reply_markup=KEYBOARD)
    if send_loc:
        await message.answer_location(LAT, LON)


async def main():
    bot = Bot(TOKEN)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
