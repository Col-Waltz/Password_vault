import time
import logging

import asyncio
from contextlib import suppress
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.utils.exceptions import MessageCantBeDeleted,MessageToDeleteNotFound

class Input(StatesGroup):
    organization = State()
    login = State()
    password = State()
    choise = State()
    apply = State()

class Output(StatesGroup):
    input = State()

class Delete(StatesGroup):
    input = State()
    choise = State()

storage = MemoryStorage()

mytoken = '6079387099:AAF_KWTYyYOp6NDJ7pv6Bn6zirlrqQ71Amc'
bot = Bot(token = mytoken)
dp = Dispatcher(bot = bot, storage = storage)
Users={} #{'user_id': {'Service_name': ['login','password']}}
entertext='В главном меню доступны команды: \
    \n /set - добавление или изменение логина и пароля по названию сервиса\
    \n /get - получение логина и пароля по названию сервиса\
    \n /all - получение всех сервисов для которых были сохранены логины пароли\
    \n /del - удаление записи о выбранном сервисе\
    \n /help - вызов данного окна'

async def delete_message(message: types.Message, seconds: int = 0):
    await asyncio.sleep(seconds)
    with suppress(MessageCantBeDeleted,MessageToDeleteNotFound):
        await message.delete()

@dp.message_handler(commands=['start'])
async def start_handler(message: types.Message):
    user_id = message.from_user.id
    username = message.from_user.full_name
    logging.info(f'{user_id}{username}{time.asctime()}')
    if user_id not in Users:
        Users[user_id]={}
        await message.answer(f'Здравствуйте, {username}!')
    else:
        await message.answer(f'С возвращением, {username}!')
    await message.answer(entertext)

@dp.message_handler(commands = ['set'], state = None)
async def set_new_service(message: types.Message):
    await message.answer('Введите название сервиса, пароль от которого хотите сохранить: ')
    await Input.organization.set()

@dp.message_handler(state = Input.organization)
async def organization_input(message: types.Message, state: FSMContext):
    user_id=message.from_user.id
    org_name=message.text
    if org_name in Users.get(user_id):
        await message.answer('В базе уже есть логин пароль от этого сервиса, хотите заменить? Да/Нет')
        await state.update_data({ 'organization' : org_name })
        await Input.choise.set()
    else:
        await state.update_data({ 'organization' : org_name })
        await message.answer('Введите логин')
        await Input.login.set()
    
@dp.message_handler(state=Input.choise)
async def choise(message: types.Message, state: FSMContext):
    answer = message.text
    if answer == 'Да' or answer == 'да':
        await message.answer('Введите логин')
        await Input.login.set()
    elif answer == 'Нет' or answer == 'нет':
        await message.answer('Возврат в главное меню')
        await state.finish()

@dp.message_handler(state=Input.login)
async def set_new_login(message: types.Message, state: FSMContext):
    login = message.text
    await state.update_data({ 'login' : login })
    await message.answer('Введите пароль')
    await Input.password.set()
    
@dp.message_handler(state=Input.password)
async def set_new_password(message: types.Message, state: FSMContext):
    password = message.text
    await state.update_data({ 'password' : password })
    await message.answer('Проверьте введенные данные еще раз и если все верно напишите: Подтвердить, в ином случае напишите:Сброс')
    await Input.apply.set()

@dp.message_handler(state=Input.apply)
async def set_new_tuple(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    answer = message.text
    if answer in ['Подтвердить','подтвердить']:
        data = await state.get_data()
        Users[user_id].update({data['organization']:[data['login'],data['password']]})
        await message.answer('Данные сохранены')
        await state.finish()
    if answer in ['Сброс','сброс']:
        await message.answer('Возврат в главное меню')
        await state.finish()

@dp.message_handler(commands=['get'], state = None)
async def check_tuples(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    if len(Users[user_id]) == 0:
        await message.answer('У вас пока нет ни одного сохраненного пароля')
    else:
        await message.answer('Введите название сервиса, от которого необходимо узнать пароль')
        await Output.input.set()

@dp.message_handler(state=Output.input)
async def output(message: types.Message,state: FSMContext):
    user_id = message.from_user.id
    org_name = message.text
    if org_name in Users[user_id].keys():
        message = await message.answer(f"Логин:{Users.get(user_id).get(org_name)[0]} \n Пароль:{Users.get(user_id).get(org_name)[1]} \n Это сообщение будет удалено в течение минуты, скопируйте логин и пароль в буфер обмена")
        asyncio.create_task(delete_message(message, 60))
    else:
        await message.answer('Сохраненного пароля для такого сервиса не существует, попробуйте использовать /all, чтобы узнать все сервисы, пароли от которых сохранены')
    await state.finish()

@dp.message_handler(commands=['del'], state = None)
async def check_tuples(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    if len(Users[user_id]) == 0:
        await message.answer('У вас пока нет ни одного сохраненного пароля')
    else:
        await message.answer('Введите название сервиса, пароль от которого необходимо удалить')
        await Delete.input.set()

@dp.message_handler(state = Delete.input)
async def check_tuples(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    org_name = message.text
    if org_name in Users[user_id]:
        await state.update_data({ 'organization' : org_name })
        await message.answer('Вы точно хотите удалить информацию о данном сервисе? Да/Нет')
        await Delete.choise.set()
    else:
        await message.answer('Сохраненного пароля для такого сервиса не существует, попробуйте использовать /all, чтобы узнать все сервисы, пароли от которых сохранены')
        await state.finish()

@dp.message_handler(state = Delete.choise)
async def check_tuples(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    answer = message.text
    if answer in ['Да','да']:
        data = await state.get_data()
        Users[user_id].pop(data['organization'])
        await message.answer('Данные удалены')
        await state.finish()
    elif answer in ['Нет','нет']:
        await message.answer('Данные сохранены')
        await state.finish()

@dp.message_handler(commands=['all'])
async def check_tuples(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    if len(Users[user_id]) == 0:
        await message.answer('У вас пока нет ни одного сохраненного пароля')
    else:    
        await message.answer(f'Пароли сохранены для сервисов:')
        for orgs in Users[user_id].keys():
            await message.answer(orgs)
    
@dp.message_handler(commands = ['help'])
async def set_new_service(message: types.Message):
    await message.answer(entertext)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
