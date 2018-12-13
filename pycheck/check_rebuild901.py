import boto3
import botocore
import os
import sys
import getopt
import json

def main(argv):
    """
        Validate no open access to MySQL port

    """
    region = ''
    try:
        opts, args = getopt.getopt(argv,"hr:",["region="])
    except getopt.GetoptError:
        print('check_rebuild901.py -r <region>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('check_rebuild901.py -b <region>')
            sys.exit()
        elif opt in ("-r", "--region"):
            region = arg
    print('region is ' +  region)

    client = boto3.client('ec2', region_name=region)
    try:
        counter_fail = 0
        sg_list = client.describe_security_groups()
        for obj in sg_list['SecurityGroups']:
            for line in obj['IpPermissions']:
                if 'FromPort' in line:
                    if line['FromPort'] == 3389:
                        for item in line['IpRanges']:
                            if item['CidrIp'] == '0.0.0.0/0':
                                counter_fail += 1
                
        if counter_fail == 0:
            allow_ingress = False
            print('we are not allowing it')
        else:
            allow_ingress = True
            print('we are allowing it')
    except Exception as err:
        print(err) 

if __name__ == "__main__":
    main(sys.argv[1:])