from async_vk_bots.ext.DataModels.Attachment.parse_attachment import parse_attachment
from ..Geo.Geo import Geo
from .ChatAction import ChatAction


class Message:
    id: int
    date: int
    peer_id: int
    from_id: int
    text: str
    random_id: int
    ref: str
    ref_source: str
    attachments: list
    important: bool
    geo: Geo
    payload: str
    fwd_messages: list
    reply_message: object
    action: ChatAction

    def __init__(self, event_message: dict):
        for key in event_message:
            if key == "attachments":
                self.attachments = [parse_attachment(attachment) for attachment in event_message[key]]
            elif key == "fwd_messages":
                self.fwd_messages = [Message(msg) for msg in event_message[key]]
            elif key == "reply_message":
                self.reply_message = Message(event_message[key])
            elif key == "geo":
                self.geo = Geo(event_message[key])
            elif key == "action":
                self.action = ChatAction(event_message[key])
            else:
                setattr(self, key, event_message[key])
