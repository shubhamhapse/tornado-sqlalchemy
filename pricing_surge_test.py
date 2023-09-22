import boto3
import datetime
from datetime import datetime, timedelta

from snippet.aws_api_tools import get_client

client = boto3.client("ec2")
instances_to_check = [
  "t3.nano",
]
x_days = 1000
now = datetime.utcnow()

s3 = boto3.client('s3')


def fetch_spot_price_only_needed_records(instance_type):
    records = []
    res = client.describe_spot_price_history(
        #YYYY-MM-DD*T*HH:MM:SS*Z 2023-08-30 15:02:54+00:00
        Filters=[
            {
                'Name': 'timestamp',
                'Values': [
                    '2023-08-30*??:??:??*?'
                ]
            },
        ],
        InstanceTypes = [instance_type],
        AvailabilityZone="us-west-2a",
        ProductDescriptions=["Linux/UNIX"]
    )
    records.extend(res["SpotPriceHistory"])
    print(f"Records found the smart way {records}")


def fetch_spot_price(instance_type, start_date, end_date):
    records = []
    res = client.describe_spot_price_history(
        InstanceTypes = [instance_type],
        AvailabilityZone="us-west-2a",
        ProductDescriptions=["Linux/UNIX"],
        StartTime = start_date,
        EndTime = end_date
    )
    records.extend(res["SpotPriceHistory"])
    while "NextToken" in res and res["NextToken"]:
        token = res["NextToken"]
        res = client.describe_spot_price_history(
            InstanceTypes=[instance_type],
            AvailabilityZone="us-west-2a",
            ProductDescriptions=["Linux/UNIX"],
            StartTime=start_date,
            EndTime=end_date,
            NextToken=token,
        )
        records.extend(res["SpotPriceHistory"])
    print(f"records found :{len(records)}")
    print(records[0]["Timestamp"])
    print(records[-1])

    if len(records)>1:
        # get spot instance price for first record in the list and the last record
        return records[-1]["SpotPrice"], records[0]["SpotPrice"]
    else:
        return "", ""


for instance_type in instances_to_check:
    start_price, end_price = fetch_spot_price(instance_type, now - timedelta(x_days), now)
    start_price = float(start_price)
    end_price = float(end_price)
    increase_in_price = end_price-start_price
    print(f"Price surge: {increase_in_price}")

    fetch_spot_price_only_needed_records(instance_type)



