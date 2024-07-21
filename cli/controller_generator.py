import os
from jinja2 import FileSystemLoader, Environment


def generate_rest_controllers(models_dir, output_dir):
    for model_file in os.listdir(models_dir):
        if model_file.endswith('.py'):
            model_name = model_file[:-3]

            template_loader = FileSystemLoader(searchpath='cli/templates')
            template_env = Environment(loader=template_loader)
            template_file = 'rest_controller.jinja2'
            template = template_env.get_template(template_file)
            code = template.render(kind=model_name)

            os.makedirs(output_dir, exist_ok=True)
            with open(os.path.join(output_dir, f'{model_name}.py'), 'w') as out_file:
                out_file.write(code)
