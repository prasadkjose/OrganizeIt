""" This is a Pydantic schema class to complement json-schema"""

from typing import List, Union, Dict, Optional
from pydantic import BaseModel, Field


class FormatRule(BaseModel):
    types: List[str] = Field(
        title="Format Rulest",
        description="List of acceptable file types for this format rule.",
    )


class SkipRule(BaseModel):

    dir: Optional[str] = Field(
        title="Skip Directories", description="Regex to match directories to skip."
    )
    files: Optional[str] = Field(
        title="Skip File Names", description="Regex to match files to skip."
    )


class NamePattern(BaseModel):
    name_pattern: str = Field(
        title="Name Patterns",
        description="Regex pattern to match file names for organization.",
    )


class NamesRule(BaseModel):
    __root__: Dict[str, NamePattern] = Field(
        title="Naming Rules",
        description="Dictionary of name patterns for organization.",
    )


class RuleItem(BaseModel):
    # Key is a string(directory names) and values are list of formats.
    format: Optional[Dict[str, FormatRule]] = Field(
        None, description="Rules for organizing files based on format."
    )
    names: Optional[NamesRule] = Field(
        None, description="Rules for organizing files based on name patterns."
    )
    skip: Optional[SkipRule] = Field(
        None, description="Rules for skipping certain files or directories."
    )


class ConfigSchema(BaseModel):
    source: str = Field(..., description="Source directory for files to be organized.")
    destination: str = Field(
        ..., description="Destination directory for organized files."
    )
    rules: List[RuleItem] = Field(
        ..., description="List of rules for organizing files."
    )
