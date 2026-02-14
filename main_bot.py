import logging 
import asyncio
from aiogram import Bot, Dispatcher, F, types
from aiogram.filters.command import Command
from config_reader import config 
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

logging.basicConfig(level=logging.INFO)
bot = Bot(token=config.bot_token.get_secret_value())
dp = Dispatcher()

class lobby(StatesGroup):
    user_name = State()

group = []

@dp.message(Command('start'))
async def cmd_start(message: types.Message):
    await message.answer('Hello, bro)')
    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(
        text='create new lobby',
        callback_data='create_new'
    ))
    builder.row(types.InlineKeyboardButton(
        text='check old lobby',
        callback_data='check_old'
    ))
    await message.answer('What do you want to do?', reply_markup=builder.as_markup())

@dp.callback_query(F.data == 'create_new')
async def cmd_create_new_lobby(callback: types.CallbackQuery):
    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(
        text='add user',
        callback_data='add'
    ))
    builder.row(types.InlineKeyboardButton(
        text='thats all',
        callback_data='stop'
    ))
    await callback.message.answer('Choose the action with the group', reply_markup=builder.as_markup())
    await callback.answer()
    await callback.message.answer('Press "add" and enter users name:')


@dp.callback_query(F.data == 'add')
async def cmd_add(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(lobby.user_name)
    await callback.answer()


@dp.callback_query(F.data == 'stop')
async def cmd_stop(callback: types.CallbackQuery):
    s = ', '.join(group)
    await callback.message.answer(f'Члены группы: {s}')
    await callback.answer()

@dp.message(lobby.user_name)
async def cmd_halder(message: types.Message, state: FSMContext):
    await state.update_data(user_name=message.text)
    data = await state.get_data()
    group.append(data['user_name'])


async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())