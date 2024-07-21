import importlib
import os

from fastapi import FastAPI

app = FastAPI(
    title='models-and-rest-generator',
    version='0.1.0',
    description='FastAPI application with generated REST controllers',
)


routes_dir = 'routes'
for filename in os.listdir(routes_dir):
    if filename.endswith('.py'):
        module_name = filename[:-3]
        module = importlib.import_module(f'routes.{module_name}')
        if hasattr(module, 'router'):
            app.include_router(module.router)


if __name__ == '__main__':
    import uvicorn

    uvicorn.run(app, host='localhost', port=8000)
