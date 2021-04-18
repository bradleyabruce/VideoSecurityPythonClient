class Camera:
    def __init__(self):
        # Properties
        self.CameraID = 0
        self.Name = None
        self.MacAddress = None
        self.InternalAddress = None
        self.ExternalAddress = None
        self.Height = None
        self.Width = None
        self.DirectoryPath = None
        self.CameraStatusID = None

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
            if "InternalAddress" in key:
                self.InternalAddress = str(value)
                continue
            if "ExternalAddress" in key:
                self.ExternalAddress = value
                continue
            if "DirectoryPath" in key:
                self.DirectoryPath = value
                continue
            if "CameraStatusID" in key:
                self.CameraStatusID = value
                continue
