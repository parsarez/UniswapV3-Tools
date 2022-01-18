import requests
import csv
from datetime import datetime, timedelta
import calendar

# pretty print is used to print the output in the console in an easy to read format
from pprint import pprint
from csv import writer

# function to use requests.post to make an API call to the subgraph url
def run_query(q):

    # endpoint where you are making the request
    request = requests.post('https://api.thegraph.com/subgraphs/name/ianlapham/arbitrum-minimal'
                            '',
                            json={'query': query})
    if request.status_code == 200:
        return request.json()
    else:
        raise Exception('Query failed. return code is {}.      {}'.format(request.status_code, query))

#Get yesterday's date
yesterday = datetime(2021, 12, 29)
utc_time = calendar.timegm(yesterday.utctimetuple())

beforeadditionquery = """
{
poolDayDatas(orderDirection: desc, first: 1000
where: {
  date: %s
} orderBy: volumeUSD){
  date
  volumeUSD
  feesUSD
  tvlUSD
  pool{
    feeTier
token0{
symbol}
token1{
symbol}
  }
}
}
"""

query = beforeadditionquery % (utc_time)

result = run_query(query)
#pprint(result)

datelist = []
token0symbollist = []
token1symbollist = []
feetierlist = []
tvlUSDlist = []
volumeUSDlist = []
feesUSDlist = []
APRlist = []


for key in result["data"]["poolDayDatas"]:
    datelist.append(datetime.utcfromtimestamp(key["date"]).strftime('%Y-%m-%d'))
    token0symbollist.append(key["pool"]["token0"]["symbol"])
    token1symbollist.append(key["pool"]["token1"]["symbol"])
    feetierlist.append(key["pool"]["feeTier"])
    tvlUSDlist.append(key["tvlUSD"])
    volumeUSDlist.append(key["volumeUSD"])
    feesUSDlist.append(key["feesUSD"])
    APRlist.append('=G2*365/E2')


list = zip(datelist, token0symbollist, token1symbollist,feetierlist, tvlUSDlist, volumeUSDlist, feesUSDlist, APRlist)

header = ['Date', 'Token0', 'Token1', 'FeeTier', 'TVLUSD', 'VolumeUSD', 'FeesUSD', 'APR']

with open('arbitrumunidata.csv', 'w') as f:
    writer = csv.writer(f)
    writer.writerow(header)
    for line in list:
        writer.writerow(line)
