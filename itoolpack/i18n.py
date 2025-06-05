import os
import re
from pathlib import Path
from typing import Any

import yaml
from aiogram.types import InlineKeyboardMarkup
from itoolpack.aiogram.keyboard import build_keyboard
from pydantic import BaseModel


class LocaleModel(BaseModel):
    """
    Pydantic model representing a single translation entry.

    :param text: The translated text.
    :param keyboard: Optional list of (button_text, callback_or_url) tuples.
    """

    class KeyboardModel(BaseModel):
        keys: list[list[str]]
        rows: int | None = None

    text: str
    keyboard: KeyboardModel | None = None


class I18N:
    """
    Internationalization helper that loads YAML files from a 'locales' directory,
    validates entries via Pydantic, and optionally builds an inline keyboard.

    :param current: current file path (__file__)
    :param fallback: Language code to use when a translation key is missing.
    """

    _payloads: dict[str, dict[str, Any]] = {}

    def __init__(self, current: str, fallback: str):
        self.locales = Path(current).parent.parent / "locales"
        self.fallback = fallback

        if not self.locales.exists():
            raise FileNotFoundError(f"Locales directory not found: {self.locales}")

        self._register_languages()

        if self.fallback not in self._payloads:
            raise RuntimeError(f"Fallback language not found: {self.fallback}")

        for lang_code in list(self._payloads.keys()):
            self._load_language_payload(lang_code)

    def _register_languages(self) -> None:
        """
        Scans the 'locales' directory for '*.yaml' files and registers each language code
        (file stem) in the internal _payloads dictionary as an empty dict initially.
        """

        for file in self.locales.iterdir():
            if file.is_file() and file.suffix == ".yaml":
                self._payloads[file.stem] = {}

    def _load_language_payload(self, lang: str) -> None:
        """
        Loads and parses the YAML file for the given language code, storing its contents
        (a dict of translation entries) into _payloads[lang].

        :param lang: Language code corresponding to '{lang}.yaml'.
        """

        path = self.locales / f"{lang}.yaml"

        if not path.exists():
            return

        with open(path, encoding="utf-8") as f:
            payload = yaml.safe_load(f)

        if not isinstance(payload, dict):
            payload = {}

        self._payloads[lang] = payload

    def _get_model(self, key: str, lang: str) -> LocaleModel:
        """
        Retrieves and validates the LocaleModel for a given key and language.
        Falls back to the fallback language if necessary.

        :param key: Translation key to look up.
        :param lang: Preferred language code.
        :raises KeyError: If the key does not exist in either the preferred or fallback language.
        :return: LocaleModel instance for the given key.
        """

        actual_lang = lang if lang in self._payloads else self.fallback
        locale_dict = self._payloads.get(actual_lang, {})

        if key not in locale_dict and actual_lang != self.fallback:
            locale_dict = self._payloads[self.fallback]

        if key not in locale_dict:
            raise KeyError(
                f"Translation key '{key}' not found for language '{lang}' (nor in fallback '{self.fallback}')."
            )

        entry = locale_dict[key]
        return LocaleModel.model_validate(entry)

    def t(self, key: str, lang: str) -> str:
        """
        Retrieves only the translated text for the specified key and language.
        Falls back to the fallback language if the key is missing in the preferred language.

        :param key: Translation key to look up.
        :param lang: Preferred language code.
        :return: The translated text.
        """

        model = self._get_model(key, lang)
        return model.text

    def k(self, key: str, lang: str) -> InlineKeyboardMarkup:
        """
        Retrieves the InlineKeyboardMarkup for the specified key and language.
        Falls back to the fallback language if the key is missing in the preferred language.

        :param key: Translation key to look up.
        :param lang: Preferred language code.
        :raises KeyError: If no keyboard data is defined for the given key.
        :return: InlineKeyboardMarkup built from the keyboard definition.
        """

        model = self._get_model(key, lang)
        pattern = re.compile(r"\$\{([A-Z0-9_]+)\}")

        if not model.keyboard:
            raise KeyError(f"No keyboard defined for key '{key}' in language '{lang}'.")

        for pair in model.keyboard.keys:
            if len(pair) > 2:
                raise ValueError("Key pair length should be strictly 2 string objects.")

            for i, value in enumerate(pair):
                if not isinstance(value, str):
                    raise ValueError("Each keyboard value must be a string.")

                match = pattern.search(value)

                if match:
                    variable = match.group(1)
                    pair[i] = pattern.sub(os.getenv(variable), value)


        return build_keyboard(model.keyboard.keys, model.keyboard.rows or 2)