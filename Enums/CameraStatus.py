from enum import Enum


class CameraStatus(Enum):
    Offline = 1
    CameraBootStart = 2
    CameraBootComplete = 3
    ConnectingToServerStart = 4
    ConnectingToServerComplete = 5
    Recording = 6
    Error = 7

