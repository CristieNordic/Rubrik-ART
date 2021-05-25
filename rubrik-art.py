#!/usr/bin/python3

# Automatic Restore Tester Rubrik
# By Cristie Nordic AB

import requests
import urllib3
import json
import random
import logging
import os
import argparse
from base64 import b64encode

logging.basicConfig(filename='restore_test.log', level=logging.DEBUG)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def get_config(url=None, api_ver='v1', auth=None, logname='restore_test.log'):
    print('Get Configuration Information')
    if url:
        logging.info('URL has been used with the function call')
    elif os.getenv('RUBRIK_URL'):
        logging.info('System Variable RUBRIK_URL will be used')
        url = os.getenv('RUBRIK_URL')
    else:
        from config import RUBRIK_URL
        logging.info('Using URL from configuration File')
        url = RUBRIK_URL

    rubrik_url = 'https://{url}/api/{api_ver}'.format(**locals())


    if auth:
        logging.info('Auth has been set part of the function')
    elif os.getenv('RUBRIK_AUTH'):
        logging.info('Find the Rubrik Authentication as a system variable')
        auth = os.getenv('RUBRIK_AUTH')
    else:
        from config import RUBRIK_AUTH
        logging.info('Using Authenication from configuration file')
        auth = RUBRIK_AUTH

    rubrik_auth = { 'Authorization' : 'Basic %s' %  auth }

    return(rubrik_url, rubrik_auth)

def encode_username_password(username, password):
    print('Encoding your username and password')
    username_and_password = str.encode('{username}:{password}'.format(**locals()))
    return(b64encode(username_and_password).decode('ascii'))

def get_random_vm(rubrik_url=None, rubrik_auth=None):
    print('Get Random VM')
    vms = requests.get(rubrik_url+'/vmware/vm', headers=rubrik_auth, verify=False).json()['data']
    active = []
    for i,e in enumerate(vms):
        if vms[i]['effectiveSlaDomainName'] != 'Unprotected' and vms[i]['powerStatus'] == 'poweredOn':
            active.append(vms[i])
    return vms[+random.randint(0, len(active)-1)]

def get_random_snapshot(vmId=None, rubrik_url=None, rubrik_auth=None):
    snapshotlist = requests.get(rubrik_url+'/vmware/vm/'+vmId+'/snapshot', headers=rubrik_auth, verify=False).json()['data']
    if len(snapshotlist) == 1:
        return snapshotlist[0]['id']
    elif len(snapshotlist) == 0:
        logging.warning('No Snapshots found')
        exit('No Snapshots found')
    random_snapshot = snapshotlist[+random.randint(0, len(snapshotlist)-1)]['id']
    logging.info('Random Snapshot being restored : %s',random_snapshot)
    return random_snapshot

def restore_random_vm(powerOn = 'false', disableNetwork ='true', rubrik_url=None, rubrik_auth=None):
    """example : restore_random_vm('false','false') will not power on vm and will not disable network"""

    restore_vm = get_random_vm(rubrik_url=rubrik_url, rubrik_auth=rubrik_auth)
    print('Restore VM:', restore_vm['name'])
    logging.info('Random VM name %s:', restore_vm['name'])
    restore_name='RestoreTest-'+restore_vm['name']
    logging.info('Restored VM name %s:', restore_name)
    restore_random_snapshot = get_random_snapshot(vmId=restore_vm['id'], rubrik_url=rubrik_url, rubrik_auth=rubrik_auth)
    restore_url = rubrik_url+'/vmware/vm/snapshot/'+restore_random_snapshot+'/mount'
    logging.info(restore_url)
    payload = '{"vmName" : "'+restore_name+'", "powerOn" : '+powerOn+', "disableNetwork" : '+disableNetwork+'}'
    logging.info(payload)

    restore_test = requests.post(restore_url, headers=rubrik_auth, data=payload, verify=False)
    print('Restore Test Finish...')
    return restore_test

def main():
    if a.username and a.password:
        base64_authenication = encode_username_password(a.username, a.password)
    elif a.key:
        base64_authenication = a.key

    if a.url:
        if base64_authenication:
            rubrik_url, rubrik_auth = get_config(url=a.url, auth=base64_authenication)
        else:
            rubrik_url, rubrik_auth = get_config(url=a.url)
    else:
        rubrik_url, rubrik_auth = get_config()

    art = restore_random_vm(rubrik_url=rubrik_url, rubrik_auth=rubrik_auth)
    if art.status_code == 202:
        print('Successfully restore VM...')
    else:
        print(art)

if __name__ == "__main__":
    p = argparse.ArgumentParser(
        description='''Rubrik Automatic Restore Test''',
        epilog='''Contact support@cristie.se'''
    )
    g = p.add_mutually_exclusive_group(required = False)
    p.add_argument("--url", "-U", help = "IP or FQDN Address to your Rubrik Cluster")
    g.add_argument("--key", "-k", help = "Username and Password in Base64 encoded format")
    g.add_argument("--username", "-u", help = "Username name in clear text format")
    p.add_argument("--password", "-p", help = "Password in in clear text format")
    a = p.parse_args()
    main()
