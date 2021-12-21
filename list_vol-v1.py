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
    header = (['Volume name', 'Volume UUID', 'Vserver Name', 'Vol State', ' Vol Type', 'Junction Path', 'Read IOPS', 'Write IOPS', 'Other IOPS', 'Total IOPS', 'Read throughput', 'Write throughput', 'Other throughput', 'Total throughput'])
    tab.header(header)
    tab.set_cols_width([18,40,20,15,15,25,5,5,5,5,10,10,10,10])
    tab.set_cols_align(['c','c','c','c','c','c','c','c','c','c','c','c','c','c'])
    for volumelist in vols:
        ctr = ctr + 1
        vol = volumelist['name']
        uuid = volumelist['uuid']
        #print(vol)
        url = "https://{}/api/storage/volumes/{}".format(cluster, uuid)
        response = requests.get(url, headers=headers_inc, verify=False)
        vuid = response.json()
        tmp2 = dict(vuid)
        sv = tmp2['svm']
        na = tmp2['nas']
        vsrv = sv['name']
        state = tmp2['state']
        tier = tmp2['type']
        url1 = "https://{}/api/storage/volumes?uuid={}&fields=nas.path".format(cluster, uuid)
        response = requests.get(url1, headers=headers_inc, verify=False)
        nas = response.json()
        ng = dict(nas)
        #print("ng",ng)
        ngi = ng['records']
        #print("ngi",ngi)
        for keys in ngi:
            chk = keys.get('nas')
            if chk is None:
                path = "NA"
            else:
                val = keys['nas']
                tval = dict(val)
                chk1 = tval['path']
                if (chk1 is None):
                    path = "NA"
                else:
                    path = tval['path']
        staturl = "https://{}/api/storage/volumes?uuid={}&fields=statistics.iops_raw.read,statistics.iops_raw.write,statistics.iops_raw.other,statistics.iops_raw.total,statistics.throughput_raw.total,statistics.throughput_raw.read,statistics.throughput_raw.write,statistics.throughput_raw.other".format(cluster, uuid)
        response = requests.get(staturl, headers=headers_inc, verify=False)
        stats = response.json()
        dstat = dict(stats)
        #print(dmetr)
        rstat = dstat['records']
        #print(rmetr)
        for keys in rstat:
            val = keys['statistics']
            tval = dict(val)
            iops = tval['iops_raw']
            ival = dict(iops)
            riops = ival['read']
            wiops = ival['write']
            oiops = ival['other']
            tiops = ival['total']
            thrp = tval['throughput_raw']
            ithrp = dict(thrp)
            rthrp = ithrp['read']
            wthrp = ithrp['write']
            othrp = ithrp['other']
            tthrp = ithrp['total']
            #for key in val:
            #    print(key)
            #    tiops = tval['total']
        tab.add_row([vol,uuid,vsrv,state,tier,path,riops,wiops,oiops,tiops,rthrp,wthrp,othrp,tthrp])
        tab.set_cols_width([18,40,20,15,15,25,5,5,5,5,10,10,10,10])
        tab.set_cols_align(['c','c','c','c','c','c','c','c','c','c','c','c','c','c'])
    print("Number of Volumes for this Storage Tenant: {}".format(ctr))
    setdisplay = tab.draw()
    print(setdisplay)
    #print(uuid)

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