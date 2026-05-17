class Gateway:
    def __init__(self, userID, linkCode, controllers=[]):
        self.userID = userID
        self.linkCode = linkCode
        self.linked = False
        self.controllers = controllers

    @staticmethod
    def from_dict(source):
        # ...
        return Gateway(
            userID=source.get("userID"),
            linkCode=source.get("linkCode"),
            linked=source.get("linked", False),
            controllers=source.get("controllers", []),
        )
    def to_dict(self):
        # ...
        return {
            "userID": self.userID,
            "linkCode": self.linkCode,
            "linked": self.linked,
            "controllers": self.controllers,
        }

    def __repr__(self):
        return f"Gateway(\
                userID={self.userID}, \
                linkCode={self.linkCode}, \
                linked={self.linked}, \
                controllers={self.controllers}\
            )"
