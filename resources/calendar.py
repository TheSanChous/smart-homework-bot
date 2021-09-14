from aiogram.types import *
import datetime
import calendar
from .strings import month_names


def create_callback_data(action,year,month,day):
    return "calendar:"+";".join([action,str(year),str(month),str(day)])


def separate_callback_data(data):
    return data.split(":")[1].split(";")


def create_calendar(year=None,month=None):
    now = datetime.datetime.now()
    if year is None:
        year = now.year
    if month is None:
        month = now.month
    data_ignore = create_callback_data("IGNORE", year, month, 0)
    keyboard = InlineKeyboardMarkup(row_width=1)
    # First row - Month and Year
    row = []
    row.append(InlineKeyboardButton(month_names[month-1]+" "+str(year), callback_data=data_ignore))
    keyboard.row(*row)
    # Second row - Week Days
    row = []
    for day in ["Пн", "Вт", "Ср", "Чт", "Пт", "Сб", "Вс"]:
        row.append(InlineKeyboardButton(day, callback_data=data_ignore))
    keyboard.row(*row)

    my_calendar = calendar.monthcalendar(year, month)
    for week in my_calendar:
        row = []
        for day in week:
            if day == 0:
                row.append(InlineKeyboardButton(" ", callback_data=data_ignore))
            elif day < now.day and month == now.month:
                row.append(InlineKeyboardButton(" ", callback_data=data_ignore))
            else:
                row.append(InlineKeyboardButton(str(day), callback_data=create_callback_data("DAY",year,month,day)))
        keyboard.row(*row)
    # Last row - Buttons
    row = []
    if now.month != month:
        row.append(InlineKeyboardButton("<", callback_data=create_callback_data("PREV-MONTH", year, month, day)))
    else:
        row.append(InlineKeyboardButton(" ", callback_data=data_ignore))
    row.append(InlineKeyboardButton(" ", callback_data=data_ignore))
    row.append(InlineKeyboardButton(">", callback_data=create_callback_data("NEXT-MONTH", year, month, day)))
    keyboard.row(*row)
    return keyboard


async def process_calendar_selection(callback_query: CallbackQuery):
    ret_data = (False,None)
    query = callback_query.data
    (action,year,month,day) = separate_callback_data(query)
    curr = datetime.datetime(int(year), int(month), 1)
    if action == "IGNORE":
        await callback_query.answer()
    elif action == "DAY":
        await callback_query.answer()
        ret_data = True, datetime.datetime(int(year),int(month),int(day))
    elif action == "PREV-MONTH":
        pre = curr - datetime.timedelta(days=1)
        await callback_query.message.edit_reply_markup(reply_markup=create_calendar(int(pre.year),int(pre.month)))
    elif action == "NEXT-MONTH":
        ne = curr + datetime.timedelta(days=31)
        await callback_query.message.edit_reply_markup(reply_markup=create_calendar(int(ne.year),int(ne.month)))
    else:
        await callback_query.answer()
        # UNKNOWN
    return ret_data
