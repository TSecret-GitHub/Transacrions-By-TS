from telebot import types
from config import *
bar.next() #4

menu = types.ReplyKeyboardMarkup(True, True)
menu.row('Баланс', 'Перевести', 'Статус')
#menu.row('Функционал с счетами')
bar.next() #5

confirm = types.InlineKeyboardMarkup()
callback_button = types.InlineKeyboardButton(text="Подтвердить", callback_data="confirm")
callback_button1 = types.InlineKeyboardButton(text="Отклонить", callback_data="cancel")
callback_button2 = types.InlineKeyboardButton(text="Заблокировать", callback_data="block")
confirm.add(callback_button)
confirm.add(callback_button1)
confirm.add(callback_button2)
bar.next() #6

yesNo = types.InlineKeyboardMarkup()
yesNo_button1 = types.InlineKeyboardButton(text="Да", callback_data="yes")
yesNo_button2 = types.InlineKeyboardButton(text="Нет", callback_data="no")
yesNo.add(yesNo_button1)
yesNo.add(yesNo_button2)
bar.next() #20

yesNo_for_order = types.InlineKeyboardMarkup()
yesNo_for_order1 = types.InlineKeyboardButton(text="Да", callback_data="yes.order")
yesNo_for_order2 = types.InlineKeyboardButton(text="Отмена", callback_data="cancel.order")
yesNo_for_order.add(yesNo_for_order1)
yesNo_for_order.add(yesNo_for_order2)
bar.next() #23

#not confirmed = types.InlineKeyboardMarkup()

#update = types.ReplyKeyboardMarkup(True, True)
#update.row('Обновить Chat ID Супер-Администратора')