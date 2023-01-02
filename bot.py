from auth_data import token
from main import Yandex_weather
import random

from aiogram import Bot, Dispatcher, executor, types
from aiogram.types.reply_keyboard import ReplyKeyboardMarkup
from aiogram.dispatcher.filters import Text
from aiogram.utils.markdown import hbold, hlink
from aiogram.types import InputFile
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.contrib.fsm_storage.memory import MemoryStorage

answers = ['Спрашиваем метеорологов...', 'Танцуем с бубном...', "Шаманим хорошую погоду...", "Сверяемся со звездами..."]

condition = {'clear': '🌞', 'partly-cloudy': '🌤️', 'cloudy': '☁', 'overcast': '☁', 'drizzle': '⛅', 'light-rain': '🌦️',
             'rain': 'rain, на душе pain', 'moderate-rain': '🌧️', 'heavy-rain': '🌧️', 'continuous-heavy-rain': '🌧️',
             'showers': '🌧️', 'wet-snow': '❄', 'light-snow': '❄', 'snow': '🌨️', 'snow-showers': '🌨️', 'hail': '🧊',
             'thunderstorm': '🌪️', 'thunderstorm-with-rain': '⛈', 'thunderstorm-with-hail': '⛈'}

storage = MemoryStorage()
bot = Bot(token=token, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot, storage=storage)


class FSMInputName(StatesGroup):
    choose_city_week_forecast = State()
    choose_city_day_forecast = State()


@dp.message_handler(commands='start')
async def start(message: types.Message):
    week_forecast = 'Прогноз на неделю'
    now_forecast = 'Погода сейчас'
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(week_forecast, now_forecast)

    await message.answer("Выберите действие", reply_markup=keyboard)


# 1st button

@dp.message_handler(Text(equals="Прогноз на неделю"))
async def get(message: types.Message):
    # await state.set_state(FSMInputName.choose_city_week_forecast)
    await message.answer("Введите город")
    await FSMInputName.choose_city_week_forecast.set()


@dp.message_handler(state=FSMInputName.choose_city_week_forecast)
async def new(msg_: types.Message, state: FSMContext):
    await msg_.answer(random.choice(answers))

    weather = Yandex_weather(f'{msg_.text}')
    weather.geo_pos()
    weather.get_data()
    ms = weather.create_hist()

    picture = InputFile(f'Forecast for {msg_.text}_{ms}.png')

    await bot.send_photo(chat_id=msg_.chat.id, photo=picture)
    await msg_.answer(f'Прогноз на даты с {weather.date[0]} по {weather.date[6]}')
    await msg_.answer('Такие дела')
    await state.finish()


# # 2nd button

@dp.message_handler(Text(equals="Погода сейчас"))
async def get_data(message: types.Message):
    await message.answer("Введите город")
    await FSMInputName.choose_city_day_forecast.set()


@dp.message_handler(state=FSMInputName.choose_city_day_forecast)
async def new_data(msg: types.Message, state: FSMContext):
    await msg.answer(random.choice(answers))

    weather_now = Yandex_weather(f'{msg.text}')
    weather_now.geo_pos()
    weather_now.get_data()

    await msg.answer(f'Сейчас целых {weather_now.now_temp} °C! А ощущается как все {weather_now.feels_like} °C 💀\n'
                     f'На улице сейчас {condition.get(weather_now.condition)}')
    await msg.answer('Бот считает, что этого достаточно, чтобы остаться дома пить чай ☕')

    await state.finish()


def main():
    executor.start_polling(dp, skip_updates=True)  # launch bot


if __name__ == "__main__":
    main()
