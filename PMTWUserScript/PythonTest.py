from requests.auth import HTTPBasicAuth, HTTPDigestAuth
import requests
import logging

basic_auth = HTTPBasicAuth("Default User", "robotics")
header = {'Accept': 'application/hal+json;v=2.0'}
FORMAT = '%(asctime)-15s%(message)s'

def get_request(conn, uri, proto='https://', host='localhost:5466'):
    try:
        resp = conn.get(proto + host, auth=basic_auth, headers=header, verify=False)
        str1 = proto + host + uri
        print(str1)
        resp = conn.get(str1, headers=header, verify=False)
        print("Micael")
        print(resp.text)
    except Exception as e:
        print('Error:{}'.format(e))

if __name__ == '__main__':
    conn = requests.Session()
    get_request(conn, "/rw/iosystem/signals")
    conn.close()