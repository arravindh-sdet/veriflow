from jsonschema import validate
from jsonschema.exceptions import ValidationError


def validate_schema(json_data, schema):
    try:
        validate(instance=json_data, schema=schema)
    except ValidationError as e:
        raise AssertionError(f"Schema validation failed: {e.message}")
