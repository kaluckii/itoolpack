import glob
import importlib

from types import ModuleType

from fastapi import APIRouter


def escape_module(module: str) -> str:
    """
    Converts a module path into a dotted module name by replacing directory
    separators with dots and removing the ".py" file extension if present.
    """

    return module.replace("\\", ".").replace("/", ".").replace(".py", "")


def export_telegram_controllers(
    path: str | None = "controllers/telegram/**/*.py",
) -> list[ModuleType]:
    """
    Imports all controllers modules dynamically, by default from the "controllers/telegram" directory.

    :raises ModuleNotFoundError: If a module cannot be found during the import.
    """

    modules = []

    for m in glob.iglob(path, recursive=True):
        modules.append(importlib.import_module(escape_module(m)))

    return modules


def export_server_handlers(
    path: str | None = "server/**/*.py",
) -> list[APIRouter]:
    """
    Dynamically discovers and imports all Python modules matching the given glob path,
    and collects any `handler` variables that are instances of FastAPI's `APIRouter`.

    This is typically used to automatically register all route controllers from a specific
    directory structure (e.g., `server/**/*`) without manually importing each one.

    :param path: Glob pattern pointing to the target Python files (defaults to 'server/**/*.py').
    :return: List of discovered APIRouter instances.
    """
    handlers = []

    for m in glob.iglob(path, recursive=True):
        module = importlib.import_module(escape_module(m))

        if hasattr(module, "handler"):
            if isinstance(module.handler, APIRouter):
                handlers.append(module.handler)

    return handlers


def export_tortoise_models(path: str | None = "domain/**/*/model.py") -> list[str]:
    """
    Imports all models by searching recursively for `model.py` files in the
    specified directory structure and escaping their module paths. Returns the
    list of models.
    """

    models = ["aerich.models"]
    for m in glob.iglob(path, recursive=True):
        models.append(escape_module(m))

    return models


def export_piccolo_models(path: str = "domain/**/*/model.py") -> list[str]:
    """
    Imports all Piccolo models by searching recursively for `model.py` files in the
    specified directory structure and escaping their module paths. Returns the list of models.
    """

    models = []

    for m in glob.iglob(path, recursive=True):
        models.append(escape_module(m))

    return models