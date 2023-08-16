import requests
from bs4 import BeautifulSoup
from telegram import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

from database import Database


def main_menu(context, chat_id):
    context.bot.send_message(
        chat_id=chat_id,
        text="Main menu",
        reply_markup=ReplyKeyboardMarkup(
            [
                [KeyboardButton(text="Namoz vaqtlari"), KeyboardButton(text="Ma'lumot")]
            ],
            resize_keyboard=True,
        )
    )


def remove_inline(query, context, chat_id, message_id):
    query.message.edit_text(
        text="🕓",
        reply_markup=None,
    )
    context.bot.delete_message(chat_id=query.message.chat_id, message_id=message_id)


def send_regions(context, chat_id, message_id=None):
    regions = Database("data.db").get_regions()
    buttons = [[InlineKeyboardButton(text=regions[0]['region_name'], callback_data=f"region_{regions[0]['id']}"),
                InlineKeyboardButton(text=regions[1]['region_name'], callback_data=f"region_{regions[1]['id']}")],
               [InlineKeyboardButton(text=regions[2]['region_name'], callback_data=f"region_{regions[2]['id']}"),
                InlineKeyboardButton(text=regions[3]['region_name'], callback_data=f"region_{regions[3]['id']}")],
               [InlineKeyboardButton(text=regions[4]['region_name'], callback_data=f"region_{regions[4]['id']}"),
                InlineKeyboardButton(text=regions[5]['region_name'], callback_data=f"region_{regions[5]['id']}")],
               [InlineKeyboardButton(text=regions[6]['region_name'], callback_data=f"region_{regions[6]['id']}"),
                InlineKeyboardButton(text=regions[7]['region_name'], callback_data=f"region_{regions[7]['id']}")],
               [InlineKeyboardButton(text=regions[8]['region_name'], callback_data=f"region_{regions[8]['id']}"),
                InlineKeyboardButton(text=regions[9]['region_name'], callback_data=f"region_{regions[9]['id']}")],
               [InlineKeyboardButton(text=regions[10]['region_name'], callback_data=f"region_{regions[10]['id']}"),
                InlineKeyboardButton(text=regions[11]['region_name'], callback_data=f"region_{regions[11]['id']}")],
               [InlineKeyboardButton(text=regions[12]['region_name'], callback_data=f"region_{regions[12]['id']}")],
               [InlineKeyboardButton(text="Main menu", callback_data="main_menu")]]

    if message_id:
        context.bot.edit_message_text(
            chat_id=chat_id,
            text="Viloyatlardan birini tanlang",
            reply_markup=InlineKeyboardMarkup(buttons),
            message_id=message_id
        )
    else:
        context.bot.send_message(
            chat_id=chat_id,
            text="Viloyatlardan birini tanlang",
            reply_markup=InlineKeyboardMarkup(buttons)
        )


def send_photo(context, chat_id, data_sp):
    re = requests.get(f"https://namozvaqti.uz/shahar/{data_sp[1]}")
    soup = BeautifulSoup(re.text, "html.parser")
    city = Database("data.db").get_one_city(data_sp[1])
    time = soup.find_all(class_="time")
    name = soup.find_all(class_="nam")
    text = soup.find(class_="vil").text.split("            ")
    text_2 = text[1].split("\n")
    context.bot.sendPhoto(
        photo=open("mosque.jpg", "rb"),
        chat_id=chat_id,
        caption=f"<strong>🕌{city[0]['city_name']} Namoz vaqtlari</strong>\n\n"
                f"{name[0].text}:\t\t{time[0].text}  (gacha saharlik)\n"
                f"{name[1].text}:\t\t{time[1].text}\n"
                f"{name[2].text}:\t\t{time[2].text}\n"
                f"{name[3].text}:\t\t{time[3].text}\n"
                f"{name[4].text}:\t\t{time[4].text}  (dan song iftor)\n"
                f"{name[5].text}:\t\t{time[5].text}\n\n"
                f"{text_2[0]}",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        text="Namoz haqida ko'proq ma'lumot",
                        callback_data="more_action"
                    )
                ]
            ]
        ),
        parse_mode="HTML"
    )


def send_cities(context, chat_id, data_sp, message_id=None):
    city = Database("data.db").get_city(region_id=int(data_sp[1]))
    buttons = []
    for i in city:
        buttons.append([InlineKeyboardButton(text=i['city_name'], callback_data=f"city_{i['path']}")])
    buttons.append([InlineKeyboardButton(text="Back", callback_data="region_back")])

    if message_id:
        context.bot.edit_message_text(
            chat_id=chat_id,
            message_id=message_id,
            text="Shahringizni tanlang",
            reply_markup=InlineKeyboardMarkup(buttons)
        )

    else:
        context.bot.send_message(
            chat_id=chat_id,
            text="Shahringizni tanlang",
            reply_markup=InlineKeyboardMarkup(buttons)
        )


def send_buttons(context, chat_id, message_id=None):
    informs = Database("data.db").get_namaz()
    buttons = [
        [
            InlineKeyboardButton(text=informs[0]['namaz_name'], callback_data=f"namaz_{informs[0]['id']}"),
            InlineKeyboardButton(text=informs[1]['namaz_name'], callback_data=f"namaz_{informs[1]['id']}")
        ],
        [
            InlineKeyboardButton(text=informs[2]['namaz_name'], callback_data=f"namaz_{informs[2]['id']}"),
            InlineKeyboardButton(text=informs[3]['namaz_name'], callback_data=f"namaz_{informs[3]['id']}")
        ],
        [
            InlineKeyboardButton(text=informs[4]['namaz_name'], callback_data=f"namaz_{informs[4]['id']}"),
            InlineKeyboardButton(text=informs[5]['namaz_name'], callback_data=f"namaz_{informs[5]['id']}")
        ],
        [InlineKeyboardButton(text="Back", callback_data="main_menu")]
    ]

    if message_id:
        context.bot.edit_message_text(
            chat_id=chat_id,
            message_id=message_id,
            text="Qaysi namoz haqida bilmoqchisiz ?",
            reply_markup=InlineKeyboardMarkup(buttons)
        )
    else:
        context.bot.send_message(
            chat_id=chat_id,
            text="Qaysi namoz haqida bilmoqchisiz ?",
            reply_markup=InlineKeyboardMarkup(buttons)
        )

def send_namaz_inform(context, chat_id, id):
    inform = Database("data.db").get_one_namaz(id)
    text = (f"{inform[0]['namaz_name']} namozi\n\n"
            f"{inform[0]['text']}")
    buttons = [
        [InlineKeyboardButton(text="Back", callback_data="namaz_back")]
    ]

    context.bot.send_message(
        chat_id=chat_id,
        reply_markup=InlineKeyboardMarkup(buttons),
        text=text
    )
