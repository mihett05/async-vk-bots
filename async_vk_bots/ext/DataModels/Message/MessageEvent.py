from typing import Optional


class MessageEvent:
    conversation_message_id: Optional[int]
    user_id: int
    peer_id: int
    event_id: str
    payload: str

    def __init__(self, event: dict):
        if "conversation_message_id" in event:
            self.conversation_message_id = event["conversation_message_id"]
        else:
            self.conversation_message_id = None
        self.user_id = event["user_id"]
        self.peer_id = event["peer_id"]
        self.event_id = event["event_id"]
        self.payload = event["payload"]
