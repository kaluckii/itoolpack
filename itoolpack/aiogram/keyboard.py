from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


def build_keyboard(buttons: list[list[str]], rows: int = 2) -> InlineKeyboardMarkup:
    """
    Builds an InlineKeyboardMarkup using the given set of buttons and specified
    row configuration. Detects hyperlinks in the provided data and creates url-button.
    """

    builder = InlineKeyboardBuilder()
    for text, callback in buttons:
        if not "http" in callback:
            builder.button(text=text, callback_data=callback)

        else:
            builder.button(text=text, url=callback)

    builder.adjust(rows, repeat=True)
    return builder.as_markup()
