import numpy
from picamera import PiCamera
from picamera.array import PiRGBArray
from vidgear.gears import NetGear

# Camera Properties
IM_WIDTH = 1920
IM_HEIGHT = 1088

# Initialize camera
camera = PiCamera()

# Initialize video feed
rawCapture = PiRGBArray(camera, size=(IM_WIDTH, IM_HEIGHT))
rawCapture.truncate(0)

# Initialize Netgear Server to send frames to
server = NetGear(address='192.168.1.49', port='8089', protocol='tcp')

# Continuously capture frames and perform object detection on them
for frame1 in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    try:
        # read frames from stream
        frame = numpy.copy(frame1.array)

        # check for frame if Nonetype
        if frame is None:
            break

        # {do something with the frame here}

        # send frame to server
        server.send(frame)

    except KeyboardInterrupt:
        break

    rawCapture.truncate(0)
# safely close video stream
camera.close()

# safely close server
server.close()
