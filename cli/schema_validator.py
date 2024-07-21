import jsonschema
import json


def validate_json_schema(filepath: str):
    with open(filepath, 'r') as scheme_file:
        schema = json.load(scheme_file)
    jsonschema.Draft7Validator.check_schema(schema)
