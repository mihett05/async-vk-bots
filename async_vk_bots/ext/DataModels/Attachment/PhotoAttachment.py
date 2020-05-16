from .Attachment import Attachment


class PhotoSize:
    type: str
    url: str
    width: int
    height: int

    def __init__(self, size: dict):
        for key in size:
            setattr(self, key, size[key])


class PhotoAttachment(Attachment):
    album_id: int
    user_id: int
    text: str
    date: int
    sizes: list
    width: int
    height: int

    def __init__(self, attachment):
        super(PhotoAttachment, self).__init__(attachment)
        self.sizes = [PhotoSize(size) for size in self._obj["sizes"]]
