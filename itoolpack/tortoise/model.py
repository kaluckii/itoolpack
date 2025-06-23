from tortoise import fields
from tortoise.models import Model as __Model
from tortoise.contrib.pydantic import pydantic_model_creator


class PydanticDescriptor:
    def __get__(self, instance, owner):
        if not hasattr(owner, "_pydantic_schema"):
            owner._pydantic_schema = pydantic_model_creator(owner)
        return owner._pydantic_schema


class Model(__Model):
    pd = PydanticDescriptor()

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        cls.__assign_related_name()

    @classmethod
    def __assign_related_name(cls) -> None:
        for attr_name, attr_value in cls.__dict__.items():
            if isinstance(
                attr_value,
                (
                    fields.relational.ForeignKeyFieldInstance,
                    fields.relational.OneToOneFieldInstance,
                    fields.relational.ManyToManyFieldInstance,
                ),
            ):
                if attr_value.related_name is None:
                    attr_value.related_name = cls.__name__.lower()
