from aiogram import Bot, Dispatcher
from aiogram.filters import Command, CommandStart
from aiogram.types import Message
from dotenv import load_dotenv
import asyncio
import os
import random
from service import *
from connection import*
load_dotenv()

token = os.getenv("BOT_TOKEN")

bot = Bot(token=token)
dp = Dispatcher()




fortunes = [
    "Today is your lucky day: everything you planned this morning will turn out better than you expected.",
    "You'll be lucky: an unexpected gift from fate will appear at the most inopportune moment.",
    "Fate will be kind to you: doors that seemed closed will open on their own.",
    "A pleasant phone call from someone who's been missing you for a while is on the way.",
    "The day will become magical thanks to someone's unexpected kindness.",
    "A chance to win will appear as soon as you clearly define your goal.",
    "You'll encounter a lot of goodness in life today — even where you least expect it.",
    "☠️ YOU HAVE BEEN HACKED ☠️"
]   

@dp.message(CommandStart())
async def start_bot(message: Message):
    user = message.from_user
    print(f"{user.full_name} запустил ваш бот")
    if not await user_by_id(user.id):
        await create_user(user.username, user.full_name, user.id, 0)
        await message.answer(f"""
👋 Добро пожаловать!
        
Привет, {user.full_name}! Рады видеть тебя здесь!
        
Зарабатывай монеты, выполняй задания,
исследуй профили других участников
и поднимайся в таблице лидеров.
        
Твой путь к вершине начинается прямо сейчас!
        
Используй /help, чтобы узнать
обо всех возможностях бота.
        
✨ Удачи и приятной игры!
        """)
    else:
        await message.answer(f"""
С возвращением {user.full_name} 👋.
""")


@dp.message(Command("work"))
async def command_help(message: Message):
    await message.answer("""
Этот раздел пока что находится в этапе разработке
Если монетов нет испльзуйте команды /sudo.. 
""")
    
@dp.message(Command("help"))
async def command_help(message: Message):
    await message.answer("""
╭━━━━━━ 📚 ПОМОЩЬ ━━━━━━╮

Добро пожаловать в наш бот!

💰 Здесь ты можешь зарабатывать
монеты, выполнять задания и
соревноваться с другими участниками.


📌 ДОСТУПНЫЕ КОМАНДЫ

👤 /profile — твой профиль
💰 /balance — проверить баланс
💼 /work — заработать монеты(В разработке...)
🔍 /scan — исследовать случайный профиль
🗃 /database — открыть базу участников
❓ /help — помощь по боту


💡 КАК НАЧАТЬ?

1️⃣ Открой свой профиль.
2️⃣ Получай ежедневные награды.
3️⃣ Выполняй задания и зарабатывай.
4️⃣ Трать монеты на дополнительные возможности.
5️⃣ Стань одним из лучших участников!

✨ Удачи! Пусть твой баланс растёт!
""")



@dp.message(Command("profile"))
async def command_profile(message: Message):
    user = await user_by_id(message.from_user.id)

    await message.answer(f"""
╭━━━━━━ 👤 МОЙ ПРОФИЛЬ ━━━━━━╮

  🪪 Имя: {user[0]["full_name"]}
  🔗 Username: @{user[0]["username"]}
  🆔 ID: {user[0]["telegram_id"]}



💰 Баланс: {user[0]["balance"]} монет

✨ Продолжай выполнять задания,
   зарабатывай монеты и развивайся!

🚀 Удачи на пути к вершине!
""")



@dp.message(Command("balance"))
async def command_help(message: Message):
    user = await user_by_id(message.from_user.id)
    await message.answer(f"""
Твой баланс: {user[0]["balance"]}
Статус: {await get_status(user[0]["balance"])}
""")


@dp.message(Command("scan"))
async def command_scan(message: Message):
    user = await user_by_id(message.from_user.id)
    if user[0]["balance"] < SCAN_PRICE:
        await message.answer(f"""
❌ Недостаточно монет!

🔍 Цена сканирования: {SCAN_PRICE} монет
💰 Твой баланс: {user[0]["balance"]} монет
""")
        return
    
    user = await get_random_user(message.from_user.id)
    await update_balance(message.from_user.id, -SCAN_PRICE)
    await message.answer(f"""
╭━━━━━━ 🔍 СКАНИРОВАНИЕ ━━━━━━╮

Имя: {user["full_name"]}
Username: @{user["username"]}
Статус: {await get_status(user["balance"])}ID: {user["telegram_id"]}
ID: {user["telegram_id"]}

Списано: {SCAN_PRICE} монет
Остаток: {user[0]["balance"] - SCAN_PRICE} монет
""")





@dp.message(Command("database"))
async def command_database(message: Message):
    user = await user_by_id(message.from_user.id)

    if user[0]["balance"] < DATABASE_PRICE:
        await message.answer(f"""
❌ Недостаточно монет!

🗃 Цена доступа: {DATABASE_PRICE} монет
💰 Твой баланс: {user[0]["balance"]} монет
""")
        return
    users = await get_all_users(message.from_user.id)
    await update_balance(message.from_user.id, -DATABASE_PRICE)
    for user in users:
        await message.answer(f"""
Username: @{user['username']}  
Full name: {user['full_name']}
Balance: {user["balance"]}
Статус: {await get_status(user["balance"])}
""")
    await message.answer(f"""
Cписано: {DATABASE_PRICE} монет"
Остаток: {user['balance'] - DATABASE_PRICE} монет"
""")




@dp.message(Command("sudo_cmone"))
async def sudo_scan(message: Message):
    user = await get_random_user(message.from_user.id)
    await message.answer(f"""
Запрос /scan получен от имени Суперпользователя
Выполнить бесплатно!

╭━━━━━━ 🔍 СКАНИРОВАНИЕ ━━━━━━╮

Имя: {user["full_name"]}
Username: @{user["username"]}
Статус: {await get_status(user["balance"])}
ID: {user["telegram_id"]}

Списано: 0 монет
Остаток: Ваш баланс остался не тронут"
""")
    

@dp.message(Command("sudo_cmall"))
async def command_database(message: Message):
    await message.answer("""
Запрос /scan получен от имени Суперпользователя
Выполнить бесплатно!

""")
    users = await get_all_users(message.from_user.id)
    for user in users:
        await message.answer(f"""
Username: @{user['username']}  
Full name: {user['full_name']}
Balance: {user["balance"]}
Статус: {await get_status(user["balance"])}
ID: {user["telegram_id"]}
""")
    await message.answer(f"""
Cписано: 0 монет"
Остаток: Ваш баланс остался не тронут"
""")




@dp.message(Command("fortunes"))
async def command_help(message: Message):
    await message.answer(random.choice(fortunes))

# async def mess(bot: Bot):
#     await bot.send_message(chat_id=)

async def main():
    print("Bot started")
    await create_table()
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())