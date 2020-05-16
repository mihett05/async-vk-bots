class Place:
    id: int
    title: str
    latitude: int
    longitude: int
    created: int
    icon: str
    country: str
    city: str

    def __init__(self, place: dict):
        for key in place:
            setattr(self, key, place[key])
