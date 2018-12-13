import boto3
import botocore
import os
import sys
import getopt
import json

def main(argv):
    """
        Validate all VPCS have Flow logs present

    """
    region = ''
    try:
        opts, args = getopt.getopt(argv,"hr:",["region="])
    except getopt.GetoptError:
        print('check_rebuild903.py -r <region>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('check_rebuild903.py -b <region>')
            sys.exit()
        elif opt in ("-r", "--region"):
            region = arg
    print('region is ' +  region)
    try:
        list_vpc_pass = []
        list_vpc_fail = []
        ec2 = boto3.client('ec2', region_name=region)
        count_fails = 0
        flow_logs = list(ec2.describe_flow_logs()['FlowLogs'])
        if flow_logs:
            for item in flow_logs:
                if not item['FlowLogStatus'] == 'ACTIVE':
                    count_fails += 1
                    list_vpc_fail.append(item['ResourceId'])
                else:
                    list_vpc_pass.append(item['ResourceId'])

            if count_fails == 0:
                flow_logging = True
                print('FLow logs is present for the following VPCs:', ' '.join(list_vpc_pass))
                exit(0)
            else:
                flow_logging = False
                print('FLow logs is not present for the following VPCs:', ' '.join(list_vpc_fail))
                exit(1)
        else:
            flow_logging = False
            print('FLow logs is not present for any VPCs')
            exit(1)

    except Exception as err:
        print(err) 

if __name__ == "__main__":
    main(sys.argv[1:])