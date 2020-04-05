from .Place import Place


class Geo:
    type: str
    coordinates: list
    place: Place

    def __init__(self, geo: dict):
        for key in geo:
            if key == "place":
                self.place = Place(geo[key])
            else:
                setattr(self, key, geo[key])
