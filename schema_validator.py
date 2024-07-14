import jsonschema
import json


def validate_json_schema(filepath: str):
    with open(filepath, 'r') as scheme_file:
        schema = json.load(scheme_file)
    try:
        jsonschema.Draft7Validator.check_schema(schema)
        # print('No errors were found.')
    except jsonschema.exceptions.SchemaError as e:
        print(f'Error: \n{e}')
