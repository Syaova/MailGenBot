from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup

# Главное меню
menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="📩 Генерировать почты")],
        [KeyboardButton(text="👤 Профиль")]
    ],
    resize_keyboard=True
)

# Выбор домена
domains_keyboard = InlineKeyboardMarkup(row_width=2)
for dom in ["gmail.com", "outlook.com", "yahoo.com"]:
    domains_keyboard.insert(InlineKeyboardButton(text=dom, callback_data=f"domain_{dom}"))

# Выбор количества почт
count_keyboard = InlineKeyboardMarkup(row_width=3)
for c in [1, 3, 5]:
    count_keyboard.insert(InlineKeyboardButton(text=str(c), callback_data=f"count_{c}"))
