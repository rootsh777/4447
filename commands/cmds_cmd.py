from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes

async def cmds_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    keyboard = [
        [InlineKeyboardButton("Comprobante 1", callback_data="comprobante1")],
        [InlineKeyboardButton("Comprobante 2", callback_data="comprobante2")],
        [InlineKeyboardButton("Comprobante 3", callback_data="comprobante3")],
        [InlineKeyboardButton("Comprobante 4", callback_data="comprobante4")],
        [InlineKeyboardButton("Comprobante 5", callback_data="comprobante5")],
        [InlineKeyboardButton("Movimientos", callback_data="movimientos")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "Selecciona el comprobante que deseas generar:",
        reply_markup=reply_markup
    )