#!/usr/bin/python3

# Automatic Restore Tester Rubrik
# By Cristie Nordic AB
# Author Chris Melin / Cristie Nordic AB
# Version 1.0


import requests
import json
import random
import logging
import os
#from config import auth

logging.basicConfig(filename='restore_test.log', level=logging.DEBUG)
#rubrikurl = "https://ENTERYOURIP/api/v1"
#headers = auth


def get_config(rubrik_url=None, rubrik_auth=None, logname='restore_test.log'):
    if rubrik_url:
        print('URL has been set')
    elif os.getenv('RUBRIK_URL'):
        print('Find the Rubrik URL as a system variable')
        rubrik_url = os.getenv('RUBRIK_URL')
    else:
        from config import RUBRIK_URL
        print('URL is set to none')
        rubrik_url = RUBRIK_URL



    if rubrik_auth:
        print('Auth has been set')
    elif os.getenv('RUBRIK_AUTH'):
        logging.info('Find the Rubrik Authentication as a system variable')
        rubrik_auth = os.getenv('RUBRIK_AUTH')
    else:
        from config import RUBRIK_AUTH
        print('Auth hasnt been set')
        rubrik_auth = RUBRIK_AUTH


    return(rubrik_url, rubrik_auth)

def get_random_vm():
    vms = requests.get(rubrikurl+'/vmware/vm', headers=headers, verify=False).json()['data']
    active = []
    for i,e in enumerate(vms):
        if vms[i]['effectiveSlaDomainName'] != 'Unprotected' and vms[i]['powerStatus'] == 'poweredOn':
            active.append(vms[i])
    return vms[+random.randint(0, len(active)-1)]

def get_random_snapshot(vmId):
    snapshotlist = requests.get(rubrikurl+'/vmware/vm/'+vmId+'/snapshot', headers=headers, verify=False).json()['data']
    if len(snapshotlist) == 1:
        return snapshotlist[0]['id']
    elif len(snapshotlist) == 0:
        logging.warning('No Snapshots found')
        exit('No Snapshots found')
    random_snapshot = snapshotlist[+random.randint(0, len(snapshotlist)-1)]['id']
    logging.info('Random Snapshot being restored : %s',random_snapshot)
    return random_snapshot


def restore_random_vm(powerOn = 'false', disableNetwork ='true'):
    """example : restore_random_vm('false','false') will not power on vm and will not disable network"""

    restore_vm = get_random_vm()
    logging.info('Random VM name %s:', restore_vm['name'])
    restore_name='RestoreTest-'+restore_vm['name']
    logging.info('Restored VM name %s:', restore_name)
    restore_random_snapshot = get_random_snapshot(restore_vm['id'])
    restore_url = rubrikurl+'/vmware/vm/snapshot/'+restore_random_snapshot+'/mount'
    logging.info(restore_url)
    payload = '{"vmName" : "'+restore_name+'", "powerOn" : '+powerOn+', "disableNetwork" : '+disableNetwork+'}'
    logging.info(payload)

    restore_test = requests.post(restore_url, headers=headers, data=payload, verify=False)
    return restore_test
