from typing import Any, Callable, Union


class Filter:
    @classmethod
    def magic(cls, magic: Callable[..., Any]):
        """
        Wraps a custom callable filter.

        :param magic: A callable that receives a message and returns a boolean.
        :return: A lambda that applies the custom magic filter.
        """
        return lambda message: magic(message)

    @classmethod
    def hastext(cls):
        """
        Checks if the message contains text or a caption.

        :return: A lambda that returns True if message has text or caption.
        """
        return lambda message: bool(message.text) or bool(message.caption)

    @classmethod
    def command(cls, command: str):
        """
        Checks if the message is a command and matches the given command text.

        :param command: The command to check for (e.g., "start").
        :return: A lambda that returns True if message is a command and matches.
        """
        if not command:
            return lambda _: False

        return (
            lambda message: message.text
            and message.text.startswith("/")
            and command in message.text
        )

    @classmethod
    def callback(cls, data: Union[str, list[str]], startswith: bool = False):
        """
        Filters callback data either by exact match, list of matches, or prefix.

        :param data: A string or list of strings to match against callback data.
        :param startswith: If True, matches only the beginning of the data.
        :return: A lambda that filters callback queries accordingly.
        """
        if isinstance(data, list):
            return lambda callback_query: callback_query.data in data

        if startswith:
            return lambda callback_query: callback_query.data.startswith(data)

        return lambda callback_query: callback_query.data == data
