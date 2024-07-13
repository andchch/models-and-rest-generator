import click
from schema_validator import validate_json_schema


@click.group()
def cli():
    pass


@cli.command()
@click.option(
    '--json-schema',
    required=True,
    type=click.Path(exists=True),
    help='Path to JSON Schema for generating pydantic models',
)
@click.option(
    '--out-dir',
    required=True,
    type=click.Path(),
    help='Output directory for generated models.',
)
def generate_models(json_schema, out_dir):
    validate_json_schema(json_schema)
    pass


@cli.command()
@click.option(
    '--models-dir',
    required=True,
    type=click.Path(exists=True),
    help='Directory with Pydantic models.',
)
@click.option(
    '--out-dir',
    required=True,
    type=click.Path(),
    help='Output directory for generated REST controllers.',
)
def generate_rest_routes(models_dir, out_dir):
    pass


if __name__ == '__main__':
    cli()
