import json
import os
from typing import Dict, Tuple
from jinja2 import Template
import time

base_types = {
    'string': 'str',
    'integer': 'int',
    'number': 'float',
    'boolean': 'bool',
    'array': 'List[Any]',
}


def load_json_schema(filepath: str) -> Dict:
    with open(filepath, 'r') as file:
        return json.load(file)


# TODO: handle empty objects, string parameters, arrays of specific types like List[str]
def parse_object(json_object: Tuple[str, Dict]) -> Dict[str, str]:
    field_name = json_object[0]
    field_type = json_object[1].get('type')

    return_class = {}
    if field_type == 'object':
        parent = {field_name: field_name.capitalize()}
        return_class.update(parent)
        child = {}
        for object_property in json_object[1]['properties'].items():
            if object_property[1].get('type') == 'object':
                child.update(parse_object(object_property))
            else:
                child.update(
                    {
                        object_property[0]: base_types.get(
                            object_property[1].get('type')
                        )
                    }
                )
        return_class.update(child)

    elif field_type in base_types:
        return {json_object[0]: base_types.get(field_type)}

    return return_class


def parse_schema(schema_path, output_dir='models'):
    schema = load_json_schema(schema_path)  # noqa
    classes = {}

    for field in schema['properties'].items():
        classes.update(parse_object(field))
    print(classes)


def generate_pydantic_models(schema_path, output_dir='models'):
    schema = load_json_schema(schema_path)  # noqa

    # TODO: Parse configuration

    # -----------------------------------------------------------

    template = Template('templates/pydantic_class.jinja2')
    model_code = template.render(...)  # TODO: provide argument(s)

    # ------------------------------------------------------------

    os.makedirs(output_dir, exist_ok=True)
    # TODO: Provide model_name from json schema (....lower())
    with open(
        os.path.join(output_dir, f'model_{....lower()}.py'), 'w'
    ) as file:
        file.write(model_code)


if __name__ == '__main__':
    start = time.perf_counter()
    parse_schema('test_polygon/test_schema1.json')
    finish = time.perf_counter()
    print('Время работы: ' + str(finish - start))
