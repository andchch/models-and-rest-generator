import json
from typing import Dict, List
import time

base_types = {
    'string': 'str',
    'integer': 'int',
    'number': 'float',
    'boolean': 'bool',
    'array': 'List[Any]',
}

keywords = {
    'string': 'str',
    'integer': 'int',
    'number': 'float',
    'boolean': 'bool',
    'array': 'List[Any]',
    'null': 'None',
    'maxLength': 'max_length',
    'minLength': 'min_length',
    'pattern': 'regex',
}

options_keywords = ['max_length', 'min_length', 'regex']


def load_json_schema(filepath: str) -> Dict:
    with open(filepath, 'r') as file:
        return json.load(file)


# TODO: handle optional fields, empty objects arrays of specific types like List[str]
def parse_schema(schema, parent=None):
    result = {}
    if 'type' in schema and 'properties' in schema:
        for key, value in schema['properties'].items():
            field_info = {
                'type': value.get('type', 'unknown'),  # unknown to Any
                'requirements': value.get('required', []),
                'parent': parent,
            }

            for keyword, val in keywords.items():
                if keyword in value:
                    field_info[val] = value[keyword]

            result[key] = field_info

            if value.get('type') == 'object' and 'properties' in value:
                result.update(parse_schema(value, parent=key))
            elif (
                value.get('type') == 'array'
                and 'items' in value
                and 'properties' in value['items']
            ):
                result.update(parse_schema(value['items'], parent=key))
    return result


def get_field_code(name: str, properties: Dict) -> str:
    if properties['type'] == 'object':
        field_code = f'{name}: {name}'
        return field_code

    options = ''
    for key, value in properties.items():
        if not value:
            continue
        if key in options_keywords:
            if key == 'regex':
                if options == '':
                    options += f'{key}=r"{value}"'
                else:
                    options += f', {key}=r"{value}"'
            else:
                if options == '':
                    options += f'{key}={value}'
                else:
                    options += f', {key}={value}'

    field_type = base_types[properties['type']]
    field_code = f'{name}: Annotated[{field_type}, Field({options})]'
    return field_code


def generate_pydantic_models(parsed_data, kind='root'):
    models: Dict[str, List[str]] = {}
    for key, value in parsed_data.items():
        parent = value.get('parent')
        if parent is None:
            if kind in models.keys():
                models[kind].append(get_field_code(key, value))
            else:
                models[kind] = [get_field_code(key, value)]
        else:
            if parent in models.keys():
                models[parent].append(get_field_code(key, value))
            else:
                models[parent] = [get_field_code(key, value)]

    return models

    # TODO: Parse configuration

    # -----------------------------------------------------------

    """template = Template('templates/pydantic_class.jinja2')
    model_code = template.render(...)  # TODO: provide argument(s)"""

    # ------------------------------------------------------------

    """os.makedirs(output_dir, exist_ok=True)
    # TODO: Provide model_name from json schema (....lower())
    with open(os.path.join(output_dir, f'model_{model_name}.py'), 'w') as file:
        file.write(model_code)"""


if __name__ == '__main__':
    start = time.perf_counter()
    schema = load_json_schema('test_polygon/test_schema.json')
    s = parse_schema(schema)
    s1 = generate_pydantic_models(s)
    finish = time.perf_counter()
    print('Время работы: ' + str(finish - start))
    # print(json.dumps(s, indent=2))
