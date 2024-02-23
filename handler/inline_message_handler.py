from function import send_regions, send_photo, send_cities, remove_inline, main_menu, send_buttons, send_namaz_inform


async def inline_message_handler(update, context):
    query = update.callback_query
    data_sp = query.data.split("_")
    chat_id = query.message.chat_id
    message_id = query.message.message_id
    if data_sp[0] == "region":
        if data_sp[1] == "back":
            await send_regions(context, chat_id, message_id)
        else:
            await send_cities(context, chat_id, data_sp, message_id)

    elif data_sp[0] == "city":
        if data_sp[1] == "Back to region":
            await send_regions(context, chat_id, message_id)
        else:
            await remove_inline(query, context, chat_id, message_id)
            await send_photo(context, chat_id, data_sp)

    elif data_sp[0] == "namaz":
        if data_sp[1] == "back":
            await send_buttons(context, chat_id, message_id)
        else:
            await remove_inline(query, context, chat_id, message_id)
            await send_namaz_inform(context, chat_id, id=data_sp[1])

    elif query.data == "main_menu":
        await remove_inline(query, context, chat_id, message_id)
        await main_menu(context, chat_id)
