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
#import texttable as tt
import pandas as pd
import numpy as np
import requests
import openpyxl as xl
import urllib3 as ur
ur.disable_warnings()



def find_cls(volume: str, svm_name: str):
    """Get cluster info from inventory using user inputs"""
    usr_data = "C:\\Users\\Administrator.DEMO\\Desktop\\svmvol.xlsx"
    int_data = "C:\\Users\\Administrator.DEMO\\Desktop\\clstrsvm.xlsx"
    cons_data = "C:\\Users\Administrator.DEMO\\Desktop\\clstrsvmvol.xlsx"
    
    df_usr = pd.read_excel(usr_data)
    df_int = pd.read_excel(int_data)
    
    #print(df_usr.columns,df_int.columns)
    
    df_usr.rename(columns={'SVM_Name':'IDs'}, inplace=True)
    
    df_tmp = pd.merge(df_usr, df_int[['IDs','svm_name']], on='IDs', how='left')
    print(df_tmp)
    
    return df_usr.columns,df_int.columns



def parse_args() -> argparse.Namespace:
    """Parse the command line arguments from the user"""

    parser = argparse.ArgumentParser(
        description="This script will list volumes in a SVM")
    parser.add_argument(
        "-vol", "--volume", required=True, help="Volume Name")
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
    find_cls(ARGS.volume, ARGS.svm_name)
    # disp_vol(ARGS.cluster, ARGS.svm_name, headers)
