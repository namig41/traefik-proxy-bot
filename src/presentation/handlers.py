import presentation.keyboard_buttons as keyboard_buttons
import presentation.text as text
from aiogram import (
    F,
    Router,
)
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import (
    CallbackQuery,
    Message,
)
from logic import (
    Client,
    User,
)
from presentation.states import (
    Del,
    DelConf,
    Gen,
)
from settings import config


router = Router()
admin_id = config.TELEGRAM_ADMIN_ID


@router.message(Command("start"))
async def start_handler(message: Message):
    text = (
        "🔰 <b>FlyNet VPN — надёжный щит для безопасного интернета</b> 🔑\n\n"
        "<b>Возможности:</b>\n"
        "• 🎥 Минимальные задержки 4K видео\n"
        "• 🔥 Без рекламы на YouTube\n"
        "• 🚀 Неограниченный трафик и высокая скорость\n"
        "• 🖥 Одновременное подключение до 3х устройств\n"
        "• 🔒 Анонимность и безопасность\n"
        "• ⚙️ Стабильная работа и простая настройка\n"
        "• ☝️ Подключение в пределах одного клика\n"
        "• 🌍 Доступ к сервисам по всему миру\n"
        "• 💲 Оплата удобным для вас способом"
    )

    await message.answer(text, reply_markup=keyboard_buttons.main_menu)


@router.callback_query(F.data == "main_menu")
async def menu_handler(clbck: CallbackQuery, state: FSMContext):
    await state.clear()
    if clbck.from_user.username == admin_id:
        await clbck.message.answer(
            text=text.MAIN_MENU, reply_markup=keyboard_buttons.admin_menu,
        )
    else:
        await clbck.message.answer(
            text=text.MAIN_MENU, reply_markup=keyboard_buttons.client_menu,
        )


@router.callback_query(F.data == "get_instructions")
async def get_instructions(clbck: CallbackQuery):
    await clbck.message.answer(
        text=text.INSTRUCTIONS, reply_markup=keyboard_buttons.instruction_menu,
    )


@router.callback_query(F.data == "add_client")
async def add_client(clbck: CallbackQuery, state: FSMContext):
    if clbck.from_user.username == admin_id:
        await clbck.message.answer(
            text=text.CLIENT_ID_AWAIT, reply_markup=keyboard_buttons.iexit_kb,
        )
        await state.set_state(Gen().typing_telegram_id)


@router.message(Gen.typing_telegram_id)
async def get_telegram_id(msg: Message, state: FSMContext):
    if msg.from_user.username == admin_id:
        tg_id = msg.text
        await state.update_data(chosen_id=tg_id)
        await msg.answer(
            text.CLIENT_LIMIT_AWAIT, reply_markup=keyboard_buttons.iexit_kb,
        )
        await state.set_state(Gen().typing_limit)


@router.message(Gen.typing_limit)
async def get_limit(msg: Message, state: FSMContext):
    if msg.from_user.username == admin_id:
        limit = msg.text
        if not limit.isnumeric():
            await state.clear()
            return await msg.answer(
                text.LIMIT_ERROR, reply_markup=keyboard_buttons.iexit_kb,
            )
        else:
            limit = int(limit)
            user_data = await state.get_data()
            tg_id = user_data["chosen_id"]
            User().create(user_id=tg_id, limit=limit)
            await msg.answer(
                text.USER_IS_CREATED, reply_markup=keyboard_buttons.iexit_kb,
            )
            await state.clear()


@router.callback_query(F.data == "delete_client")
async def del_client(clbck: CallbackQuery, state: FSMContext):
    if clbck.from_user.username == admin_id:
        await clbck.message.answer(
            text.CLIENT_ID_AWAIT, reply_markup=keyboard_buttons.iexit_kb,
        )
        await state.set_state(Del().typing_telegram_id)


@router.message(Gen.typing_telegram_id)
async def delete_telegram_id(msg: Message, state: FSMContext):
    if msg.from_user.username == admin_id:
        tg_id = msg.text
        User().delete(user_id=tg_id)
        await state.clear()


@router.callback_query(F.data == "create_config")
async def add_config(clbck: CallbackQuery):
    user_id = str(clbck.from_user.username)
    if User().get(user_id) is None:
        return await clbck.message.answer(
            text.user_not_defined,
            reply_markup=keyboard_buttons.iexit_kb,
        )
    if not User().allowed_to_create_client(user_id):
        return await clbck.message.answer(
            text.user_limit_exited,
            reply_markup=keyboard_buttons.iexit_kb,
        )
    client_id = Client().create(user_id=user_id)
    client = Client().get(client_id)
    uri = client.conn_str
    await clbck.message.answer(text=uri, reply_markup=keyboard_buttons.iexit_kb)


@router.callback_query(F.data == "delete_config")
async def delete_config(clbck: CallbackQuery, state: FSMContext):
    user_id = str(clbck.from_user.username)
    if User().get(user_id) is None:
        return await clbck.message.answer(
            text.user_not_defined,
            reply_markup=keyboard_buttons.iexit_kb,
        )
    if not User().allowed_to_create_client(user_id):
        return await clbck.message.answer(
            text.user_limit_exited,
            reply_markup=keyboard_buttons.iexit_kb,
        )
    await clbck.message.answer(
        text.config_id_await, reply_markup=keyboard_buttons.iexit_kb,
    )
    await state.set_state(DelConf().typing_conf_id)


@router.message(DelConf.typing_conf_id)
async def delete_config_id(msg: Message, state: FSMContext):
    conf_id = msg.text
    if not conf_id.isalnum():
        await state.clear()
        return await msg.answer(
            text.config_id_error, reply_markup=keyboard_buttons.iexit_kb,
        )
    else:
        client_id = msg.text
        if Client().get(client_id) is None:
            return await msg.answer(
                text.CLIENT_NOT_DEFINED, reply_markup=keyboard_buttons.iexit_kb,
            )
        Client().delete(client_id=client_id)
        await state.clear()
        await msg.answer(text.CONFIG_IS_DELETED, reply_markup=keyboard_buttons.iexit_kb)


@router.callback_query(F.data == "conf_list")
async def add_config_list(clbck: CallbackQuery):
    user_id = clbck.from_user.username
    client_ids = Client().get_by_user(str(user_id))
    if client_ids is None or not client_ids:
        return await clbck.message.answer(text=text.CONFIGS_NOT_FOUND)
    for client_id in client_ids:
        client = Client().get(client_id)
        uri = client.conn_str
        await clbck.message.answer(text=uri)


@router.callback_query(F.data == "instruction_ios")
async def get_ios_instruction(clbck: CallbackQuery):
    await clbck.message.answer(
        text=text.INSTRUCTION_IOS, reply_markup=keyboard_buttons.iexit_kb,
    )


@router.callback_query(F.data == "instruction_android")
async def get_android_instruction(clbck: CallbackQuery):
    await clbck.message.answer(
        text=text.INSTRUCTION_ANDROID, reply_markup=keyboard_buttons.iexit_kb,
    )


@router.callback_query(F.data == "instruction_macos")
async def get_macos_instruction(clbck: CallbackQuery):
    await clbck.message.answer(
        text=text.INSTRUCTION_MACOS, reply_markup=keyboard_buttons.iexit_kb,
    )


@router.callback_query(F.data == "instruction_windows")
async def get_windows_instruction(clbck: CallbackQuery):
    await clbck.message.answer(
        text=text.INSTRUCTION_WINDOWS, reply_markup=keyboard_buttons.iexit_kb,
    )
