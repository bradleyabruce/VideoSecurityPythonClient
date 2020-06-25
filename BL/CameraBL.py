import socket
import sys
import uuid
from requests import get
from DL import DBConn
from Enums import CameraStatus
from Objects.Camera import Camera


def get_local_ip():
    try:
        os = sys.platform
        local_ip = "Unavailable"
        if os == "linux":
            host_name = socket.gethostname()
            local_ip = socket.gethostbyname(host_name + ".local")

        elif os == "darwin":
            # MacOS
            local_ip = socket.gethostbyname_ex(socket.gethostname())[-1][0]

        return local_ip
    except Exception:
        return "Unavailable"


def get_external_ip():
    try:
        external_ip = get('https://api.ipify.org').text
        return external_ip
    except Exception:
        return "Unavailable"


def get_current_mac_address():
    try:
        mac_address = ':'.join(['{:02x}'.format((uuid.getnode() >> ele) & 0xff)
                                for ele in range(0, 8 * 6, 8)][::-1])
        return mac_address
    except Exception:
        return "Unavailable"


def startup():
    try:
        mac_address = get_current_mac_address()
        camera = query_values_from_db(mac_address)

        # Update existing data and return
        if camera is not None:
            if update_values_into_db(camera):
                camera = query_values_from_db(mac_address)
                return camera
            else:
                return None

        # Create new entry and return
        else:
            if insert_default_values_into_db(mac_address):
                camera = query_values_from_db(mac_address)
                return camera
            else:
                return None

    except Exception as err:
        print(err)


def query_values_from_db(mac_address):
    camera = Camera()
    if mac_address is not "Error":
        query = "SELECT c.CameraID FROM tCamera c WHERE c.MacAddress = '" + mac_address + "';"

        query = "SELECT c.CameraID, c.Name, c.MacAddress, c.InternalIPAddress, c.ExternalIPAddress, c.Height, c.Width, cd.DirectoryPath, c.CameraStatusID" \
                " FROM tCamera c" \
                " LEFT JOIN tCameraDirectory cd ON c.CameraID = cd.CameraID" \
                " WHERE c.MacAddress = '" + mac_address + "';"

        result = DBConn.query_return(query)
        if len(result) > 0:
            camera.mapper(result[0])
            return camera
        else:
            return None


def insert_default_values_into_db(mac_address):
    try:
        internal_ip = get_local_ip()
        external_ip = get_external_ip()

        # Insert into tCamera
        camera = Camera()
        camera.Name = "Camera"
        camera.MacAddress = mac_address
        camera.InternalIPAddress = internal_ip
        camera.ExternalIPAddress = external_ip
        camera.Height = 1088
        camera.Width = 1920
        camera.StatusID = CameraStatus.CameraStatus.StartingUp.value
        camera.CameraID = 0
        camera.DirectoryPath = ""

        query = "INSERT INTO tCamera" \
                " (Name, MacAddress, InternalIPAddress, ExternalIPAddress, Height, Width,CameraStatusID)" \
                " VALUES" \
                " ('" + camera.Name + "' ,'" + camera.MacAddress + "', '" + camera.InternalIPAddress + "', '" + camera.ExternalIPAddress + "', " + str(camera.Height) + ", " + str(camera.Width) + ", " + str(camera.StatusID) +");"
        camera.CameraID = DBConn.query_update(query, True)

        # Insert into tCameraDirectory
        query = "INSERT INTO tCameraDirectory" \
                " (CameraID, DirectoryPath)" \
                " VALUES" \
                " (" + str(camera.CameraID) + ", 'Camera/" + str(camera.CameraID) + "/');"
        camera_directory_id = DBConn.query_update(query, True)
        return True

    except Exception as err:
        print(err)
        return False


def update_values_into_db(camera):
    try:
        internal_ip = get_local_ip()
        external_ip = get_external_ip()
        status_id = CameraStatus.CameraStatus.StartingUp.value

        camera.InternalIPAddress = internal_ip
        camera.ExternalIPAddress = external_ip
        camera.StatusID = status_id

        query = "UPDATE tCamera" \
                " SET" \
                " InternalIPAddress = '" + camera.InternalIPAddress +"', ExternalIPAddress = '" + camera.ExternalIPAddress + "', CameraStatusID = " + str(camera.StatusID) + \
                " WHERE CameraID = " + str(camera.CameraID)
        updated_rows = DBConn.query_update(query, False)
        # Updated rows will only be greater than 0 if something actually changes
        # We have to assume that it works
        return True
    except Exception as err:
        print(err)
        return False


def update_status_id(camera):
    try:
        query = "UPDATE tCamera" \
                " SET" \
                " CameraStatusID = " + str(camera.StatusID) + \
                " WHERE CameraID = " + str(camera.CameraID)
        updated_rows = DBConn.query_update(query, False)
        # Updated rows will only be greater than 0 if something actually changes
        # We have to assume that it works
        return True
    except Exception as err:
        print(err)
        return False
