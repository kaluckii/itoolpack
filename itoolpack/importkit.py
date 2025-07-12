import glob
import importlib

from types import ModuleType
from fastapi import APIRouter


def escape_module(module: str) -> str:
    """
    Convert a file path to a Python module path by replacing slashes with dots
    and removing the '.py' extension.
    """
    return module.replace("\\", ".").replace("/", ".").replace(".py", "")


def export_telegram_controllers(
    path: str = "controllers/telegram/**/*.py",
) -> list[ModuleType]:
    """
    Recursively import all Python modules matching the given glob pattern.
    Used to dynamically load Telegram controller modules.

    :param path: Glob pattern to search for controller files.
    :return: List of imported module objects.
    :raises ModuleNotFoundError: If a module cannot be found.
    """
    modules = []

    for m in glob.iglob(path, recursive=True):
        modules.append(importlib.import_module(escape_module(m)))

    return modules


def export_server_routers(
    path: str = "**/server/**/*.py", router_instance: str = "controller"
) -> list[APIRouter]:
    """
    Recursively import all modules matching the glob path and collect APIRouter
    instances from the specified variable name (e.g. 'controller').

    :param path: Glob pattern to search for server files.
    :param router_instance: Variable name to look for (must be an APIRouter).
    :return: List of discovered APIRouter instances.
    """
    handlers = []

    for m in glob.iglob(path, recursive=True):
        module = importlib.import_module(escape_module(m))
        router = getattr(module, router_instance, None)

        if isinstance(router, APIRouter):
            handlers.append(router)

    return handlers


def export_tortoise_models(path: str = "domain/**/model.py") -> list[str]:
    """
    Discover model modules by locating 'model.py' files and converting their
    paths to dotted module names.

    :param path: Glob pattern to search for model files.
    :return: List of model module paths as strings.
    """
    models = ["aerich.models"]

    for m in glob.iglob(path, recursive=True):
        models.append(escape_module(m))

    return models
