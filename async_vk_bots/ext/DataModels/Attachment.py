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
        self.obj = attachment[self.type]
        self.id = self.obj["id"]
        self.owner_id = self.obj["owner_id"]

    @staticmethod
    def parse(attachment):
        return Attachment(attachment)

    def to_vk(self):
        return f"{self.type}{self.owner_id}_{self.id}_{self.access_key}"
