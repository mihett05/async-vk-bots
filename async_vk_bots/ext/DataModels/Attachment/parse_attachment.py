from .Attachment import Attachment
from .PhotoAttachment import PhotoAttachment
from .VideoAttachment import VideoAttachment


def parse_attachment(attachment):
    t = attachment["type"]  # type
    if t == "photo":
        return PhotoAttachment(attachment)
    elif t == "video":
        return VideoAttachment(attachment)
    else:
        return Attachment(attachment)
