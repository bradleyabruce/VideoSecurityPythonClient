class Server:
    def __init__(self):
        # Properties
        self.ServerID = 0
        self.Name = None
        self.MacAddress = None
        self.InternalIPAddress = None
        self.ExternalIPAddress = None
        self.DirectoryPath = None
        self.StatusID = None

    def mapper(self, result_set):
        for key, value in result_set.items():
            if "ServerID" in key:
                self.ServerID = value
                continue
            if "Name" in key:
                self.Name = str(value)
                continue
            if "MacAddress" in key:
                self.MacAddress = str(value)
                continue
            if "InternalIPAddress" in key:
                self.InternalIPAddress = str(value)
                continue
            if "ExternalIPAddress" in key:
                self.ExternalIPAddress = value
                continue
            if "DirectoryPath" in key:
                self.DirectoryPath = value
                continue
            if "Status" in key:
                self.StatusID = value
                continue
