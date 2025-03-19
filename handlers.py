import logging
import os
import copy
import uuid
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext
from telegram.error import BadRequest
from config import (
    conversation_fields,
    comprobante_titles,
    REQUIRED_CHANNELS,
    REQUIRED_CHANNELS_URLS,
    ALLOWED_CHATS,
    ALLOWED_CHAT_LINK,
    USUARIOS_AUTORIZADOS,
    FREE_MODE,
    ADMIN_ID,
    COMPROBANTES  # Se asume que COMPROBANTES está definido en config.py
)
import utils  # Contiene la función generar_comprobante

async def verificar_acceso(update: Update, context: CallbackContext) -> bool:
    """
    Verifica inmediatamente:
      - En grupos/canales, que el chat esté en ALLOWED_CHATS.
      - En chat privado, que el usuario esté suscrito a los REQUIRED_CHANNELS.
      - Además, si FREE_MODE es False, que el usuario esté en USUARIOS_AUTORIZADOS.
    Si falta membresía, envía botones para unirse y detiene el flujo.
    """
    chat = update.effective_chat
    user_id = update.effective_user.id

    # Si se usa en grupo/canal, comprobar que el chat esté autorizado.
    if chat.type in ["group", "supergroup", "channel"]:
        if chat.id not in ALLOWED_CHATS:
            try:
                await update.message.reply_text(
                    f"❌ Este chat no está autorizado para usar el bot.\n"
                    f"Por favor, únete al grupo autorizado: {ALLOWED_CHAT_LINK}"
                )
            except Exception as e:
                logging.error(f"Error al enviar mensaje en chat no autorizado: {e}")
            await context.bot.leave_chat(chat.id)
            return False

    # En chats privados, verificar membresía en REQUIRED_CHANNELS.
    if chat.type == "private":
        missing = []
        for channel in REQUIRED_CHANNELS:
            try:
                member = await context.bot.get_chat_member(chat_id=channel, user_id=user_id)
                if member.status not in ["creator", "administrator", "member", "restricted"]:
                    missing.append(channel)
            except BadRequest:
                missing.append(channel)
            except Exception as e:
                logging.error(f"Error verificando canal {channel}: {e}")
                missing.append(channel)
        if missing:
            keyboard = [
                [
                    InlineKeyboardButton("Grupo 1", url=REQUIRED_CHANNELS_URLS.get("grupo1", "")),
                    InlineKeyboardButton("Grupo 2", url=REQUIRED_CHANNELS_URLS.get("grupo2", ""))
                ]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await update.message.reply_text(
                "❌ No puedes utilizar el bot. Únete a estos grupos para poder usarlo:",
                reply_markup=reply_markup
            )
            return False

    # Verificar autorización del usuario (si no está en modo libre)
    if not FREE_MODE and user_id not in USUARIOS_AUTORIZADOS:
        await update.message.reply_text("❌ No estás autorizado para usar este bot.")
        return False

    return True

def get_main_menu(user_id: int) -> InlineKeyboardMarkup:
    """Devuelve el menú principal. Se muestra el botón 'admins' solo para el admin."""
    keyboard = [
        [InlineKeyboardButton("💡 Cómo usar", callback_data="how_to")],
        [InlineKeyboardButton("👤 Creador", callback_data="creator")]
    ]
    if user_id == ADMIN_ID:
        keyboard.append([InlineKeyboardButton("🔒 Admins", callback_data="admins")])
    return InlineKeyboardMarkup(keyboard)

async def button_handler(update: Update, context: CallbackContext) -> None:
    """Manejador para los botones inline."""
    query = update.callback_query
    await query.answer()
    data = query.data

    if data == "how_to":
        text = (
            "📖 *Cómo usar el bot:*\n\n"
            "• Usa el comando /cmds para ver los comprobantes disponibles.\n"
            "• Selecciona el comprobante deseado y sigue las instrucciones.\n"
            "• Cada comprobante se creará de forma interactiva, preguntándote cada dato."
        )
        await query.edit_message_text(text=text, parse_mode="Markdown")
    elif data == "creator":
        text = "👤 *Creador:*\n\nEste bot fue creado por [@sff_222]."
        await query.edit_message_text(text=text, parse_mode="Markdown")
    elif data == "admins":
        if update.effective_user.id != ADMIN_ID:
            await query.edit_message_text(text="❌ Acceso denegado. No eres admin.")
        else:
            text = (
                "⚙️ *Panel de Administración:*\n\n"
                "Usa los botones para cambiar el modo del bot o para agregar nuevos usuarios.\n"
                "Para agregar un usuario, utiliza el comando /add <ID>."
            )
            keyboard = [
                [InlineKeyboardButton("🔓 Modo Libre", callback_data="admin_free")],
                [InlineKeyboardButton("🔒 Modo Restringido", callback_data="admin_close")],
                [InlineKeyboardButton("➕ Agregar Usuario", callback_data="admin_add")]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await query.edit_message_text(text=text, parse_mode="Markdown", reply_markup=reply_markup)
    elif data in conversation_fields.keys():
        context.user_data["current_comprobante"] = data
        context.user_data["step"] = 0
        title = comprobante_titles.get(data, data)
        prompt = conversation_fields[data][0][1]
        await query.edit_message_text(text=f"🍀 *{title}*\n\n{prompt}", parse_mode="Markdown")
    elif data == "admin_free":
        if update.effective_user.id != ADMIN_ID:
            await query.edit_message_text(text="❌ Acceso denegado. No eres admin.")
        else:
            await query.edit_message_text(text="✅ Modo libre activado.")
    elif data == "admin_close":
        if update.effective_user.id != ADMIN_ID:
            await query.edit_message_text(text="❌ Acceso denegado. No eres admin.")
        else:
            await query.edit_message_text(text="✅ Modo restringido activado.")
    elif data == "admin_add":
        if update.effective_user.id != ADMIN_ID:
            await query.edit_message_text(text="❌ Acceso denegado. No eres admin.")
        else:
            await query.edit_message_text(text="Para agregar un usuario, utiliza el comando /add <ID>.")
    else:
        await query.edit_message_text(text="❌ Opción no reconocida.")

async def handle_comprobante_input(update: Update, context: CallbackContext) -> None:
    """Manejador de la conversación interactiva para generar comprobantes."""
    if not await verificar_acceso(update, context):
        return

    if "current_comprobante" not in context.user_data:
        return

    comp = context.user_data["current_comprobante"]
    steps = conversation_fields.get(comp)
    step_index = context.user_data.get("step", 0)
    current_field = steps[step_index][0]
    text = update.message.text.strip()

    if current_field == "phone":
        if not text.replace(" ", "").isdigit():
            await update.message.reply_text("⚠️ El número debe ser numérico. Intente de nuevo:")
            return
    if current_field in ("value", "cc"):
        if not text.isdigit():
            await update.message.reply_text(f"⚠️ El campo {current_field} debe ser numérico. Intente de nuevo:")
            return

    context.user_data[current_field] = text
    step_index += 1
    context.user_data["step"] = step_index

    if step_index < len(steps):
        next_prompt = steps[step_index][1]
        await update.message.reply_text(next_prompt)
    else:
        try:
            # Para cada comprobante, se crea una copia del config y se asigna un nombre aleatorio al output.
            import uuid
            comp_conf = copy.deepcopy(COMPROBANTES[comp])
            ext = comp_conf["output"].split('.')[-1]
            comp_conf["output"] = f"{comp}_{uuid.uuid4().hex}.{ext}"
            if comp == "comprobante1":
                path = utils.generar_comprobante(
                    context.user_data["name"],
                    context.user_data["phone"],
                    int(context.user_data["value"]),
                    comp_conf,
                    ajuste_x=-200
                )
            elif comp == "comprobante2":
                path = utils.generar_comprobante(
                    context.user_data["name"],
                    context.user_data["phone"],
                    int(context.user_data["value"]),
                    comp_conf,
                    ajuste_x=-140
                )
            elif comp == "comprobante3":
                path = utils.generar_comprobante(
                    context.user_data["name"],
                    context.user_data["phone"],
                    int(context.user_data["value"]),
                    comp_conf,
                    ajuste_x=-140
                )
            elif comp == "comprobante4":
                path = utils.generar_comprobante(
                    "",  # No se usa el nombre
                    context.user_data["phone"],
                    int(context.user_data["value"]),
                    comp_conf,
                    ajuste_x=-100
                )
            elif comp == "comprobante5":
                path = utils.generar_comprobante(
                    context.user_data["name"],
                    context.user_data["phone"],
                    int(context.user_data["value"]),
                    comp_conf,
                    ajuste_x=-140,
                    cc=context.user_data["cc"]
                )
            elif comp == "movimientos":
                path = utils.generar_comprobante(
                    context.user_data["name"],
                    "",
                    int(context.user_data["value"]),
                    comp_conf
                )
            else:
                await update.message.reply_text("❌ Comprobante no reconocido.")
                return

            with open(path, "rb") as f:
                await update.message.reply_document(document=f, caption="✅ Se generó correctamente.")
            # Elimina el archivo generado
            os.remove(path)
        except Exception as e:
            logging.error(f"Error al generar comprobante: {e}")
            await update.message.reply_text("❌ Error al generar el comprobante.")
        for key in ("current_comprobante", "step", "name", "phone", "value", "cc"):
            context.user_data.pop(key, None)