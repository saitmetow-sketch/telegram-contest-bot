import asyncio
from aiohttp import web
from aiogram import Bot, Dispatcher, F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message, CallbackQuery

# Siz bergan token to'g'ridan-to'g'ri yozildi
TOKEN = "8843973392:AAHwWFKmaL0JqGVcRvPL94CmY2cvJV0SFao"
OWNER_ID = 7020448136

bot = Bot(token=TOKEN)
dp = Dispatcher()
router = Router()

admins = {OWNER_ID}
subscribed_channels = []
users = {OWNER_ID}

class AdminStates(StatesGroup):
    waiting_for_admin_id = State()
    waiting_for_broadcast = State()
    waiting_for_channel = State()

async def check_subscriptions(user_id: int) -> bool:
    for ch in subscribed_channels:
        try:
            member = await bot.get_chat_member(chat_id=ch["id"], user_id=user_id)
            if member.status in ["left", "kicked"]: return False
        except: return False
    return True

@router.message(Command("start"))
async def cmd_start(message: Message, state: FSMContext):
    user_id = message.from_user.id
    users.add(user_id)
    if subscribed_channels and not await check_subscriptions(user_id):
        await message.answer("⚠️ Botdan foydalanish uchun kanallarga obuna bo'ling!")
        return
    
    markup = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🏆 Top 10", callback_data="top")],
        [InlineKeyboardButton(text="🔍 Tekshirish", callback_data="check")]
    ])
    if user_id in admins:
        markup.inline_keyboard.append([InlineKeyboardButton(text="⚙️ Admin Menyu", callback_data="admin_menu")])
    await message.answer("✅ Bot ishga tushdi!", reply_markup=markup)

@router.callback_query(F.data == "admin_menu")
async def admin_menu(callback: CallbackQuery):
    markup = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📢 Reklama", callback_data="broadcast")],
        [InlineKeyboardButton(text="📊 Statistika", callback_data="stats")],
        [InlineKeyboardButton(text="➕ Kanal qo'shish", callback_data="add_chan")]
    ])
    await callback.message.edit_text("⚙️ Admin menyu:", reply_markup=markup)

async def handle(request): return web.Response(text="Bot is running!")

async def web_server():
    app = web.Application()
    app.add_routes([web.get("/", handle)])
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", 8080)
    await site.start()

async def main():
    dp.include_router(router)
    asyncio.create_task(web_server())
    print("Bot ishga tushdi...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
