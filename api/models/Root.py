from typing import Annotated, Dict, List, Any
from pydantic import BaseModel, Field


class Exposedports(BaseModel):
    protocol: Annotated[str, Field()]
    name: Annotated[str, Field()]
    port: Annotated[float, Field()]


class Log(BaseModel):
    level: Annotated[str, Field()]


class Specification(BaseModel):
    jvmConfig: Annotated[List[str], Field()]
    exposedPorts: Exposedports
    log: Log
    environmentVariables: Annotated[List[str], Field()]
    sharedNamespace: Annotated[bool, Field()]


class Settings(BaseModel):
    settingAaa: Annotated[Dict[Any, Any], Field()]
    settingAab: Annotated[Dict[Any, Any], Field()]


class Configuration(BaseModel):
    specification: Specification
    settings: Settings


class Root(BaseModel):
    kind: Annotated[str, Field()]
    version: Annotated[str, Field()]
    name: Annotated[str, Field()]
    description: Annotated[str, Field()]
    configuration: Configuration

