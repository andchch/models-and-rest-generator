import json
from typing import Dict
import time
from jinja2 import FileSystemLoader, Environment


base_types = {
    'string': 'str',
    'integer': 'int',
    'number': 'float',
    'boolean': 'bool',
    'array': 'List[Any]',
    'dict': 'Dict[Any]',
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


def parse_schema(schema: Dict, parent=None, path='') -> Dict[str, Dict]:
    result = {}
    if 'type' in schema and 'properties' in schema:
        required_fields = schema.get('required', [])

        for key, value in schema['properties'].items():
            current_path = f'{path}.{key}' if path else key
            field_info = {
                'type': value.get('type'),
                'required': key in required_fields,
                'parent': parent,
                'path': current_path,
            }

            for keyword, val in keywords.items():
                if keyword in value:
                    field_info[val] = value[keyword]

            result[current_path] = field_info

            if (
                value.get('type') == 'object'
                and 'properties' in value
                and value['properties'] is not None
            ):
                result.update(
                    parse_schema(value, parent=key, path=current_path)
                )
            elif (
                value.get('type') == 'array'
                and 'items' in value
                and 'properties' in value['items']
            ):
                result.update(
                    parse_schema(value['items'], parent=key, path=current_path)
                )
    return result


def generate_field_code(name: str, properties: Dict) -> str:
    if properties['type'] == 'object':
        field_code = f'{name}: {name.capitalize()}'
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


def get_depth(parsed_data):
    levels = {}
    for name in parsed_data.keys():
        heirarchy = name.split('.')
        for single_name in heirarchy:
            levels[single_name.capitalize()] = heirarchy.index(single_name)
    return levels


def sort_models_by_dependencies(models: Dict, properties: Dict) -> Dict:
    combined_items = [
        (key, models[key], properties.get(key, float('-inf')))
        for key in models
    ]
    sorted_items = sorted(
        combined_items, key=lambda item: item[2], reverse=True
    )
    sorted_models = {key: value for key, value, _ in sorted_items}
    return sorted_models


if __name__ == '__main__':
    start = time.perf_counter()
    schema = load_json_schema('test_polygon/test_schema.json')
    s = parse_schema(schema)

    models = {}
    for path, info in s.items():
        parts = path.split('.')
        if len(parts) == 1:
            class_name = s.get('Kind', 'Root')
            field_name = parts[0]
        else:
            class_name = (
                parts[-2].capitalize()
                if len(parts) > 1
                else parts[0].capitalize()
            )
            field_name = parts[-1]

        if class_name not in models:
            models[class_name] = []
        models[class_name].append(generate_field_code(field_name, info))

    a = sort_models_by_dependencies(models, get_depth(s))

    templateLoader = FileSystemLoader(searchpath='./templates')
    templateEnv = Environment(loader=templateLoader)
    template_file = 'pydantic_class.jinja2'
    template = templateEnv.get_template(template_file)
    code = template.render(models=a)

    with open('models/model.py', 'w') as file:
        file.write(code)

    finish = time.perf_counter()
    print('Время работы: ' + str(finish - start))
