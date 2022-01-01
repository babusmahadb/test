"""
ONTAP REST API Sample Scripts

Purpose: Script to list volumes properties using ONTAP REST API.

Usage: list_volumes_property.py [-h] [-u API_USER] [-p API_PASS]
"""

import pandas as pd
import openpyxl as xl
import urllib3 as ur

import base64
import argparse
from getpass import getpass
import logging
import texttable as tt
import requests
ur.disable_warnings()

def find_clstr():
    """Get cluster info from inventory using user inputs"""
    usr_data = "C:\\Users\\Administrator.DEMO\\Documents\\GitHub\\test\\test\\svmvol.xlsx"
    inv_data = "C:\\Users\\Administrator.DEMO\\Documents\\GitHub\\test\\test\\clstrsvm.xlsx"
       
    usr_df = pd.read_excel(usr_data)
    inv_df = pd.read_excel(inv_data)
    
    #print(usr_df)
    #print(inv_df)
    
    for ind1 in usr_df.index:
        usr_df.loc[ind1,'clstr_match'] = list(inv_df[inv_df['svm_name'].str.contains(usr_df['SVM_Name'][ind1])]['cls_name'])
    
    #print(usr_df)
    
    cons_df = usr_df[['clstr_match','Vol_Name','SVM_Name']]
    cons_df.to_excel("C:\\Users\\Administrator.DEMO\\Documents\\GitHub\\test\\test\\clstrvol.xlsx", sheet_name='clstrvol', index=False, header=False)
    
    #print(cons_df)

    return cons_df
    
def parse_args() -> argparse.Namespace:
    """Parse the command line arguments from the user"""

    parser = argparse.ArgumentParser(
        description="This script will list volumes in a SVM")
    
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

#def get_volumes(cluster: str, svm_name: str, volume_name: str, headers_inc: str):
#    """Get Volumes"""
#    url = "https://{}/api/storage/volumes/?svm.name={}".format(cluster, volume_name)
#    response = requests.get(url, headers=headers_inc, verify=False)
#    return response.json()

def vol_meta(cluster: str, svm_name: str, volume_name: str, headers_inc: str):
    
    """ Pulls Volume Name & UUID """
    
    vol_url = "https://{}/api/storage/volumes/?svm.name={}&name={}".format(cluster,svm_name,volume_name)
    vol_response = requests.get(vol_url, headers=headers_inc, verify=False)
    vol_json = vol_response.json()
    
    vol_dt = dict(vol_json)
    vol_rd = vol_dt['records']
    
    for i in vol_rd:
        volume = dict(i)
        
    vol_name = volume['name']
    vol_uuid = volume['uuid']
    
    return vol_name,vol_uuid
    
    
def nas_path(cluster: str, volume_uuid: str, headers_inc: str):
    
    """ Pulls Junction Path & Vserver details"""
    
    vol_url = "https://{}/api/storage/volumes/{}".format(cluster, volume_uuid)
    vol_response = requests.get(vol_url, headers=headers_inc, verify=False)
    vol_json = vol_response.json()
    
    vol_dt = dict(vol_json)
    tmp = vol_dt['svm']
    vsrv = tmp['name']
    state = vol_dt['state']
    tier = vol_dt['type']
    
    nas_url = "https://{}/api/storage/volumes?uuid={}&fields=nas.path".format(cluster, volume_uuid)
    response = requests.get(nas_url, headers=headers_inc, verify=False)
    nas_json = response.json()
    
    nas_dt = dict(nas_json)
    nas_rd = nas_dt['records']
    for keys in nas_rd:
        chk = keys.get('nas')
        if chk is None:
            path = "NA"
        else:
            val = keys['nas']
            nas_jp = dict(val)
            chk1 = nas_jp['path']
            if (chk1 is None):
                path = "NA"
            else:
                path = nas_jp['path']
                
                
    return vsrv, state, tier, path

def vol_stats(cluster: str, volume_uuid: str, headers_inc: str):
    
    """ Pulls Volume's Raw Statistical IOPS & Throughput details"""
        
    stat_url = "https://{}/api/storage/volumes?uuid={}&fields=statistics.iops_raw.read,statistics.iops_raw.write,statistics.iops_raw.other,statistics.iops_raw.total,statistics.throughput_raw.total,statistics.throughput_raw.read,statistics.throughput_raw.write,statistics.throughput_raw.other".format(cluster, volume_uuid)
    response = requests.get(stat_url, headers=headers_inc, verify=False)
    stat_json = response.json()
    
    stat_dt = dict(stat_json)
    stat_rd = stat_dt['records']
    for keys in stat_rd:
        val = keys['statistics']
        st_js = dict(val)
        iops = st_js['iops_raw']
        ival = dict(iops)
        riops = ival['read']
        wiops = ival['write']
        oiops = ival['other']
        tiops = ival['total']
        thrp = st_js['throughput_raw']
        ithrp = dict(thrp)
        rthrp = ithrp['read']
        wthrp = ithrp['write']
        othrp = ithrp['other']
        tthrp = ithrp['total']

    return riops,wiops,oiops,tiops,rthrp,wthrp,othrp,tthrp

def snap_mirr(cluster: str, svm_name: str, volume_name: str, headers_inc: str):
    
    """ Pulls Volume's Snapmirror details"""
        
    snap_url = "https://{}/api/snapmirror/relationships?list_destinations_only=true&source.path={}:{}&return_records=true&return_timeout=15".format(cluster, svm_name, volume_name)
    response = requests.get(snap_url, headers=headers_inc, verify=False)
    snap_json = response.json()
    
    snap_dt = dict(snap_json)
    snap_rd = snap_dt['records']
    # isp is "is_proctedted", scrp is "source_path", desp is "destination_path"
    isp = scrp = desp = "NA"
    if snap_rd:
        for keys in snap_rd:
            src_val = keys['source']
            src_p = dict(src_val)
            scrp = src_p['path']
            des_val = keys['destination']
            des_p = dict(des_val)
            desp = des_p['path']
            isp = "Yes"
    else:
        scrp = "NA"
        desp = "NA"
        isp = "No"
            
    return isp,scrp,desp

    
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
    
    # Pulls Cluster information using uservol.xls and inventory.xls using find_clstr() and place data to clstrvol.xls 
    cons_df = find_clstr()
    
    #res_data = "C:\\Users\\Administrator.DEMO\\Documents\\GitHub\\test\\test\\Voldetails.xlsx"
    #res_df = pd.read_excel(res_data)
    #result_csv = res_df.to_excel("C:\\Users\\Administrator.DEMO\\Documents\\GitHub\\test\\test\\Voldetails.xlsx", sheet_name = 'Volume Details', columns = None, index = None)
    #result_csv.columns = ['Volume Name','Volume UUID']
    
    for index, row in cons_df.iterrows():
        cluster = row[0]
        volume_name = row[1]
        svm_name = row[2]
        mv = vol_meta(cluster, svm_name, volume_name, headers)
        js_vol_name = mv[0]
        js_vol_uuid = mv[1]
        np = nas_path(cluster,js_vol_uuid, headers)
        st = vol_stats(cluster,js_vol_uuid, headers)
        sp = snap_mirr(cluster,svm_name,js_vol_name, headers)
        
        tmp = mv + np + st + sp
        print(tmp)
        
      


