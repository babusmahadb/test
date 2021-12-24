"""
To get the CIFS Shares
"""

#Importing Modules

import base64
import argparse
from getpass import getpass
import logging
import texttable as tt
import requests
import urllib3 as ur
ur.disable_warnings()

#getting the CIFS  Shares
def get_volumes(cluster: str, svm_name: str, headers_inc: str):
    """Get Volumes"""
    url = "https://{}/api/storage/volumes/?svm.name={}".format(cluster, svm_name)
    response = requests.get(url, headers=headers_inc, verify=False)
    return response.json()
 
 
def disp_vol(cluster: str, svm_name: str, headers_inc: str):
    """Display Volumes"""
    ctr = 0
    tmp = dict(get_volumes(cluster, svm_name, headers_inc))
    vols = tmp['records']
    tab = tt.Texttable()
    header = (['Volume name', 'Volume UUID', 'SnapMirror(Y/N)', 'Source Path', ' Dest Path'])
    tab.header(header)
    tab.set_cols_width([18,50,25,15,15])
    tab.set_cols_align(['c','c','c','c','c'])
    for volumelist in vols:
        ctr = ctr + 1
        vol = volumelist['name']
        uuid = volumelist['uuid']
        url1 = "https://{}/api/storage/volumes/{}".format(cluster, uuid)
        response = requests.get(url1, headers=headers_inc, verify=False)
        vuid = response.json()
        tmp2 = dict(vuid)
        sv = tmp2['svm']
        vsrv = sv['name']
        svmvol = vsrv+"%3A"+vol
        smurl = "https://{}/api/protocols/cifs/shares?fields=*&return_records=true&return_timeout=15".format(cluster)
        response = requests.get(smurl, headers=headers_inc, verify=False)
        vuid1 = response.json()
        print(vuidl)
        tmp3 = dict(vuid1)
        dsmr = tmp3['records']
        isp = scrp = desp = "NA"
        for keys in dsmr:
            chk = keys.get('source')
            if chk is None:
                scrp = "NA"
                desp = "NA"
                isp = "No"
            else:
                val = keys['source']
                tval = dict(val)
                scrp = tval['path']
                dval = keys['destination']
                dtval = dict(dval)
                desp = dtval['path']
                isp = "Yes"
        tab.add_row([vol,uuid,isp,scrp,desp])
        tab.set_cols_width([18,40,25,15,15])
        tab.set_cols_align(['c','c','c','c','c'])
    print("Number of Volumes for this Storage Tenant: {}".format(ctr))
    setdisplay = tab.draw()
    print(setdisplay)

def parse_args() -> argparse.Namespace:
    """Parse the command line arguments from the user"""

    parser = argparse.ArgumentParser(
        description="This script will list volumes in a SVM")
    parser.add_argument(
        "-c", "--cluster", required=True, help="API server IP:port details")
    parser.add_argument(
        "-vs", "--svm_name", required=True, help="SVM Name"
    )
    parser.add_argument(
        "-u",
        "--api_user",
        default="admin",
        help="API Username")
    parser.add_argument("-p", "--api_pass", help="API Password")
    parsed_args = parser.parse_args()

    # collect the password without echo if not already provided
    if not parsed_args.api_pass:
        parsed_args.api_pass = getpass()

    return parsed_args


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="[%(asctime)s] [%(levelname)5s] [%(module)s:%(lineno)s] %(message)s",
    )
    ARGS = parse_args()
    BASE_64_STRING = base64.encodebytes(
        ('%s:%s' %
         (ARGS.api_user, ARGS.api_pass)).encode()).decode().replace('\n', '')

    headers = {
        'authorization': "Basic %s" % BASE_64_STRING,
        'content-type': "application/json",
        'accept': "application/json"
    }
