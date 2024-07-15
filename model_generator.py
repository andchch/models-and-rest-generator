import json
import os
from typing import Dict, Tuple, List
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


# TODO: handle optional fields, empty objects, string parameters, arrays of specific types like List[str], relationships
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


def parse_relations_field(field: Tuple) -> Dict[str, List[str]]:
    relations = {}
    field_name = field[0]
    field_type = field[1].get('type')
    if field_type == 'object':
        for sub_field in field[1]['properties'].keys():
            if field_name not in relations.keys():
                relations[field_name] = [sub_field]
            else:
                relations[field_name].append(sub_field)
        relations.update(parse_relations_field(field))

    return relations


def parse_relations(schema_path: str) -> Dict[str, List[str]]:
    schema = load_json_schema(schema_path)

    relations = {}
    for field in schema['properties'].items():
        field_type = field[1].get('type')
        field_name = field[0]
        if field_type == 'object':
            for sub_field in field[1]['properties'].keys():
                if field_name not in relations.keys():
                    relations[field_name] = [sub_field]
                else:
                    relations[field_name].append(sub_field)
            relations.update(parse_relations_field(field))

    return relations


def parse_schema(schema_path: str) -> ...:
    schema = load_json_schema(schema_path)
    model_name = f"{schema.get('title')}_{schema['properties']['version']}"

    classes = {}
    relations = {}
    for field in schema['properties']:
        if 'Model' not in relations.keys():
            relations['Model'] = [field]
        else:
            relations['Model'].append(field)

    for field in schema['properties'].items():
        classes.update(parse_object(field))

    relations.update(parse_relations(schema_path))

    return classes, relations, model_name


def generate_pydantic_models(schema_path, output_dir='test_polygon'):
    model_name = parse_schema(schema_path)[2]

    # TODO: Parse configuration

    # -----------------------------------------------------------

    template = Template('templates/pydantic_class.jinja2')
    model_code = template.render(...)  # TODO: provide argument(s)

    # ------------------------------------------------------------

    os.makedirs(output_dir, exist_ok=True)
    # TODO: Provide model_name from json schema (....lower())
    with open(os.path.join(output_dir, f'model_{model_name}.py'), 'w') as file:
        file.write(model_code)


if __name__ == '__main__':
    start = time.perf_counter()
    parse_schema('test_polygon/test_schema1.json')
    finish = time.perf_counter()
    print('Время работы: ' + str(finish - start))
