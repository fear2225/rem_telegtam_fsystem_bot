__version__ = '1.2.0'
__author__ = 'https://github.com/fear2225'
__doc__ = '[*] Remote access to computer file system\n'\
        '[!] if you try to enter directories with restricted access,'\
        'it may cause an error, go back to the /root directory'\
        'commands:\n'\
        '/start - start with root dir & show user id\n'\
        '/root - return to root dir\n'\
        '/help - show this message'\
        'config:\n'\
        '[!] for proper operation, it must be used by one user at a time\n'\
        '[!] Do not change sequence of lines!!!\n'\
        '[!] Var and data should be separated by "=" or "= "\n'\
        '[!] Path example: "root=C:\\Users\\"\n'\
        '[!] Whitelist should contain users id divided by "," or be blank\n'


# Internal
import asyncio
import sys

from pathlib import Path

from aiogram import Bot, Dispatcher, types, executor
from aiogram.types import Message, CallbackQuery
from aiogram.types.input_file import InputFile
from aiogram.types import InlineKeyboardMarkup as ilMarkup, InlineKeyboardButton as ilButton

# External

# ========================================

def config_unpack():
    '''unpack clear param in the order of their declaration'''
    print(f'[*] main.py location: {sys.argv[0]}')
    _temp = []
    with open(sys.argv[0][0:-7]+'config.txt','r') as f:
        for line in f:
            _temp.append(line.strip().split(sep='=', maxsplit=1)[1])
    return _temp

# todo whitelist by user.id
# Global parameters
TOKEN, ROOT, FILE_NAME_WIDTH, N_BUTTONS, WALIST = config_unpack()
ROOT = Path(ROOT)
FILE_NAME_WIDTH = int(FILE_NAME_WIDTH)
N_BUTTONS = int(N_BUTTONS)
work_path = ROOT
TO_DEL = 0
FILE_ROW = 0
CALLBACK_LIST_TEMP = []


# ========================================
# Whitelist
def WhiteList() -> None:
    global WALIST

    if len(WALIST) == 0:
        WALIST = False
        return None

    WALIST = WALIST.split(sep=',')
    for i, _ in enumerate(WALIST):
        WALIST[i] = WALIST[i].strip()
        if (len(WALIST[i]) < 5):
            print('[!] Wrong parameters in whitelist')
            print(WALIST)
            sys.exit()
    return None


def WhitelistCheck(*args) -> bool:
    global WALIST
    if WALIST == False:
        return True

    if args in WALIST:
        return True
    return False


# TODO сделать вывод всех файлов и папок
# TODO без ебаного деления
# ========================================
bot = Bot(token=TOKEN)
dp = Dispatcher(bot=bot)



def command_up(path:Path, root=ROOT) -> Path:
    '''go to parent dierctory'''
    if path == path.parent or path <= root:
        return path
    else:
        return path.parent


def nameShorts(text:Path, max=20) -> list:
    '''Shorts for telegram`s callback in InLineKeyboard'''
    if max < 10:
        max = 10

    if len(text.name) <= max:
        return [str(text.name),
                str(text)]
    else:
        n = max//2
        return [str(text.name)[:n-1] + '...' + str(text.name)[-(n-2):],
                str(text)]


def list_dir(path:Path) -> list:
    _temp = []
    for i in path.iterdir():
        _temp.append(i)
    return _temp


def create_keyboard() -> ilMarkup:
    global work_path, N_BUTTONS,  FILE_ROW, FILE_NAME_WIDTH
    global CALLBACK_LIST_TEMP
    keyboard = ilMarkup(row_width=1)
    paths_to_show = list_dir(path=work_path)

    # Store table of callback`s and path`s
    CALLBACK_LIST_TEMP = []

    ROW = len(paths_to_show)//N_BUTTONS
    if  (ROW - FILE_ROW) <= 0:
        FILE_ROW = 0

    poz = 0
    if paths_to_show:

        for i in paths_to_show[FILE_ROW*N_BUTTONS:(FILE_ROW+1)*N_BUTTONS]:
            i = nameShorts(text=i, max=FILE_NAME_WIDTH)
            CALLBACK_LIST_TEMP.append(i[1])
            keyboard.add(ilButton(text=i[0], callback_data=poz))
            poz += 1


        if (ROW-1) > 0:
            keyboard.add(ilButton(text='next ==>', callback_data='/next'))

    keyboard.add(ilButton(text='^^^ UP ^^^', callback_data='/up'))

    return keyboard


async def to_del() -> None:
    global bot, TO_DEL
    # TODO не работает
    chat_id:int = 0
    if isinstance(TO_DEL, Message):
        chat_id = TO_DEL['chat']['id']
    elif isinstance(TO_DEL, CallbackQuery):
        chat_id = TO_DEL['chat']['id']
    elif isinstance(TO_DEL, int):
        return None
    else:
        print('[!] Wrong TO_DEL type')
        return None

    try:
        await bot.delete_message(chat_id=chat_id,
                                message_id=TO_DEL.message_id)
    except:
        print(f'[!] Failed to delete message: {type(TO_DEL)}\n{TO_DEL}')


@dp.message_handler(commands=['start', 'root', 'help', 'list', 'ver', 'off'])
async def show_data(message: Message) -> None:
    global bot, TO_DEL, WALIST
    global work_path

    if not WhitelistCheck(str(message.from_user.id)):
        print(f'[!] Denied! {message.from_user.id}')
        return None

    if message.text == '/off':
        await message.answer(text='Shutdow')
        print('[*] Turned off by command')
        sys.exit()
        return None

    if message.text == '/help':
        await message.answer(text=__doc__)
        return None

    if message.text == '/ver':
        await message.answer(text=__version__)
        return None

    await to_del()

    reply_text = ''

    if message.text == '/start':
        reply_text = f'user: {message.from_user.id}\n'

    if message.text == '/root':
        work_path = Path(Path.cwd())



    if message.text == '/list':
        reply_text += f'Whitelisted users: {WALIST}\n'

    # add keyboard
    reply_text += f'path: {work_path}'

    keyboard = create_keyboard()
    TO_DEL = await message.answer(text=reply_text, reply_markup=keyboard)


@dp.callback_query_handler()
async def callback_navigate(call:CallbackQuery) -> None:
    global bot, TO_DEL
    global work_path
    global FILE_ROW
    # todo круговой row
    # todo del

    await to_del()

    if call.data == '/up':
        work_path = command_up(path=work_path, root=ROOT)
        print('[^^]', work_path)
        FILE_ROW = 0

    elif call.data == '/next':
        FILE_ROW += 1

    else:
        CallbackPath = Path(CALLBACK_LIST_TEMP[int(call.data)])
        if CallbackPath.is_dir():
            work_path = CallbackPath
            print('[vv]', CallbackPath)
        elif CallbackPath.is_file():
            print('[=>]', CallbackPath.as_posix())
            await bot.send_document(chat_id=call.from_user.id,
                                    document=InputFile((CallbackPath.as_posix()))
                                    )
        else:
            print('Error file type')

    keyboard = create_keyboard()
    # todo error button linit 64 byte
    TO_DEL = await bot.send_message(text=f'path: {work_path}',
                                    chat_id=call.from_user.id,
                                    reply_markup=keyboard)



def main():
    executor.start_polling(dp, skip_updates=True)


if __name__ == '__main__':
    print('[*] Initialisation complete')
    print(f'[*] Start path: {str(work_path)}')
    print(f'[*] Root path: {str(ROOT)}')
    WhiteList()
    if not WALIST:
        print(f'[*] Whitelist enable :{WALIST}')
    else:
        print(f'[*] Whitelist users {len(WALIST)}: {WALIST}')

    # asyncio.run(main())
    main()

    print('[*] Bot has stopped')
