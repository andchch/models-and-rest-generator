import click

from controller_generator import generate_rest_controllers
from model_generator import generate_pydantic_models
from schema_validator import validate_json_schema


@click.group()
def cli():
    pass


@cli.command(help='Generate Pydantic models from JSON Schema.')
@click.option(
    '-js',
    '--json-schema',
    required=True,
    type=click.Path(exists=True),
    help='Path to JSON Schema for generating pydantic models',
)
@click.option(
    '-o',
    '--out-dir',
    required=False,
    type=click.Path(),
    help='Output directory for generated models.',
    default='api/models',
    show_default=True,
)
def gen_models(json_schema, out_dir):
    try:
        validate_json_schema(json_schema)
    except Exception as e:
        click.echo(f'JSON Error: {e}')
        return
    generate_pydantic_models(json_schema, out_dir)


@cli.command(help='Generate REST controllers from Pydantic models.')
@click.option(
    '--models-dir',
    required=False,
    type=click.Path(exists=True),
    help='Directory with Pydantic models.',
    default='api/models',
    show_default=True,
)
def gen_controllers(models_dir):
    generate_rest_controllers(models_dir)


if __name__ == '__main__':
    cli()
