class _Photo:
    photo_50: str
    photo_100: str
    photo_200: str

    def __init__(self, photo):
        for key in photo:
            setattr(self, key, photo[key])


class ChatAction:
    type: str
    member_id: int
    text: str
    email: str
    photo: _Photo

    def __init__(self, action):
        for key in action:
            setattr(self, key, action[key])
