from vkbottle.bot import Bot, Message
from vkbottle.tools import Keyboard
import sqlite3, random

privs = {0: ['Стандартный игрок', '', 0], 1: ['VIP', '(Bronze)', 500], 2: ['VIP', '(Silver)', 800], 3: ['VIP', '(Gold)', 1200]}

async def select(user_id):
    return sqlite3.connect('base.sql').cursor().execute(f'SELECT * FROM users WHERE user_id = {user_id}').fetchone()

async def update(user_id, col, val):
    con = sqlite3.connect('base.sql')
    c = con.cursor()
    c.execute(f'UPDATE users SET {col} = {val} WHERE user_id = {user_id}')
    con.commit()
    return

async def insert(user_id):
    con = sqlite3.connect('base.sql')
    c = con.cursor()
    c.execute(f'INSERT INTO users(user_id) VALUES({user_id})')
    con.commit()
    return

async def check_reg(user_id):
    if (await select(user_id)) is None:
        await insert(user_id)
        return
    return

async def MAIN_keyboard():
    k = Keyboard(True, False)
    k.schema([[{'type': 'text', 'label': 'Клик', 'color': 'positive'}],
              [{'type': 'text', 'label': 'Профиль', 'color': 'positive'},
               {'type': 'text', 'label': 'Баланс', 'color': 'positive'}],
              [{'type': 'text', 'label': 'Магазин', 'color': 'positive'},
               {'type': 'text', 'label': 'Казино', 'color': 'positive'}],
              [{'type': 'text', 'label': 'Вывод', 'color': 'positive'},
               {'type': 'text', 'label': 'Помощь', 'color': 'negative'}]])
    return k.get_json()

async def SUMMES_keyboard():
    k = Keyboard(True, False)
    k.schema([[{'type': 'text', 'label': '50', 'color': 'positive'},
               {'type': 'text', 'label': '100', 'color': 'positive'},
               {'type': 'text', 'label': '500', 'color': 'positive'}],
              [{'type': 'text', 'label': '1000', 'color': 'positive'},
               {'type': 'text', 'label': '5000', 'color': 'positive'},
               {'type': 'text', 'label': '10000', 'color': 'positive'}],
              [{'type': 'text', 'label': 'Назад', 'color': 'negative'}]])
    return k.get_json()

async def ADMIN_keyboard():
    k = Keyboard(True, False)
    k.schema([[{'type': 'text', 'label': 'выдать', 'color': 'positive'},
               {'type': 'text', 'label': 'отнять', 'color': 'negative'}],
              [{'type': 'text', 'label': 'выдать прив', 'color': 'positive'},
               {'type': 'text', 'label': 'отнять прив', 'color': 'negative'}]])
    return k.get_json()

bot = Bot(token='ac27ac317a0219e3f30ebf10f1c1a3a56e5ab8d55a08dd4420291efbc5787919d3fad99db9c2ae0517632')

@bot.on.message(text=['профиль', "ПРОФИЛЬ", "Профиль", "проф", "ПРОФ", "Проф"])
async def HANDLER_profile(msg: Message):
    await check_reg(msg.from_id)
    await msg.answer(f'&#128100; > Ваш профиль:'
                     f'\n&#127380; > Ваш игровой айди: {(await select(msg.from_id))[0]}'
                     f'\n&#128176; > Ваш баланс: {(await select(msg.from_id))[2]} VK Coin'
                     f'\n&#128433; > За клик: {(await select(msg.from_id))[4]}'
                     f'\n&#127915; > Привелегия: {privs.get((await select(msg.from_id))[3])[0]}'
                     f'{privs.get((await select(msg.from_id))[3])[1]}',
                     keyboard=(await MAIN_keyboard()))
    return

@bot.on.message(text=['баланс', "БАЛАНС", "Баланс"])
async def HANDLER_balance(msg: Message):
    await check_reg(msg.from_id)
    await msg.answer(f'&#128176; > {(await select(msg.from_id))[2]} VK Coin!',
                     keyboard=(await MAIN_keyboard()))
    return

@bot.on.message(text=['магазин', "МАГАЗИН", "Магазин"])
async def HANDLER_magazine(msg: Message):
    await check_reg(msg.from_id)
    await msg.answer(f'&#128722; > Мои товары: '
                     f'\n&#129353; > Bronze - 15 руб / + 500 к клику + VIP'
                     f'\n&#129352; > Silver - 30 руб / + 800 к клику + VIP'
                     f'\n&#129351; > Gold = 70 руб / + 1200 к клику + VIP'
                     f'\n&#8505; > Для покупки товара писать [sanitar_iz_dyrki_dyrka|нашему админу]!',
                     keyboard=(await MAIN_keyboard()))
    return

@bot.on.message(text=['казино', "КАЗИНО", "Казино"])
async def HANDLER_kazino(msg: Message):
    await check_reg(msg.from_id)
    await update(msg.from_id, 'last_com', 10)
    await msg.answer(f'&#127920; > Выберете ставку!',
                     keyboard=(await SUMMES_keyboard()))
    return

@bot.on.message(text=['клик', "КЛИК", "Клик"])
async def HANDLER_cry(msg: Message):
    await check_reg(msg.from_id)
    await update(msg.from_id, 'balance', (await select(msg.from_id))[2] + ((await select(msg.from_id))[4] + privs.get((await select(msg.from_id))[3])[2]))
    await msg.answer(f'&#128433; > Вы получили {(await select(msg.from_id))[4] + privs.get((await select(msg.from_id))[3])[2]} VK Coin!',
                     keyboard=(await MAIN_keyboard()))
    return

@bot.on.message(text=['вывод', "ВЫВОД", "Вывод"])
async def HANDLER_vivod(msg: Message):
    await check_reg(msg.from_id)
    await msg.answer(f'&#8505; > Для вывода писать [sanitar_iz_dyrki_dyrka|нашему админу]!',
                     keyboard=(await MAIN_keyboard()))
    return

@bot.on.message(text=['репорт', "РЕПОРТ", "Репорт"])
async def HANDLER_report(msg: Message):
    await check_reg(msg.from_id)
    await msg.answer(f'&#8505; > Репорт - писать [sanitar_iz_dyrki_dyrka|нашему админу]!',
                     keyboard=(await MAIN_keyboard()))
    return

@bot.on.message(text=["помощь", "ПОМОЩЬ", "Помощь",
                      "команды", "КОМАНДЫ", "Команды",
                      "меню", "МЕНЮ", "Меню"])
async def HANDLER_help(msg: Message):
    await check_reg(msg.from_id)
    await msg.answer(f'&#8505; > Мои команды:'
                     f'\n&#8505; > Профиль - просмотр профиля'
                     f'\n&#8505; > Баланс - просмотр баланса'
                     f'\n&#8505; > Казино - игра в казино'
                     f'\n&#8505; > Помощь - команды бота'
                     f'\n&#8505; > Магазин - магазин'
                     f'\n&#8505; > Вывод - вывод VK Coin'
                     f'\n&#8505; > Репорт - связь с админом',
                     keyboard=(await MAIN_keyboard()))
    return

@bot.on.private_message(text=['админ панель', 'АДМИН ПАНЕЛЬ', 'Админ панель'])
async def HANDLER_adminpanel(msg: Message):
    await msg.answer('&#128312; > Команды админа: ',
                     keyboard=(await ADMIN_keyboard()))

@bot.on.private_message(text='выдать')
async def HANDLET_vidat(msg: Message):
    await update(msg.from_id, 'last_com', 20)
    await msg.answer('&#128313; > Введите игровой айди пользователя: ')

@bot.on.private_message(text='отнять')
async def HANDLET_otnat(msg: Message):
    await update(msg.from_id, 'last_com', 30)
    await msg.answer('&#128313; > Введите игровой айди пользователя: ')

@bot.on.private_message(text='выдать прив')
async def HANDLET_vidatpriv(msg: Message):
    await update(msg.from_id, 'last_com', 40)
    await msg.answer('&#128313; > Введите игровой айди пользователя: ')

@bot.on.private_message(text='отнять прив')
async def HANDLET_otnatpriv(msg: Message):
    await update(msg.from_id, 'last_com', 50)
    await msg.answer('&#128313; > Введите игровой айди пользователя: ')

@bot.on.message()
async def HANDLER_order(msg: Message):
    await check_reg(msg.from_id)
    if msg.text in ['50', '100', '500', '1000', '5000', '10000'] and (await select(msg.from_id))[-1] == 10:
        if (await select(msg.from_id))[2] < int(msg.text):
            await msg.answer(f'&#128219; > Ставка больше баланса!',
                             keyboard=(await MAIN_keyboard()))
            await update(msg.from_id, 'last_com', 0)
            return
        await update(msg.from_id, 'balance', (await select(msg.from_id))[2] - int(msg.text))
        rand = random.randint(1, 100)
        if rand <= 30:
            await update(msg.from_id, 'balance', (await select(msg.from_id))[2] + int(msg.text) * 2)
            await msg.answer(f'&#129535; > Вам выпал х2!\n'
                             f'&#128176; > Ваш баланс: {(await select(msg.from_id))[2]} VK Coin',
                             keyboard=(await MAIN_keyboard()))
        elif rand <= 70:
            await update(msg.from_id, 'balance', (await select(msg.from_id))[2] + int(msg.text) * 1)
            await msg.answer(f'&#129535; > Вам выпал х1!\n'
                             f'&#128176; > Ваш баланс: {(await select(msg.from_id))[2]} VK Coin',
                             keyboard=(await MAIN_keyboard()))
        else:
            await update(msg.from_id, 'balance', (await select(msg.from_id))[2] + int(msg.text) * 0)
            await msg.answer(f'&#129535; > Вам выпал х0!\n'
                             f'&#128176; > Ваш баланс: {(await select(msg.from_id))[2]} VK Coin',
                             keyboard=(await MAIN_keyboard()))
        await update(msg.from_id, 'last_com', 0)
        return
    elif (await select(msg.from_id))[-1] == 20:
        if sqlite3.connect('base.sql').cursor().execute(f'SELECT * FROM users WHERE id = {int(msg.text)}').fetchone() is None:
            await msg.answer('&#128312; > Нет игрока с таким айди!',
                             keyboard=(await MAIN_keyboard()))
            await update(msg.from_id, 'last_com', 0)
            return
        else:
            await update(msg.from_id, 'uid', int(msg.text))
            await update(msg.from_id, 'last_com', 21)
            await msg.answer('&#128313; > Введите сумму: ')
    elif (await select(msg.from_id))[-1] == 21:
        await update(sqlite3.connect('base.sql').cursor().execute(f'SELECT * FROM users WHERE id = {int((await select(msg.from_id))[5])}').fetchone()[1], 'balance', sqlite3.connect('base.sql').cursor().execute(f'SELECT * FROM users WHERE id = {int((await select(msg.from_id))[5])}').fetchone()[2] + int(msg.text))
        await msg.answer('&#128312; > Операция завершена!',
                         keyboard=(await MAIN_keyboard()))
        await update(msg.from_id, 'last_com', 0)
    elif (await select(msg.from_id))[-1] == 30:
        if sqlite3.connect('base.sql').cursor().execute(f'SELECT * FROM users WHERE id = {int(msg.text)}').fetchone() is None:
            await msg.answer('&#128312; > Нет игрока с таким айди!',
                             keyboard=(await MAIN_keyboard()))
            await update(msg.from_id, 'last_com', 0)
            return
        else:
            await update(msg.from_id, 'uid', int(msg.text))
            await update(msg.from_id, 'last_com', 31)
            await msg.answer('&#128313; > Введите сумму: ')
    elif (await select(msg.from_id))[-1] == 31:
        await update(sqlite3.connect('base.sql').cursor().execute(f'SELECT * FROM users WHERE id = {int((await select(msg.from_id))[5])}').fetchone()[1], 'balance', sqlite3.connect('base.sql').cursor().execute(f'SELECT * FROM users WHERE id = {int((await select(msg.from_id))[5])}').fetchone()[2] - int(msg.text))
        await msg.answer('&#128312; > Операция завершена!',
                         keyboard=(await MAIN_keyboard()))
        await update(msg.from_id, 'last_com', 0)

    elif (await select(msg.from_id))[-1] == 40:
        if sqlite3.connect('base.sql').cursor().execute(f'SELECT * FROM users WHERE id = {int(msg.text)}').fetchone() is None:
            await msg.answer('&#128312; > Нет игрока с таким айди!',
                             keyboard=(await MAIN_keyboard()))
            await update(msg.from_id, 'last_com', 0)
            return
        else:
            await update(msg.from_id, 'uid', int(msg.text))
            await update(msg.from_id, 'last_com', 41)
            await msg.answer('&#128313; > Введите номер привелегии(1 - bronze, 2 - silver, 3 - gold): ')
    elif (await select(msg.from_id))[-1] == 41:
        await update(sqlite3.connect('base.sql').cursor().execute(f'SELECT * FROM users WHERE id = {int((await select(msg.from_id))[5])}').fetchone()[1], 'priv', int(msg.text))
        await msg.answer('&#128312; > Операция завершена!',
                         keyboard=(await MAIN_keyboard()))
        await update(msg.from_id, 'last_com', 0)
    elif (await select(msg.from_id))[-1] == 50:
        if sqlite3.connect('base.sql').cursor().execute(f'SELECT * FROM users WHERE id = {int(msg.text)}').fetchone() is None:
            await msg.answer('&#128312; > Нет игрока с таким айди!',
                             keyboard=(await MAIN_keyboard()))
            await update(msg.from_id, 'last_com', 0)
            return
        else:
            await update(msg.from_id, 'uid', int(msg.text))
            await update(msg.from_id, 'last_com', 0)
            await update(sqlite3.connect('base.sql').cursor().execute(
                f'SELECT * FROM users WHERE id = {int((await select(msg.from_id))[5])}').fetchone()[1], 'priv', 0)
            await msg.answer('&#128312; > Операция завершена!',
                             keyboard=(await MAIN_keyboard()))
            return
    await msg.answer('&#128219; > Нет такой команды!',
                     keyboard=(await MAIN_keyboard()))
    return

bot.run_forever()