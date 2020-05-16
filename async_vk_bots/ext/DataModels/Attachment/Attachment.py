class Attachment:
    type: str
    owner_id: int
    id: int
    access_key: str

    def __init__(self, attachment):
        self.type = attachment["type"]
        self.access_key = ""
        if "access_key" in attachment:
            self.access_key = attachment["access_key"]
        self._obj = attachment[self.type]
        for key in self._obj:
            setattr(self, key, self._obj[key])

    def to_vk(self):
        return f"{self.type}{self.owner_id}_{self.id}_{self.access_key}"
