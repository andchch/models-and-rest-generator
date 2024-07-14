import json
import os
from typing import Dict
from jinja2 import Template


def load_json_schema(filepath: str) -> Dict:
    with open(filepath, 'r') as file:
        return json.load(file)


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
