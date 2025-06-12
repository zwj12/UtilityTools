import sys
from requests.auth import HTTPBasicAuth, HTTPDigestAuth
import requests
import xml.etree.ElementTree as ET
import json


# dns-sd -B _http._tcp,rws
# dns-sd -L "RobotWebServices_1600-515088" _http._tcp
# dns-sd -Q CN-L-0317001.local.
class WebServiceConnection:
    __session = None
    __proto = "https://"
    __host = None
    __port = 80
    __server = None
    __username = None
    __password = None
    __auth = None
    __headerJson = {'Accept': 'application/hal+json;v=2.0'}
    __headerXML = {'Accept': 'application/xhtml+xml;v=2.0'}
    __headerContentType = {'Content-Type': 'application/x-www-form-urlencoded;v=2.0'}
    __RWSVersion = '1.0'
    __cookies = None
    __system_name = None
    __rw_version = None
    __sysid = None
    __ctrl_name = None
    __ctrl_type = False
    __ctrl_id = None
    __namespace = '{http://www.w3.org/1999/xhtml}'

    @staticmethod
    def get_session():
        if WebServiceConnection.__session is None:
            raise Exception("No Session!")
        else:
            return WebServiceConnection.__session

    @staticmethod
    def get_host():
        if WebServiceConnection.__host is None:
            raise Exception("No Host!")
        else:
            return WebServiceConnection.__host

    @staticmethod
    def get_port():
        if WebServiceConnection.__port is None:
            return 80
            # raise Exception("No Port!")
        else:
            return WebServiceConnection.__port
        
    @staticmethod
    def get_server():
        if WebServiceConnection.__server is None:
            raise Exception("No Server!")
        else:
            return WebServiceConnection.__server
        
    @staticmethod
    def get_headerJson():
        if WebServiceConnection.__headerJson is None:
            raise Exception("No headerJson!")
        else:
            return WebServiceConnection.__headerJson  
          
    @staticmethod
    def get_headerXML():
        if WebServiceConnection.__headerXML is None:
            raise Exception("No headerXML!")
        else:
            return WebServiceConnection.__headerXML    
        
    @staticmethod
    def get_headerContentType():
        if WebServiceConnection.__headerContentType is None:
            raise Exception("No headerContentType!")
        else:
            return WebServiceConnection.__headerContentType    
                     
    @staticmethod
    def get_cookies():
        if WebServiceConnection.__cookies is None:
            raise Exception("No Cookies!")
        else:
            return WebServiceConnection.__cookies

    @staticmethod
    def get_ctrl_name() -> bool:
        if WebServiceConnection.__ctrl_name is None:
            raise Exception("No Control Name!")
        else:
            return WebServiceConnection.__ctrl_name

    @staticmethod
    def get_ctrl_type() -> bool:
        if WebServiceConnection.__ctrl_type is None:
            raise Exception("No Control Type!")
        else:
            return WebServiceConnection.__ctrl_type

    @staticmethod
    def get_ctrl_id() -> bool:
        if WebServiceConnection.__ctrl_id is None:
            raise Exception("No Control ID!")
        else:
            return WebServiceConnection.__ctrl_id

    @staticmethod
    def get_system_name():
        if WebServiceConnection.__sysid is None:
            raise Exception("No System Name!")
        else:
            return WebServiceConnection.__system_name

    @staticmethod
    def get_system_guid():
        if WebServiceConnection.__sysid is None:
            raise Exception("No System Guid!")
        else:
            return WebServiceConnection.__sysid

    @staticmethod
    def get_rw_version():
        if WebServiceConnection.__rw_version is None:
            raise Exception("No Robot Ware Version!")
        else:
            return WebServiceConnection.__rw_version

    def __init__(self, host, port, username, password, RWSVersion = '1.0'):
        WebServiceConnection.__session = requests.Session()
        WebServiceConnection.__host = host
        WebServiceConnection.__port = port
        WebServiceConnection.__username = username
        WebServiceConnection.__password = password
        WebServiceConnection.__RWSVersion = RWSVersion   
        digest_auth = HTTPDigestAuth(username, password)
        basic_auth = HTTPBasicAuth("Default User", "robotics")

        if WebServiceConnection.__RWSVersion == '1.0':
            WebServiceConnection.__proto = "http://"
            WebServiceConnection.__auth = digest_auth
        else:
            WebServiceConnection.__proto = "https://"
            WebServiceConnection.__auth = basic_auth
        
        WebServiceConnection.__server = f"{WebServiceConnection.__proto}{WebServiceConnection.__host}:{WebServiceConnection.__port}"

        # For json format data
        url = f"{WebServiceConnection.__server}/rw/system?json=1"
        resp = WebServiceConnection.__session.get(url, auth=WebServiceConnection.__auth, headers=WebServiceConnection.__headerJson, verify=False)
        # print(resp.text)        
        WebServiceConnection.__cookies = resp.cookies        
        obj = json.loads(resp.text)
        if WebServiceConnection.__RWSVersion == '1.0':
            WebServiceConnection.__system_name = obj["_embedded"]["_state"][0]["name"]
            WebServiceConnection.__rw_version = obj["_embedded"]["_state"][0]["rwversion"]
            WebServiceConnection.__sysid = obj["_embedded"]["_state"][0]["sysid"]
        else:
            WebServiceConnection.__system_name = obj["state"][0]["name"]
            WebServiceConnection.__rw_version = obj["state"][0]["rwversion"]
            WebServiceConnection.__sysid = obj["state"][0]["sysid"]

        # For xml format data        
        url = f"{WebServiceConnection.__server}/ctrl"
        resp = WebServiceConnection.__session.get(url, cookies=WebServiceConnection.__cookies, headers=WebServiceConnection.__headerXML, verify=False)
        # print(resp.text)
        root = ET.fromstring(resp.text)
        if WebServiceConnection.__RWSVersion == '1.0':
            if root.findall(".//{0}li[@class='ctrl-identity-info-li']".format(WebServiceConnection.__namespace)):
                WebServiceConnection.__ctrl_name = root.find(
                    ".//{0}li[@class='ctrl-identity-info-li']/{0}span[@class='ctrl-name']"
                    .format(WebServiceConnection.__namespace)).text
                controller_type = root.find(
                    ".//{0}li[@class='ctrl-identity-info-li']/{0}span[@class='ctrl-type']"
                    .format(WebServiceConnection.__namespace)).text
                if controller_type == "Virtual Controller":
                    WebServiceConnection.__ctrl_type = True
                elif controller_type == "Real Controller":
                    WebServiceConnection.__ctrl_type = False
                    WebServiceConnection.__ctrl_id = root.find(
                        ".//{0}li[@class='ctrl-identity-info-li']/{0}span[@class='ctrl-id']"
                        .format(WebServiceConnection.__namespace)).text
        else:
            if root.findall(".//{0}li[@class='ctrl-identity-info-li']".format(WebServiceConnection.__namespace)):
                WebServiceConnection.__ctrl_name = root.find(
                    ".//{0}li[@class='ctrl-identity-info-li']/{0}span[@class='ctrl-name']"
                    .format(WebServiceConnection.__namespace)).text
                controller_type = root.find(
                    ".//{0}li[@class='ctrl-identity-info-li']/{0}span[@class='ctrl-type']"
                    .format(WebServiceConnection.__namespace)).text
                if controller_type == "Virtual Controller":
                    WebServiceConnection.__ctrl_type = True
                elif controller_type == "Real Controller":
                    WebServiceConnection.__ctrl_type = False
                    WebServiceConnection.__ctrl_id = root.find(
                        ".//{0}li[@class='ctrl-identity-info-li']/{0}span[@class='ctrl-id']"
                        .format(WebServiceConnection.__namespace)).text

    # RMMP stands for Request Manual Mode Privileges.
    @staticmethod
    def request_manual_mode_privileges():
        url = f"{WebServiceConnection.__server}/users/rmmp"
        payload = {"privilege": "modify"}
        resp = WebServiceConnection.__session.post(url, cookies=WebServiceConnection.__cookies, headers=WebServiceConnection.__headerContentType, verify=False, data=payload)
        print(resp.status_code)

    @staticmethod
    def cancel_manual_mode_privileges():
        url = f"{WebServiceConnection.__server}/users/rmmp?action=cancel"
        resp = WebServiceConnection.__session.post(url, cookies=WebServiceConnection.__cookies, headers=WebServiceConnection.__headerContentType, verify=False)
        print(resp.status_code)

    @staticmethod
    def request_master_ship():
        url = f"{WebServiceConnection.__server}/rw/mastership?action=request"
        resp = WebServiceConnection.__session.post(url, cookies=WebServiceConnection.__cookies, headers=WebServiceConnection.__headerContentType, verify=False)
        print(resp.status_code)
        print("Master ship is requested")

    @staticmethod
    def release_master_ship():
        url = f"{WebServiceConnection.__server}/rw/mastership?action=release"
        resp = WebServiceConnection.__session.post(url, cookies=WebServiceConnection.__cookies, headers=WebServiceConnection.__headerContentType, verify=False)
        print(resp.status_code)
        print("Master ship is released")


def main(argv):
    """main

    """
    print("Run from main: ", argv)
    try:

        host = "127.0.0.1"
        port = 5466
        username = "Default User"
        password = "robotics"
        print(f"Connecting to RWS server at {host}:{port}")  
        web_service_connection = WebServiceConnection(host, port, username, password, '2.0')

    except Exception:
        print("Error: ", sys.exc_info()[0])
        pass
    finally:
        print("Finally")
        pass

if __name__ == "__main__":
    main(sys.argv)
else:
    pass