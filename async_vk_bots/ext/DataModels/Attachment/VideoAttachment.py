from .Attachment import Attachment


class VideoAttachment(Attachment):
    title: str
    description: str
    duration: int
    photo_130: str
    photo_320: str
    photo_640: str
    photo_800: str
    photo_1280: str
    first_frame_130: str
    first_frame_320: str
    first_frame_640: str
    first_frame_800: str
    first_frame_1280: str
    date: int
    adding_date: int
    views: int
    comments: int
    player: str
    platform: str
    can_edit: bool
    can_add: bool
    is_private: bool
    processing: bool
    live: bool
    upcoming: bool
    is_favorite: bool

    def __init__(self, attachment):
        super(VideoAttachment, self).__init__(attachment)
        self.can_edit = "can_edit" in self._obj
        self.can_add = bool(self._obj["can_add"])
        self.is_private = "is_private" in self._obj
        self.processing = "processing" in self._obj
        self.live = "live" in self._obj
        self.upcoming = "upcoming" in self._obj
