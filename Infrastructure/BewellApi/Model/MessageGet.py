from dataclasses import dataclass
from datetime import datetime
from typing import Any


@dataclass
class MessageGet:
    text: str
    type: str
    title: str
    # options: List[Option]
    id: int
    author_id: int
    recipient_id: int
    # answer: Answer
    # signature_required: bool
    # signature_timestamp: int
    # signature_datetime: int
    created_timestamp: datetime

    # updated_timestamp: int
    def __lt__():
        pass

    @staticmethod
    def from_dict(obj: Any) -> "MessageGet":
        _text = str(obj.get("text"))
        _type = str(obj.get("type"))
        _title = str(obj.get("title"))
        # _options = [Option.from_dict(y) for y in obj.get("options")]
        _id = int(obj.get("id"))
        _author_id = int(obj.get("author_id"))
        _recipient_id = int(obj.get("recipient_id"))
        # _answer = Answer.from_dict(obj.get("answer"))
        # _signature_required = False
        # _signature_timestamp = int(obj.get("signature_timestamp"))
        # _signature_datetime = int(obj.get("signature_datetime"))
        _created_timestamp = datetime.fromtimestamp(obj.get("created_timestamp"))
        # _updated_timestamp = int(obj.get("updated_timestamp"))
        return MessageGet(
            _text, _type, _title, _id, _author_id, _recipient_id, _created_timestamp
        )
