from tortoise import fields


def AutoNamedOneToOneField(model: str, *, to_model_name: str) -> fields.OneToOneField:
    related_name = to_model_name.lower()
    return fields.OneToOneField(model, related_name=related_name)
