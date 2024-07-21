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


class vk_test(BaseModel):
    kind: Annotated[str, Field(max_length=32)]
    version: Annotated[
        str,
        Field(
            regex=r'^(?P<major>0|[1-9]\d*)\.(?P<minor>0|[1-9]\d*)\.(?P<patch>0|[1-9]\d*)(?:-(?P<prerelease>(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*)(?:\.(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*))*))?(?:\+(?P<buildmetadata>[0-9a-zA-Z-]+(?:\.[0-9a-zA-Z-]+)*))?$'
        ),
    ]
    name: Annotated[str, Field(max_length=128)]
    description: Annotated[str, Field()]
    configuration: Configuration
