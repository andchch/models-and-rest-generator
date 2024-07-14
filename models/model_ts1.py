from typing import Annotated, Dict, List
from pydantic import BaseModel, Field


SEMVER_REGEX = '^v?(?P<major>0|[1-9]\d*)\.(?P<minor>0|[1-9]\d*)\.(?P<patch>0|[1-9]\d*)(?:-(?P<prerelease>(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*)(?:\.(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*))*))?(?:\+(?P<buildmetadata>[0-9a-zA-Z-]+(?:\.[0-9a-zA-Z-]+)*))?$'


class exposedPorts(BaseModel):
    protocol: str
    name: str
    port: int


class log(BaseModel):
    level: str


class Specification(BaseModel):
    jvmConfig: list
    exposedPorts: exposedPorts
    log: log
    environmentVariables: List[str]
    sharedNamespace: bool


class Settings(BaseModel):
    settingAaa: Dict
    settingAab: Dict


class Configuration(BaseModel):
    specification: Specification
    settings: Settings


class Model(BaseModel):
    kind: Annotated[str, Field(..., max_length=32)]
    version: Annotated[str, Field(..., regex=SEMVER_REGEX)]
    name: Annotated[str, Field(..., max_length=128)]
    description: Annotated[str, Field(default_factory=str, max_length=4096)]
    configuration: Configuration
