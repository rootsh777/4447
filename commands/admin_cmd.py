from telegram import Update
from telegram.ext import ContextTypes
from config import ADMIN_ID, USUARIOS_AUTORIZADOS, save_users, FREE_MODE

async def add_access(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.effective_user.id != ADMIN_ID:
        await update.message.reply_text("❌ No tienes permiso para usar este comando.")
        return
    try:
        if context.args:
            new_id = int(context.args[0])
            if new_id not in USUARIOS_AUTORIZADOS:
                USUARIOS_AUTORIZADOS.append(new_id)
                save_users(USUARIOS_AUTORIZADOS)
                await update.message.reply_text(f"✅ Acceso añadido para ID: {new_id}")
            else:
                await update.message.reply_text("ℹ️ El ID ya tiene acceso.")
        else:
            await update.message.reply_text("Por favor proporciona un ID.\nEjemplo: /add 123456789")
    except Exception as e:
        await update.message.reply_text("Error al procesar el comando.")

async def free_mode_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.effective_user.id != ADMIN_ID:
        await update.message.reply_text("❌ No tienes permiso para usar este comando.")
        return
    global FREE_MODE
    FREE_MODE = True
    await update.message.reply_text("✅ El bot ahora es libre para todos.")

async def close_mode_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.effective_user.id != ADMIN_ID:
        await update.message.reply_text("❌ No tienes permiso para usar este comando.")
        return
    global FREE_MODE
    FREE_MODE = False
    await update.message.reply_text("✅ El bot ahora está restringido a usuarios autorizados.")