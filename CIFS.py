#! /usr/bin/env python3

"""
ONTAP REST API Sample Scripts

This script was developed by NetApp to help demonstrate NetApp
technologies.  This script is not officially supported as a
standard NetApp product.

Purpose: Script to list volumes using ONTAP REST API.

Usage: list_volumes.py [-h] -c CLUSTER -vs SVM_NAME [-u API_USER]
                       [-p API_PASS]

Copyright (c) 2020 NetApp, Inc. All Rights Reserved.
Licensed under the BSD 3-Clause “New” or Revised” License (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at
https://opensource.org/licenses/BSD-3-Clause

"""
import base64
import argparse
from getpass import getpass
import logging
import texttable as tt
import requests
import urllib3 as ur
ur.disable_warnings()


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
    header = (['Volume name', 'No. of CIFS Shares','CIFS Shares List','ACl'])
    tab.header(header)
    tab.set_cols_width([18,20,60,60])
    tab.set_cols_align(['c','c','c','c'])
    
    
    CSEList=[]
    for volumelist in vols:
        ctr = ctr + 1
        vol = volumelist['name']
        uuid = volumelist['uuid']
        urlC="https://{}/api/protocols/cifs/shares/?volume={}".format(cluster,vol)
        Cresponse = requests.get(urlC, headers=headers_inc, verify=False)
        Cshare = Cresponse.json()
        Crcout = Cshare['num_records']
        CST=[]
        CSList=[]
        CSRList=[]
        CSTList=[]
        if Crcout!=0:
            CSRecords=Cshare['records']
            
            for cs in CSRecords:
                CSTemp=dict(cs)
                CSN=CSTemp['name']
                CST.append(CSN)
                VS=CSTemp['svm']
                VSN=VS['uuid']
                
                if "root" in vol:
                    CSRT= CSN + "Share is in Root Volume"
                    CSRList.append(CSRT)
                else:
                    CSI="https://{}/api/protocols/cifs/shares/{}/{}".format(cluster,VSN,CSN)
                    CSIresponse=requests.get(CSI,headers=headers_inc, verify=False)
                    CSID = CSIresponse.json()
                    CSTN=CSID['name']
                    CSTA=CSID['acls']
                    CSTAT=[]
                    for i in CSTA:
                        CSTAC=i['permission']
                        CSTUG=i['user_or_group']
                        CSTMP="CIFS Share "+CSN+" has "+CSTUG+" Permission"+CSTAC
                        #print(CSTMP)
                        CSList.append(CSTMP)
        if "root" in vol:
            tab.add_row([vol,Crcout,CST,CSRList])
        elif Crcout==0:
            CT = "No Qtrees"
            CSTList.append(CT)
            tab.add_row([vol,Crcout,CST,CSTList])
        else:     
            tab.add_row([vol,Crcout,CST,CSList])
        tab.set_cols_width([18,20,60,60])
        tab.set_cols_align(['c','c','c','c'])
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

    disp_vol(ARGS.cluster, ARGS.svm_name, headers)