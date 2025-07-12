from collections.abc import Awaitable, Callable
from typing import Any

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject
from aiogram.dispatcher.middlewares.user_context import EventContext
from pydantic import BaseModel


class Context(BaseModel):
    """
    Context object that holds user information and event context.
    """

    class ContextUser(BaseModel):
        id: int
        username: str | None = None

    user: ContextUser
    event_context: EventContext


def build_context(event_context: EventContext) -> Context | None:
    """
    Build a Context object from the EventContext, extracting user information.
    If the user is not present, return None and middleware will block the request."""

    if not hasattr(event_context, "user") or not event_context.user:
        return None

    return Context(
        user=Context.ContextUser(
            id=event_context.user.id,
            username=event_context.user.username,
        ),
        event_context=event_context,
    )


class ContextMiddleware(BaseMiddleware):
    """
    Middleware to inject user context into Telegram event handlers.
    This middleware extracts user information from the event context and
    passes it to the handler. If no user context is found, it blocks the request.
    """

    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: dict[str, Any],
    ) -> Any:
        event_context = data.get("event_context", {})
        context = build_context(event_context)

        if not context:
            return print("No user context found, blocking request.")

        data["ctx"] = context
        return await handler(event, data)
