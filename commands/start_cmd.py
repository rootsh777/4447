from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes

async def start_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    keyboard = [
        [InlineKeyboardButton("💡 Cómo usar", callback_data="how_to")],
        [InlineKeyboardButton("👤 Creador", callback_data="creator")],
        [InlineKeyboardButton("🔒 Admins", callback_data="admins")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "¡Bienvenido al bot de comprobantes!\nSelecciona una opción:",
        reply_markup=reply_markup
    )