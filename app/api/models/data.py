class Data:
    def __init__(self, gatewayID, controllerID, data={}):
        self.gatewayID = gatewayID
        self.controllerID = controllerID
        self.data = data

    @staticmethod
    def from_dict(source):
        # ...
        return Data(
            gatewayID=source.get("gatewayID"),
            controllerID=source.get("controllerID"),
            data=source.get("data", {}),
        )
    def to_dict(self):
        # ...
        return {
            "gatewayID": self.gatewayID,
            "controllerID": self.controllerID,
            "data": self.data,
        }

    def __repr__(self):
        return f"Data(\
                gatewayID={self.gatewayID}, \
                controllerID={self.controllerID}, \
                data={self.data}\
            )"
