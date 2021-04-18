import socket
import sys
import uuid
from requests import get
from DL import DBConn
from Enums.CameraStatus import CameraStatus
from Enums.eTransactionType import eTransactionType
from Objects.Camera import Camera
from Objects.Exceptions import NetworkAddressNotAvailableException, MacAddressNotAvailableException
from Objects.Query import Query
from datetime import datetime

sql_select = "SELECT c.CameraID, c.Name, c.InternalAddress, c.ExternalAddress, c.MacAddress, c.PortNumber, c.CameraStatusID, c.DirectoryPath "
sql_from = " FROM tCameras c "


def get_local_ip():
    try:
        os = sys.platform
        local_ip = "Unavailable"
        if os == "linux":
            host_name = socket.gethostname()
            local_ip = socket.gethostbyname(host_name + ".local")

        else:
            # MacOS
            local_ip = socket.gethostbyname_ex(socket.gethostname())[-1][0]

        return local_ip
    except Exception:
        raise NetworkAddressNotAvailableException


def get_external_ip():
    try:
        external_ip = get('https://api.ipify.org').text
        return external_ip
    except Exception:
        raise NetworkAddressNotAvailableException


def get_current_mac_address():
    try:
        mac_address = ':'.join(['{:02x}'.format((uuid.getnode() >> ele) & 0xff)
                                for ele in range(0, 8 * 6, 8)][::-1])
        return mac_address
    except Exception:
        raise MacAddressNotAvailableException


def startup():
    try:
        mac_address = get_current_mac_address()
        camera = get_camera_from_mac_address(mac_address)

        # Update existing data and return
        if camera is not None:
            update_startup_values_into_db(camera)
        # Create new entry and return
        else:
            insert_default_values_into_db(mac_address)

        return get_camera_from_mac_address(mac_address)


    except Exception as err:

        print(err)


def get_camera_from_mac_address(mac_address):
    camera = Camera()

    query = Query()
    query.TransactionType = eTransactionType.Query
    query.Sql = sql_select + sql_from + " WHERE c.MacAddress = %s"
    query.Args = [str(mac_address)]
    result = DBConn.single_query(query)
    if len(result) > 0:
        camera.mapper(result[0])
        return camera
    else:
        return None


def insert_default_values_into_db(mac_address):
    camera = Camera()
    camera.Name = "Camera"
    camera.MacAddress = mac_address
    camera.InternalAddress = get_local_ip()
    camera.ExternalAddress = get_external_ip()
    camera.PortNumber = 8089
    camera.CameraStatusID = CameraStatus.CameraBootStart.value
    camera.DirectoryPath = ""

    insert_query = Query()
    insert_query.TransactionType = eTransactionType.Insert
    insert_query.Sql = "INSERT INTO tCameras (Name, MacAddress, InternalAddress, ExternalAddress, PortNumber, CameraStatusID, DirectoryPath) VALUES (%s, %s, %s, %s, %s, %s, %s)"
    insert_query.Args = [str(camera.Name), str(camera.MacAddress), str(camera.InternalAddress),
                         str(camera.ExternalAddress), str(camera.PortNumber), str(camera.CameraStatusID),
                         str(camera.DirectoryPath)]
    camera.CameraID = DBConn.single_query(insert_query)
    __insert_camera_log(camera.CameraID, CameraStatus.CameraBootStart.value, "Camera is starting.")

    # TODO: Update directory path with new camera ID


def update_startup_values_into_db(camera):
    camera.InternalAddress = get_local_ip()
    camera.ExternalAddress = get_external_ip()
    camera.CameraStatusID = CameraStatus.CameraBootStart.value

    update_query = Query()
    update_query.TransactionType = eTransactionType.Update
    update_query.Sql = "UPDATE tCameras SET InternalAddress = %s, ExternalAddress = %s, CameraStatusID = %s WHERE CameraID = %s"
    update_query.Args = [str(camera.InternalAddress), str(camera.ExternalAddress), str(camera.CameraStatusID), str(camera.CameraID)]
    DBConn.single_query(update_query)
    __insert_camera_log(camera.CameraID, CameraStatus.CameraBootStart.value, "Camera is starting.")


def update_camera_status(camera_id, status_id, message):
    # Server ID will not always be known. If it is not passed, look it up
    if camera_id is None:
        mac_address = get_current_mac_address()
        camera = get_camera_from_mac_address(mac_address)
        camera_id = camera.CameraID

    __update_current_camera_status(camera_id, status_id)
    __insert_camera_log(camera_id, status_id, message)


def __update_current_camera_status(camera_id, status_id):
    update_query = Query()
    update_query.TransactionType = eTransactionType.Update
    update_query.Sql = "Update tCameras SET CameraStatusID = %s WHERE CameraID = %s"
    update_query.Args = [str(status_id), str(camera_id)]
    DBConn.single_query(update_query)


def __insert_camera_log(camera_id, status_id, message):
    insert_query = Query()
    insert_query.TransactionType = eTransactionType.Insert
    insert_query.Sql = "INSERT INTO tCameraLog(CameraID, CameraStatusID, CameraMessage, LogDateTime) VALUES (%s, %s, %s, %s)"
    insert_query.Args = [str(camera_id), str(status_id), message, datetime.now()]
    DBConn.single_query(insert_query)
