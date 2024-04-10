import time
import json
from web_service_connection import WebServiceConnection

def TrigWorkArea(signalName):
    """TriggerWorkArea

    """
    username = "Default User"
    password = "robotics"
    web_service_connection = WebServiceConnection("localhost", 6155, username, password)

    url = f"http://{WebServiceConnection.get_host()}:{WebServiceConnection.get_port()}/rw/iosystem/signals/EtherNetIP/PPABOARD/{signalName}?action=set"
    payload = {"lvalue": 1, "mode": "pulse", "Pulses":1}
    resp = WebServiceConnection.get_session().post(url, cookies=WebServiceConnection.get_cookies(), data=payload)
