import asyncio, time
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from config import TOKEN, FREE_LIMIT, LIMIT_RESET_HOURS
from database import init_db, get_user, create_user, update_user_requests, reset_limit_if_needed
from generator import generate_emails
from keyboards import menu, domains_keyboard, count_keyboard

bot = Bot(TOKEN)
dp = Dispatcher()

users_temp = {}  # Временное хранение выбора домена/количества для пользователя

@dp.message(CommandStart())
async def start(message: types.Message):
    await message.answer("Добро пожаловать! Генератор почт.", reply_markup=menu)
    user = await get_user(message.from_user.id)
    if not user:
        await create_user(message.from_user.id)

@dp.message()
async def menu_handler(message: types.Message):
    await reset_limit_if_needed(message.from_user.id, LIMIT_RESET_HOURS)
    if message.text == "📩 Генерировать почты":
        await message.answer("Выберите домен:", reply_markup=domains_keyboard)
    elif message.text == "👤 Профиль":
        user = await get_user(message.from_user.id)
        used = user[1] if user else 0
        await message.answer(f"Ваш лимит: {FREE_LIMIT-used}/{FREE_LIMIT}")

@dp.callback_query()
async def callback_handler(query: types.CallbackQuery):
    user_id = query.from_user.id
    await reset_limit_if_needed(user_id, LIMIT_RESET_HOURS)
    user = await get_user(user_id)
    used = user[1] if user else 0

    if used >= FREE_LIMIT:
        await query.answer("Лимит исчерпан! Подождите восстановление.", show_alert=True)
        return

    data = query.data
    if data.startswith("domain_"):
        domain = data.split("_")[1]
        users_temp[user_id] = {"domain": domain}
        await query.message.answer("Выберите количество:", reply_markup=count_keyboard)
    elif data.startswith("count_"):
        count = int(data.split("_")[1])
        if user_id not in users_temp or "domain" not in users_temp[user_id]:
            await query.message.answer("Сначала выберите домен!")
            return
        domain = users_temp[user_id]["domain"]
        emails = generate_emails(domain, count)
        await query.message.answer("\n".join(emails))
        await update_user_requests(user_id, used+1)
        await query.answer("Готово! Лимит уменьшен.")

async def main():
    await init_db()
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
