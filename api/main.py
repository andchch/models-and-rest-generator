import importlib
import os

from fastapi import FastAPI

app = FastAPI(title='models-and-rest-generator',
              version='0.1.0',
              description='Generate Pydantic models and REST controllers from JSON Schema.')


routes_dir = 'routes'
for filename in os.listdir(routes_dir):
    if filename.endswith('.py') and filename != '__init__.py':
        module_name = filename[:-3]
        module = importlib.import_module(f'routes.{module_name}')
        if hasattr(module, 'router'):
            app.include_router(module.router)


if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='localhost', port=8000)
