import glob
import importlib
from types import ModuleType
from typing import List, Optional


def escape_module(module: str) -> str:
    """
    Converts a module path into a dotted module name by replacing directory
    separators with dots and removing the ".py" file extension if present.
    """

    return module.replace("\\", ".").replace("/", ".").replace(".py", "")


def import_controllers(
    path: Optional[str] = "controllers/*/**/controllers.py",
) -> List[ModuleType]:
    """
    Imports all controllers modules dynamically, by default from the "controllers" directory.

    :raises ModuleNotFoundError: If a module cannot be found during the import.
    """

    modules = []

    for m in glob.iglob(path, recursive=True):
        modules.append(importlib.import_module(escape_module(m)))

    return modules


def export_tortoise_models(path: Optional[str] = "domain/**/*/model.py") -> List[str]:
    """
    Imports all models by searching recursively for `model.py` files in the
    specified directory structure and escaping their module paths. Returns the
    list of models.
    """

    models = ["aerich.models"]
    for m in glob.iglob(path, recursive=True):
        models.append(escape_module(m))

    return models
