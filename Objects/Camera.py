class Camera:
    def __init__(self):
        # Properties
        self.CameraID = 0
        self.Name = None
        self.MacAddress = None
        self.InternalIPAddress = None
        self.ExternalIPAddress = None
        self.Height = None
        self.Width = None
        self.DirectoryPath = None
        self.StatusID = None

    def mapper(self, result_set):
        for key, value in result_set.items():
            if "CameraID" in key:
                self.CameraID = value
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
            if "Height" in key:
                self.Height = value
                continue
            if "Width" in key:
                self.Width = value
                continue
            if "DirectoryPath" in key:
                self.DirectoryPath = value
                continue
            if "StatusID" in key:
                self.StatusID = value
                continue
