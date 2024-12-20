from dataclasses import dataclass, field
from typing import Optional


@dataclass
class Content:
    text: str
    type: Optional[str] = "message"
    title: str = "test message"


@dataclass
class File:
    filename: str
    data: str


@dataclass
class MessagePost:
    content: Content
    files: list[File] = field(default_factory=list)
    recipient_id: int = 9610251011
    author_id: int = 1
    # expiry_timestamp: Optional[int]=None
    silent: int = 0
    type: str = "message"
