class Migration:
    def __init__(self, gatewayID, hostname, temperature, cpu):
        self.gatewayID = gatewayID
        self.hostname = hostname
        self.temperature = temperature
        self.cpu = cpu

    @staticmethod
    def from_dict(source):
        # ...
        return Migration(
            gatewayID=source.get("gatewayID"),
            hostname=source.get("hostname"),
            temperature=source.get("temperature"),
            cpu=source.get("cpu"),
        )
    def to_dict(self):
        # ...
        return {
            "gatewayID": self.gatewayID,
            "hostname": self.hostname,
            "temperature": self.temperature,
            "cpu": self.cpu,
        }

    def __repr__(self):
        return f"Migration(\
                gatewayID={self.gatewayID}, \
                hostname={self.hostname}\
                temperature={self.temperature}\
                cpu={self.cpu}\
            )"
