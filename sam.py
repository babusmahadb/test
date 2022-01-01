"""
ONTAP REST API Sample Scripts

Purpose: Script to list volumes properties using ONTAP REST API.

Usage: list_volumes_property.py [-h] [-u API_USER] [-p API_PASS]
"""

import pandas as pd
import openpyxl as xl

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
    
    # Pulls Cluster information using uservol.xls and inventory.xls using find_clstr() and place data to clstrvol.xls 
    cons_df = find_clstr()
    
    print(cons_df)
    #res_data = "C:\\Users\\Administrator.DEMO\\Downloads\\test\\Voldetails.xlsx"
    #res_df = pd.read_excel(res_data)
    #result_csv = res_df.to_excel("C:\\Users\\Administrator.DEMO\\Downloads\\test\\Voldetails.xlsx", sheet_name = 'Volume Details', columns = None, index = None)
    ##result_csv.columns = ['Volume Name','Volume UUID']
    #
    #for index, row in cons_df.iterrows():
    #    cluster = row[0]
    #    volume_name = row[1]
    #    svm_name = row[2]
    #    mv = vol_meta(cluster, svm_name, volume_name, headers)
    #
    #    tmp = mv
    #    print(tmp)