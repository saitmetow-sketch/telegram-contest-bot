import asyncio
from aiohttp import web
from aiogram import Bot, Dispatcher, F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message, CallbackQuery

# Tokeningiz
TOKEN = "8843973392:AAHwWFKmaL0JqGVcRvPL94CmY2cvJV0SFao"
OWNER_ID = 7020448136

bot = Bot(token=TOKEN)
dp = Dispatcher()
router = Router()

admins = {OWNER_ID}

@router.message(Command("start"))
async def cmd_start(message: Message):
    # Tugmalar dizayni
    markup = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🏆 Top 10 kanal", callback_data="top")],
        [InlineKeyboardButton(text="🔍 Ovoz batl tekshirish", callback_data="check")]
    ])
    
    # Rasmda ko'rsatilgan chiroyli matn
    text = (
        "✅ Xush kelibsiz!\n\n"
        "👑 Bot ishga tushdi!\n\n"
        "📌 Kanalda:\n"
        "• #konkurs - ovozli konkurs\n"
        "• #random - random konkurs\n"
        "• #batl - like batl (yangi!)\n\n"
        "📝 Random konkurs formati:\n"
        "#random\n"
        "salom yangi konkurs boshlandik\n"
        "yutuq nft emas\n"
        "shartlari\n"
        "@kanal\n"
        "#soni 3\n\n"
        "🔍 Ovoz batl tekshirish:\n"
        "• Quyidagi knopkani bosing va konkurs xabarini forward qiling\n\n"
        "👇 Kerakli bo'limni tanlang:"
    )
    
    # Agar admin bo'lsa, Admin tugmasini qo'shish
    if message.from_user.id in admins:
        markup.inline_keyboard.append([InlineKeyboardButton(text="⚙️ Admin Menyu", callback_data="admin_menu")])
        
    await message.answer(text, reply_markup=markup)

@router.callback_query(F.data == "admin_menu")
async def admin_menu(callback: CallbackQuery):
    markup = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📢 Reklama", callback_data="broadcast")],
        [InlineKeyboardButton(text="📊 Statistika", callback_data="stats")],
        [InlineKeyboardButton(text="➕ Kanal qo'shish", callback_data="add_chan")]
    ])
    await callback.message.edit_text("⚙️ **Admin Boshqaruv Paneli:**", reply_markup=markup)

async def handle(request): 
    return web.Response(text="Bot is running!")

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
