"""
    Module docstring
"""

from pydantic import BaseModel, Json
from typing import List


class Item(BaseModel):
    role: str
    content: str


class Chat(BaseModel):
    messages: list[Item]
    # info: Json[any]
