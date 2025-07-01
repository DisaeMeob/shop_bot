from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
import logging
from config import TOKEN, ADMIN_ID
from db import create_table, add_user, get_user_id, get_stat
from pdb import create_photo_db, exist, add_photo, get_photo

bot = Bot(TOKEN)
dp =Dispatcher(bot, storage=MemoryStorage())
logging.basicConfig(level=logging.INFO)
create_photo_db()
create_table()

class Form(StatesGroup):
  phoso_searcher = State()
  add = State()
  photo = State()
  buy_category = State()
  buy_product = State()
  broadcast = State() 

#Админ панель

buy_kb = types.InlineKeyboardMarkup(row_width=1)
buy_kb.add(
  types.InlineKeyboardButton(text='Ветровки', callback_data='wind'),
  types.InlineKeyboardButton(text='Зипки', callback_data='zip'),
  types.InlineKeyboardButton(text='Футболки', callback_data='tshirt'),
  types.InlineKeyboardButton(text='Штаны/Шорты', callback_data='shorts'),
  types.InlineKeyboardButton(text='Обувь', callback_data='shoes'),
  types.InlineKeyboardButton(text='Другое', callback_data='other'),
  types.InlineKeyboardButton(text='Выйти', callback_data='exit')
)
admin_kb = types.InlineKeyboardMarkup(row_width=1)
admin_kb.add(
  types.InlineKeyboardButton(text='Рассылка', callback_data='send_broadcast'),
  types.InlineKeyboardButton(text='Статистика', callback_data='stat'),
  types.InlineKeyboardButton(text='Добавить товар', callback_data='add_product'),
  types.InlineKeyboardButton(text='Выйти', callback_data='exit')
  
)

winds_kb = types.InlineKeyboardMarkup(row_width=1)
winds_kb.add(
  types.InlineKeyboardButton(text='Ветровка 1', callback_data='wind1'),
  types.InlineKeyboardButton(text='Ветровка 2', callback_data='wind2'),
  types.InlineKeyboardButton(text='Ветровка 3', callback_data='wind3'),
  types.InlineKeyboardButton(text='Выйти', callback_data='exit')
)
zips_kb = types.InlineKeyboardMarkup(row_width=1)
zips_kb.add(
  types.InlineKeyboardButton(text='Зипка 1', callback_data='zip1'),
  types.InlineKeyboardButton(text='Зипка 2', callback_data='zip2'),
  types.InlineKeyboardButton(text='Зипка 3', callback_data='zip3'),
  types.InlineKeyboardButton(text='Выйти', callback_data='exit')
)
tshirts_kb = types.InlineKeyboardMarkup(row_width=1)
tshirts_kb.add(
  types.InlineKeyboardButton(text='Футболка 1', callback_data='tshirt1'),
  types.InlineKeyboardButton(text='Футболка 2', callback_data='tshirt2'),
  types.InlineKeyboardButton(text='Футболка 3', callback_data='tshirt3'),
  types.InlineKeyboardButton(text='Выйти', callback_data='exit')
)

shorts_kb = types.InlineKeyboardMarkup(row_width=1)
shorts_kb.add(
  types.InlineKeyboardButton(text='Штаны 1', callback_data='shorts1'),
  types.InlineKeyboardButton(text='Штаны 2', callback_data='shorts2'),
  types.InlineKeyboardButton(text='Штаны 3', callback_data='shorts3'),
  types.InlineKeyboardButton(text='Выйти', callback_data='exit')
)
shoes_kb = types.InlineKeyboardMarkup(row_width=1)
shoes_kb.add(
  types.InlineKeyboardButton(text='Обувь 1', callback_data='shoes1'),
  types.InlineKeyboardButton(text='Обувь 2', callback_data='shoes2'),
  types.InlineKeyboardButton(text='Обувь 3', callback_data='shoes3'),
  types.InlineKeyboardButton(text='Выйти', callback_data='exit')
)
other_kb = types.InlineKeyboardMarkup(row_width=1)
other_kb.add(
  types.InlineKeyboardButton(text='Другое 1', callback_data='other1'),
  types.InlineKeyboardButton(text='Другое 2', callback_data='other2'),
  types.InlineKeyboardButton(text='Другое 3', callback_data='other3'),
  types.InlineKeyboardButton(text='Выйти', callback_data='exit')
)


user_kb = types.InlineKeyboardMarkup(row_width=1,)
user_kb.add(
  types.InlineKeyboardButton(text='Купить', callback_data='buy'),
  types.InlineKeyboardButton(text='Фотопоиск', callback_data='photo_search'),
  types.InlineKeyboardButton(text='Помощь', callback_data='help'),
  types.InlineKeyboardButton(text='Выйти', callback_data='exit')
)

winds_list = ['wind1', 'wind2', 'wind3']
zips_list = ['zip1', 'zip2', 'zip3']
tshirts_list = ['tshirt1', 'tshirt2', 'tshirt3']
shorts_list = ['shorts1', 'shorts2', 'shorts3']
shoes_list = ['shoes1', 'shoes2', 'shoes3']
other_list = ['other1', 'other2', 'other3']

buy_list = winds_list + zips_list + tshirts_list + shorts_list + shoes_list + other_list


#exit
@dp.callback_query_handler(lambda call: call.data == 'exit', state='*')
async def exit(call: types.CallbackQuery, state: FSMContext):
  await call.answer()
  await call.message.delete()
  await call.message.answer('Вы вышли, нажмите /start, чтобы начать заново')
  await state.finish()
  

@dp.message_handler(commands=['admin'])
async def admin(message: types.Message):
  if message.from_user.id == ADMIN_ID:
    await message.reply('Вы вошли в админ-панель, выберите функцию', reply_markup=admin_kb)
  else:
    await message.reply('Вам недоступна данная функция')
    return
  
@dp.callback_query_handler(lambda call: call.data == 'add_product')
async def add_products(call: types.CallbackQuery):
  await call.answer()
  await call.message.reply('Выберите товар к которому вы хотите добавить товар', reply_markup=buy_kb)
  await Form.add.set()

@dp.callback_query_handler(lambda call: call.data in ['wind', 'zip', 'tshirt', 'shorts', 'shoes', 'other'], state=Form.add)
async def buy_list_add(call: types.CallbackQuery, state: FSMContext):
  await state.update_data(category= call.data)
  await call.answer()
  if call.data == 'wind':
    await call.message.answer('Выберите конкретную ветровку', reply_markup=winds_kb)
  elif call.data == 'zip':
    await call.message.answer('Выберите конкретную зипку', reply_markup=zips_kb)
  elif call.data == 'tshirt':
    await call.message.answer('Выберите конкретную футболку', reply_markup=tshirts_kb)
  elif call.data == 'shorts':
    await call.message.answer('Выберите конкретную штаны/шорты', reply_markup=shorts_kb)
  elif call.data == 'shoes':
    await call.message.answer('Выберите конкретную обувь', reply_markup=shoes_kb)
  elif call.data == 'other':
    await call.message.answer('Выберите конкретное другое', reply_markup=other_kb)

@dp.callback_query_handler(lambda call: call.data in buy_list, state=Form.add)
async def add_products(call: types.CallbackQuery, state: FSMContext):
  await call.answer()
  await state.update_data(product_code = call.data)
  product_code = call.data
  check = exist(product_code)
  if check is None:
    await call.message.answer('Отправьте фото товара для добавления')
    await Form.photo.set()
  else:
    await call.message.answer('Фото уже добавлено')
    await state.finish()

@dp.message_handler(content_types=['photo'], state=Form.photo)
async def add_photos(message: types.Message, state: FSMContext):
  data = await state.get_data()
  category = data['category']
  product_code = data['product_code']
  photo_id = message.photo[-1].file_id
  add_photo(category,product_code, photo_id)
  await message.answer('Фото добавлено')
  await state.finish()
  
#рассылка
@dp.callback_query_handler(lambda call: call.data == 'send_broadcast')
async def send(call: types.CallbackQuery):
  await call.answer()
  await call.message.answer('Ввыедите текст для рассылки')
  await Form.broadcast.set()

  @dp.message_handler(state=Form.broadcast)
  async def send_br(message: types.Message, state: FSMContext):
    user_id = get_user_id()
    success = 0
    fail = 0
    for users in user_id:
      try:
        await bot.send_message(users, message.text)
        success += 1
      except:
        fail += 1
    await message.answer(f'Рассылка завершена. Успешных: {success}, Неудачных: {fail}')
    await state.finish()

#статистика
@dp.callback_query_handler(lambda call: call.data == 'stat')
async def stat(call: types.CallbackQuery):
  await call.answer()
  users = get_stat()
  if not users:
        await call.message.answer('❌ Нет пользователей в базе.')
        return
  for user in users:
      await call.message.answer(f'🆔 ID: {user[0]}\n👤 Username: @{user[1]}\n📱 Telegram ID: {user[2]}')



#Панель польователей

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
  await message.reply("Приветствуем вас в боте iyoka_shop, пожалуйста выберите функцию, которую вам нужна", reply_markup=user_kb)
  username = message.from_user.username
  telegram_id = message.from_user.id
  if username is None:
    username = 'Без username'
    return username
  else:
    pass
  add_user(telegram_id, username)

#buy
@dp.callback_query_handler(lambda call: call.data == 'buy')
async def buy(call: types.CallbackQuery):
  await call.answer()
  await call.message.answer('Выберите категорию', reply_markup = buy_kb)
  await Form.buy_category.set()

@dp.callback_query_handler(lambda call: call.data in ['wind', 'zip', 'tshirt', 'shorts', 'shoes', 'other'], state=Form.buy_category)
async def buy_category(call: types.CallbackQuery, state: FSMContext):
  await call.answer()
  await state.update_data(category = call.data)
  if call.data == 'wind':
    await call.message.answer('Выберите ветровку', reply_markup = winds_kb)
  elif call.data == 'zip':
    await call.message.answer('Выберите зипку', reply_markup=zips_kb)
  elif call.data == 'tshirt':
    await call.message.answer('Выберите футболку', reply_markup=tshirts_kb)
  elif call.data == 'shorts':
    await call.message.answer('Выберите штаны/шорты', reply_markup=shorts_kb)
  elif call.data == 'shoes':
    await call.message.answer('Выберите обувь', reply_markup=shoes_kb)
  elif call.data == 'other':
    await call.message.answer('Выберите другое', reply_markup=other_kb)

@dp.callback_query_handler(lambda call: call.data in buy_list, state=Form.buy_category)
async def buy_product(call: types.CallbackQuery, state: FSMContext):
  await call.answer()
  await state.update_data(product_code = call.data)
  product_code = call.data
  check = exist(product_code)
  data = await state.get_data()
  category = data['category']
  product_code = data['product_code']
  photo_id = get_photo(category,product_code)

  if check is None:
    await call.message.answer('❌ Фото товара ещё не добавлено.')
    return
    
  else:
    await bot.send_photo(call.from_user.id, photo_id[0], caption=('Товар: ' + category + ' ' + product_code + 'Для заказа напишите @username'))
    return        
  


#Фотопоиск

@dp.callback_query_handler(lambda call: call.data == 'photo_search')
async def photo_s(call: types.CallbackQuery):
  await call.answer()
  await Form.phoso_searcher.set()
  await call.message.answer('Пожалуйста, отправьте нам фотографию вещи, которую вы хотите найти, или напишите название и оно будет отправлено в личные сообщения продавцу @feaagff')

@dp.message_handler(content_types=['photo'], state=Form.phoso_searcher)
async def photo_s(message: types.Message, state: FSMContext):
  file_id = message.photo[-1].file_id
  username = message.from_user.username
  user_id = message.from_user.id
  await state.update_data(photo = file_id)
  await message.answer('Спасибо, фотография отправлена продавцу, либо вы можете написать ему сами - @feaagff ')
  await bot.send_photo(ADMIN_ID, caption= f'Клиент @{username}, {user_id} выбрал фукнцию "Фотопоиск" и отправил нам фотографию. Фото:''', photo = file_id)
  await state.finish()





#обработка текста



@dp.message_handler(content_types=['text'], state=Form.phoso_searcher)
async def text_s(message: types.Message, state: FSMContext):
  text = message.text
  username = message.from_user.username
  user_id = message.from_user.id
  await state.update_data(text = message.text)
  await bot.send_message(ADMIN_ID, f'Клиент @{username}, {user_id} выбрал фукнцию "Фотопоиск" и написал нам текст. Текст: {text}''')
  await message.answer('Спасибо, текст отправлен продавцу, либо вы можете написать ему сами - @feaagff ')
  await state.finish()
@dp.message_handler(content_types=['text'])
async def emty(message: types.Message):
  await message.reply('Я вас не понимаю, нажмите /start чтобы начать работу')


#Помощь



@dp.callback_query_handler(lambda call: call.data == 'help')
async def help(call: types.CallbackQuery):
  await call.answer()
  await call.message.answer('''Для покупки товара нажмите кнопку "Купить" и выберите товар, который вам нужен.
 \n Также в нем вы можете посмотреть цену и фотографии.
 \n По любым вопросам пишите @feaagff''')
  
if __name__ == '__main__':
  executor.start_polling(dp, skip_updates=True)

