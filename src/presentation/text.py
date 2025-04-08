from typing import Final

HELLO_ADMIN: Final[
    str
] = """
👋 Добрый день!

Это админская панель управления. 🛠️
Здесь вы можете добавить и удалить клиентские конфигурации. 📋
"""

HELLO_CLIENT: Final[
    str
] = """
👋 Добрый день!

Прочитайте инструкцию, чтобы понять, что с этим делать. 📖
"""

INSTRUCTIONS: Final[
    str
] = """
📝 Выберите операционную систему:
"""

CLIENT_ID_AWAIT: Final[
    str
] = """
👤 Напишите Telegram ID пользователя.
Чтобы отменить действие, нажмите на кнопку ниже. ⬇️
"""

CLIENT_LIMIT_AWAIT: Final[
    str
] = """
лимит подключений пользователя.
Чтобы отменить действие, нажмите на кнопку ниже. ⬇️
"""

TELEGRAM_ID_ERROR: Final[
    str
] = """
❌ Ошибка! Введен некорректный Telegram ID.
Чтобы вернуться, нажмите на кнопку ниже. ⬇️
"""

LIMIT_ERROR: Final[
    str
] = """
❌ Ошибка! Введен некорректный лимит.
Чтобы вернуться, нажмите на кнопку ниже. ⬇️
"""

MAIN_MENU: Final[
    str
] = """
🏠 Главное меню
"""

USER_NOT_DEFINED: Final[
    str
] = """
🚫 Пользователь не определен!
Обратитесь к администратору, чтобы он добавил вас в базу данных. 📝
"""

USER_LIMIT_EXITED: Final[
    str
] = """
⚠️ Ваш лимит на конфигурации исчерпан!
"""

CONFIG_ID_AWAIT: Final[
    str
] = """
📋 Введите название конфигурации
"""

CONFIG_ID_ERROR: Final[
    str
] = """
❌ Ошибка! Введено некорректное название конфигурации.
Оно может содержать только латинские буквы и цифры. 🔤🔢
Чтобы вернуться, нажмите на кнопку ниже. ⬇️
"""

CONFIG_IS_DELETED: Final[
    str
] = """
✅ Конфигурация удалена
"""

CLIENT_NOT_DEFINED: Final[
    str
] = """
🚫 Конфигурации не существует
"""

CONFIG_LIST: Final[
    str
] = """
📄 Список конфигураций
"""

CONFIGS_NOT_FOUND: Final[
    str
] = """
🤷‍♂️ Конфигурации не найдены
"""

USER_IS_CREATED: Final[
    str
] = """
✅ Пользователь добавлен!
"""

INSTRUCTION_IOS: Final[
    str
] = """
📱 [Ссылка на инструкцию для iOS](https://example.com/ios)
"""

INSTRUCTION_ANDROID: Final[
    str
] = """
🤖 [Ссылка на инструкцию для Android](https://example.com/android)
"""

INSTRUCTION_MACOS: Final[
    str
] = """
🍏 [Ссылка на инструкцию для MacOS](https://example.com/macos)
"""

INSTRUCTION_WINDOWS: Final[
    str
] = """
💻 [Ссылка на инструкцию для Windows](https://example.com/windows)
"""
