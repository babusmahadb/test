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
    usr_data = "C:\\Users\\Administrator.DEMO\\Downloads\\test\\svmvol.xlsx"
    inv_data = "C:\\Users\\Administrator.DEMO\\Downloads\\test\\clstrsvm.xlsx"
       
    usr_df = pd.read_excel(usr_data)
    inv_df = pd.read_excel(inv_data)
    
    #print(usr_df)
    #print(inv_df)
    
    for ind1 in usr_df.index:
        usr_df.loc[ind1,'clstr_match'] = list(inv_df[inv_df['svm_name'].str.contains(usr_df['SVM_Name'][ind1])]['cls_name'])
    
    #print(usr_df)
    
    cons_df = usr_df[['clstr_match','Vol_Name','SVM_Name']]
    cons_df.to_excel("C:\\Users\\Administrator.DEMO\\Downloads\\test\\clstrvol.xlsx", sheet_name='clstrvol', index=False, header=False)
    
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
    
    
#def disp_vol(cluster: str, svm_name: str, volume_name: str, headers_inc: str)
    
#def disp_vol(cluster: str, svm_name: str, volume_name: str, headers_inc: str):
#    """Display Volumes"""
#    #ctr = 0
#    #tmp = dict(get_volumes(cluster, svm_name ,volume_name, headers_inc))
#    #vols = tmp['records']
#    url = "https://{}/api/storage/volumes/?svm.name={}&name={}".format(cluster,svm_name,volume_name)
#    response = requests.get(url, headers=headers_inc, verify=False)
#    volume = response.json()
#    volumercd = dict(volume)
#    tmpr = volumercd['records']
#    for i in tmpr:
#        volumelist = dict(i)
#    #print(volumelist)
#    tab = tt.Texttable()
#    header = (['Volume name', 'Volume UUID', 'Vserver Name', 'Vol State', ' Vol Type', 'Junction Path', 'Read IOPS', 'Write IOPS', 'Other IOPS', 'Total IOPS', 'Read throughput', 'Write throughput', 'Other throughput', 'Total throughput'])
#    tab.header(header)
#    tab.set_cols_width([18,40,20,15,15,25,5,5,5,5,10,10,10,10])
#    tab.set_cols_align(['c','c','c','c','c','c','c','c','c','c','c','c','c','c'])
#    #for volumelist in vols:
#    #ctr = ctr + 1
#    vol = volumelist['name']
#    uuid = volumelist['uuid']
#    #print(vol)
#    url = "https://{}/api/storage/volumes/{}".format(cluster, uuid)
#    response = requests.get(url, headers=headers_inc, verify=False)
#    vuid = response.json()
#    tmp2 = dict(vuid)
#    sv = tmp2['svm']
#    na = tmp2['nas']
#    vsrv = sv['name']
#    state = tmp2['state']
#    tier = tmp2['type']
#    url1 = "https://{}/api/storage/volumes?uuid={}&fields=nas.path".format(cluster, uuid)
#    response = requests.get(url1, headers=headers_inc, verify=False)
#    nas = response.json()
#    ng = dict(nas)
#    #print("ng",ng)
#    ngi = ng['records']
#    #print("ngi",ngi)
#    for keys in ngi:
#        chk = keys.get('nas')
#        if chk is None:
#            path = "NA"
#        else:
#            val = keys['nas']
#            tval = dict(val)
#            chk1 = tval['path']
#            if (chk1 is None):
#                path = "NA"
#            else:
#                path = tval['path']
#    staturl = "https://{}/api/storage/volumes?uuid={}&fields=statistics.iops_raw.read,statistics.iops_raw.write,statistics.iops_raw.other,statistics.iops_raw.total,statistics.throughput_raw.total,statistics.throughput_raw.read,statistics.throughput_raw.write,statistics.throughput_raw.other".format(cluster, uuid)
#    response = requests.get(staturl, headers=headers_inc, verify=False)
#    stats = response.json()
#    dstat = dict(stats)
#    #print(dmetr)
#    rstat = dstat['records']
#    #print(rmetr)
#    for keys in rstat:
#        val = keys['statistics']
#        tval = dict(val)
#        iops = tval['iops_raw']
#        ival = dict(iops)
#        riops = ival['read']
#        wiops = ival['write']
#        oiops = ival['other']
#        tiops = ival['total']
#        thrp = tval['throughput_raw']
#        ithrp = dict(thrp)
#        rthrp = ithrp['read']
#        wthrp = ithrp['write']
#        othrp = ithrp['other']
#        tthrp = ithrp['total']
#        #for key in val:
#        #    print(key)
#        #    tiops = tval['total']
#    tab.add_row([vol,uuid,vsrv,state,tier,path,riops,wiops,oiops,tiops,rthrp,wthrp,othrp,tthrp])
#    tab.set_cols_width([18,40,20,15,15,25,5,5,5,5,10,10,10,10])
#    tab.set_cols_align(['c','c','c','c','c','c','c','c','c','c','c','c','c','c'])
#    #print("Number of Volumes for this Storage Tenant: {}".format(ctr))
#    setdisplay = tab.draw()
#    print(setdisplay)
#    #print(uuid)
    
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
    
    res_data = "C:\\Users\\Administrator.DEMO\\Downloads\\test\\Voldetails.xlsx"
    res_df = pd.read_excel(res_data)
    result_csv = res_df.to_excel("C:\\Users\\Administrator.DEMO\\Downloads\\test\\Voldetails.xlsx", sheet_name = 'Volume Details', columns = None, index = None)
    #result_csv.columns = ['Volume Name','Volume UUID']
    
    for index, row in cons_df.iterrows():
        cluster = row[0]
        volume_name = row[1]
        svm_name = row[2]
        mv = vol_meta(cluster, svm_name, volume_name, headers)
        print(mv)
      


