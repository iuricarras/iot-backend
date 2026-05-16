class Action:
    def __init__(self, gatewayID, controllerID, cpu=0, temp=0, speed=0):
        self.gatewayID = gatewayID
        self.controllerID = controllerID
        self.cpu = cpu
        self.temp = temp
        self.speed = speed

    @staticmethod
    def from_dict(source):
        # ...
        return Action(
            gatewayID=source.get("gatewayID"),
            controllerID=source.get("controllerID"),
            cpu=source.get("cpu", 0),
            temp=source.get("temp", 0),
            speed=source.get("speed", 0),
        )
    def to_dict(self):
        # ...
        return {
            "gatewayID": self.gatewayID,
            "controllerID": self.controllerID,
            "cpu": self.cpu,
            "temp": self.temp,
            "speed": self.speed,
        }

    def __repr__(self):
        return f"Action(\
                gatewayID={self.gatewayID}, \
                controllerID={self.controllerID}, \
                cpu={self.cpu}, \
                temp={self.temp}, \
                speed={self.speed}\
            )"
