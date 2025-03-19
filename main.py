from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters
from commands.start_cmd import start_cmd
from commands.cmds_cmd import cmds_cmd
from commands.admin_cmd import add_access, free_mode_cmd, close_mode_cmd
from handlers import button_handler, handle_comprobante_input
from flask_server import start_flask

def main() -> None:
    TOKEN = "7913988104:AAHZnEPVHfH6KRQjZ8H7vlizraUF0TAMELM"  # Reemplaza con tu token real
    application = Application.builder().token(TOKEN).build()

    # Iniciar el servidor Flask
    start_flask()

    # Comandos de usuario
    application.add_handler(CommandHandler("start", start_cmd))
    application.add_handler(CommandHandler("cmds", cmds_cmd))
    application.add_handler(CommandHandler("comprobante2", cmds_cmd))  # Mensajes informativos, si se requiere
    application.add_handler(CommandHandler("comprobante3", cmds_cmd))
    application.add_handler(CommandHandler("comprobante4", cmds_cmd))
    application.add_handler(CommandHandler("comprobante5", cmds_cmd))
    application.add_handler(CommandHandler("movimientos", cmds_cmd))
    
    # Comandos administrativos
    application.add_handler(CommandHandler("add", add_access))
    application.add_handler(CommandHandler("free", free_mode_cmd))
    application.add_handler(CommandHandler("close", close_mode_cmd))

    # Manejadores para botones y conversación
    application.add_handler(CallbackQueryHandler(button_handler))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_comprobante_input))

    application.run_polling()

if __name__ == "__main__":
    main()