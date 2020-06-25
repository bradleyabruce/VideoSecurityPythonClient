import cv2
import numpy
from picamera import PiCamera
from picamera.array import PiRGBArray
from vidgear.gears import NetGear

from BL import CameraBL

# Get camera info from database
print("Initializing camera...")
camera = CameraBL.startup()
print("Camera Initialized!")

# Camera Properties
IM_WIDTH = camera.Width
IM_HEIGHT = camera.Height

# Initialize pi camera
pi_camera = PiCamera()
pi_camera.resolution = (IM_WIDTH, IM_HEIGHT)

# Initialize video feed
rawCapture = PiRGBArray(pi_camera, size=(IM_WIDTH, IM_HEIGHT))
rawCapture.truncate(0)

# Get server info from database
address = '192.168.1.34'
port = '8089'
protocol = 'tcp'

# Initialize Netgear Server to send frames to
print("Initializing Server.")

# activate jpeg encoding and specify other related parameters
options = {'compression_format': '.jpg', 'compression_param':[cv2.IMWRITE_JPEG_QUALITY, 50]}
server = NetGear(address='192.168.1.20', port='8089', protocol='tcp', logging=True, **options)

# Continuously capture frames and perform object detection on them
for frame1 in pi_camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    try:
        # read frames from stream
        frame = numpy.copy(frame1.array)

        # check for frame if Nonetype
        if frame is None:
            break

        # {do something with the frame here}

        # send frame to server
        server.send(frame)
        print("Sent.")

    except:
        print("Client Stopped.")
        break

    rawCapture.truncate(0)
# safely close video stream
pi_camera.close()

# safely close server
server.close()
