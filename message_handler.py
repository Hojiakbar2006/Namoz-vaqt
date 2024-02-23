from telegram import InlineKeyboardMarkup, InlineKeyboardButton
from function import main_menu, send_regions, send_buttons


async def message_handler(update, context):
    message = update.message.text
    if message == "Namoz vaqtlari":
        await send_regions(context, chat_id=update.message.from_user.id)
    elif message == "Ma'lumot":
        await send_buttons(context, chat_id=update.message.from_user.id,)
