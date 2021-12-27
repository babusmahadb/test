"""
ONTAP REST API Sample Scripts

Purpose: Script to list volumes properties using ONTAP REST API.

Usage: list_volumes_property.py [-h] -vol VOLUME_NAME -vs SVM_NAME [-u API_USER]
                       [-p API_PASS]
"""

import pandas as pd
import openpyxl
import urllib3 as ur
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
    
    cons_df = usr_df[['clstr_match','Vol_Name']]
    cons_df.to_excel("C:\\Users\\Administrator.DEMO\\Downloads\\test\\clstrvol.xlsx", sheet_name='clstrvol', index=False, header=False)
    
    #print(cons_df)

    return cons_df
    
#def parse_args() -> argparse.Namespace:
#    """Parse the command line arguments from the user"""
#
#    parser = argparse.ArgumentParser(
#        description="This script will list volumes in a SVM")
#    parser.add_argument(
#        "-vol", "--volume", required=True, help="Volume Name")
#    parser.add_argument(
#        "-vs", "--svm_name", required=True, help="SVM Name"
#    )
#    parser.add_argument(
#        "-u",
#        "--api_user",
#        default="admin",
#        help="API Username")
#    parser.add_argument("-p", "--api_pass", help="API Password")
#    parsed_args = parser.parse_args()
#
#    # collect the password without echo if not already provided
#    if not parsed_args.api_pass:
#        parsed_args.api_pass = getpass()
#
#    return parsed_args


if __name__ == "__main__":
    #logging.basicConfig(
    #    level=logging.INFO,
    #    format="[%(asctime)s] [%(levelname)5s] [%(module)s:%(lineno)s] %(message)s",
    #)
    #ARGS = parse_args()
    #BASE_64_STRING = base64.encodebytes(
    #    ('%s:%s' %
    #     (ARGS.api_user, ARGS.api_pass)).encode()).decode().replace('\n', '')
    #
    #headers = {
    #    'authorization': "Basic %s" % BASE_64_STRING,
    #    'content-type': "application/json",
    #    'accept': "application/json"
    #}
    find_clstr()
    
    #disp_vol(ARGS.cluster, ARGS.svm_name, headers)
