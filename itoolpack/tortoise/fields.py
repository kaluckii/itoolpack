from tortoise.models import Model as TortoiseModel
from tortoise import fields


class AutoRelatedNameModel(TortoiseModel):
    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)

        for attr_name, attr_value in cls.__dict__.items():
            if isinstance(attr_value, fields.relational.OneToOneFieldInstance):
                if attr_value.related_name is None:
                    attr_value.related_name = cls.__name__.lower()
