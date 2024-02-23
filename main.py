from telegram.ext import ApplicationBuilder, filters, CommandHandler, CallbackQueryHandler, MessageHandler
from function import main_menu
from message_handler import message_handler
from inline_message_handler import inline_message_handler
from config import users_id, TOKEN, admin_id


async def start_handler(update, context):
    user_id = update.message.from_user.id
    username = update.message.from_user.username
    if user_id not in users_id and user_id != admin_id:
        users_id.append({"id": user_id, "user_name": username})
        await main_menu(context=context, chat_id=user_id)
        await context.bot.send_message(
            chat_id=admin_id,
            text=f"username: @{username}\nchat_id: {user_id}"
        )
    elif user_id == admin_id:
        for i in range(len(users_id)):
            await context.bot.send_message(
                chat_id=admin_id,
                text=f"username: @{users_id[i]['user_name']
                                   }\nchat_id: {users_id[i]['id']}"
            )


if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler('start', start_handler))
    app.add_handler(MessageHandler(filters.TEXT, message_handler))
    app.add_handler(CallbackQueryHandler(inline_message_handler))

    app.run_polling()
