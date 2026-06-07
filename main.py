import asyncio
from aiogram import F, Bot, Dispatcher,types
from aiogram.types import BufferedInputFile
from aiogram.filters import Command
import requests

dp = Dispatcher()

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    kb = [
        [types.KeyboardButton(text="Факти про котів"),
         types.KeyboardButton(text="Лисиці")],
        [types.KeyboardButton(text="Курс Валют"),
         types.KeyboardButton(text="Погода")],
        [types.KeyboardButton(text="Повітряна Тривога")]
    ]
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
    await message.answer("Натисніть на будь-яку кнопку", reply_markup=keyboard)

@dp.message(F.text == "Факти про котів")
async def get_cat_facts (message: types.Message):
    response = requests.get("https://meowfacts.herokuapp.com/?lang=ukr")
    response_image = requests.get("https://cataas.com/cat")
    fact = response.json().get("data")[0]
    cat_photo = BufferedInputFile(response_image.content,filename="cat.jpg")
    await message.answer_photo(photo=cat_photo, caption=f"Цікавий факт: {fact}")

@dp.message(F.text == "Лисиці")
async def get_fox_facts (message: types.Message):
    response = requests.get("https://randomfox.ca/floof")
    fox = response.json().get("image")
    await message.answer_photo(photo=fox,caption="Лисичка")

@dp.message(F.text == "Курс Валют")
async def money_facts (message: types.Message):
    url = "https://api.privatbank.ua/p24api/pubinfo?exchange&coursid=5"
    response = requests.get(url)
    data = response.json()
    for item in data:
        if item.get("ccy") == "USD":
            usdBuy = item.get("buy")
            usdSell = item.get("sale")
        elif item.get("ccy") == "EUR":
            eurBuy = item.get("buy")
            eurSell = item.get("sale")
    await message.answer(f"Курс валют (ПриватБанк)\n\n"
                         f"USD (Долар) \n"
                         f"Купівля: {usdBuy} $ | Продаж: {usdSell} $ \n\n"
                         f"EUR (Евро) \n"
                         f"Купівля: {eurBuy} € | Продаж: {eurSell} € \n\n")

@dp.message(F.text == "Погода")
async def weather_fact (message: types.Message):
    response = requests.get("https://api.open-meteo.com/v1/forecast?latitude=48.4675&longitude=35.0407&current=temperature_2m,relative_humidity_2m,wind_speed_10m,precipitation")
    data = response.json()
    curWeather = data.get("current")
    temp = curWeather.get("temperature_2m")
    huma = curWeather.get("relative_humidity_2m")
    wind = curWeather.get("wind_speed_10m")
    precip = curWeather.get("precipitation")
    await message.answer(f"Погода Дніпро\n\n"
                         f"Температура: {temp} °C\n"
                         f"Волога: {huma}% \n"
                         f"Швидкість вітра: {wind} км/год \n"
                         f"Імовірність опадів: {precip}%")

@dp.message(F.text == "Повітряна Тривога")
async def Alarm (message: types.Message):
    response = requests.get("https://sirens.in.ua/api/v1/")
    Dnipro = response.json().get("Dnipropetrovs'k")
    if Dnipro == "full":
        await message.answer("‼️Зараз ПОВІТРЯНА тривога в Дніпропетровській області. Перейдіть в укриття ‼️")
    elif Dnipro is None:
        await message.answer("✅ Зараз НЕМАЄ повітряної тривоги в Дніпропетровській області ✅")
    elif Dnipro == "partial" :
        await message.answer("⚠️ Зараз ЧАСТКОВА повітряна тривога в Дніпропетровській області ⚠️")
    else:
        await message.answer("Нема інформації")

async def main():
    token = "YOUR_TOKEN_HERE"
    if not token:
        error = "No token provided"
        raise ValueError(error)
    bot = Bot(token=token)

    print("Started")
    try:
        await dp.start_polling(bot)
    finally:
        print("Bot stopped")

#Hi! Created by Denys Chesnokov for the Final Project at IT Step.

if __name__ == '__main__':
    asyncio.run(main())