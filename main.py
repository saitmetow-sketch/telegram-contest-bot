import asyncio
from aiohttp import web
from aiogram import Bot, Dispatcher, F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message, CallbackQuery

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
    waiting_for_del_admin_id = State()
    waiting_for_broadcast = State()
    waiting_for_channel = State()
    waiting_for_req_channel = State()

@router.message(Command("start"))
async def cmd_start(message: Message):
    markup = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🏆 Top 10 kanal", callback_data="top")],
        [InlineKeyboardButton(text="🔍 Ovoz batl tekshirish", callback_data="check")]
    ])
    if message.from_user.id in admins:
        markup.inline_keyboard.append([InlineKeyboardButton(text="⚙️ Admin Menyu", callback_data="admin_menu")])
    await message.answer("✅ Xush kelibsiz! Kerakli bo'limni tanlang:", reply_markup=markup)

@router.callback_query(F.data == "admin_menu")
async def admin_menu(callback: CallbackQuery):
    markup = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="➕ Admin qo'shish", callback_data="add_adm"), InlineKeyboardButton(text="➖ Admin o'chirish", callback_data="del_adm")],
        [InlineKeyboardButton(text="📢 Reklama", callback_data="broadcast"), InlineKeyboardButton(text="📊 Statistika", callback_data="stats")],
        [InlineKeyboardButton(text="➕ Majburiy obuna", callback_data="add_chan"), InlineKeyboardButton(text="➕ So'rovli obuna", callback_data="add_req")],
        [InlineKeyboardButton(text="🗑 Kanallarni o'chirish", callback_data="del_chan")],
        [InlineKeyboardButton(text="🔙 Orqaga", callback_data="back_start")]
    ])
    await callback.message.edit_text("⚙️ **Admin Boshqaruv Paneli:**", reply_markup=markup)

@router.callback_query(F.data == "back_start")
async def back_start(callback: CallbackQuery):
    await callback.message.delete()
    await cmd_start(callback.message)

# --- Qolgan Admin funksiyalarini shu yerga yozasiz ---
# Masalan, 'broadcast' tugmasi uchun handler va boshqalar oldingi koddagidek qoladi.

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
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
