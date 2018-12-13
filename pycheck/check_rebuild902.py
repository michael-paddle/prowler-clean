import boto3
import botocore
import os
import sys
import getopt
import json

def main(argv):
    """
        Validate if cloudwatch can show cloudtrail logs

    """
    region = ''
    try:
        opts, args = getopt.getopt(argv,"hr:",["region="])
    except getopt.GetoptError:
        print('check_rebuild902.py -r <region>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('check_rebuild902.py -b <region>')
            sys.exit()
        elif opt in ("-r", "--region"):
            region = arg
    print('region is ' +  region)
    try:
        list_trails_fail = []
        list_trails_success = []
        client = boto3.client('cloudtrail', region_name=region)
        count_fail = 0
        trails = client.describe_trails(includeShadowTrails=True)
        for item in trails['trailList']:
            name_trail = item['Name']
            region = item['HomeRegion']
            trail_status = client.get_trail_status(Name=name_trail)
            if 'LatestCloudWatchLogsDeliveryTime' not in trail_status:
                count_fail += 1
                list_trails_fail.append(name_trail)
            else:
                list_trails_success.append(name_trail)
        
        if count_fail == 0:
            integration_cw = True
            print('cloudwatch is showing cloudtrail data for', ' '.join(list_trails_success))
            exit(0)
        else:
            integration_cw = False
            print('cloudwatch is missing cloudtrail data for', ' '.join(list_trails_fail))
            exit(1)

    except Exception as err:
        print(err) 

if __name__ == "__main__":
    main(sys.argv[1:])