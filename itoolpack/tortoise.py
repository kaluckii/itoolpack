from tortoise import Model as __Model
from tortoise.contrib.pydantic import pydantic_model_creator


class PydanticDescriptor:
    def __get__(self, instance, owner):
        if not hasattr(owner, "_pydantic_schema"):
            owner._pydantic_schema = pydantic_model_creator(owner)
        return owner._pydantic_schema


class Model(__Model):
    pd = PydanticDescriptor()