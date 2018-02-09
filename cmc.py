import urllib
import json
from utils import utils

grlcpriceurl = 'https://api.coinmarketcap.com/v1/ticker/garlicoin/'
dashpriceurl = 'https://api.coinmarketcap.com/v1/ticker/dash/'

utils = utils()
cursor = utils.get_mysql_cursor()

response = urllib.urlopen(grlcpriceurl)
data = json.loads(response.read())
grlcprice = data[0]['price_usd']

response = urllib.urlopen(dashpriceurl)
data = json.loads(response.read())
dashprice = data[0]['price_usd']

sql = "INSERT INTO rates (pair,rate) VALUES (%s, %s)"
pair = "GRLC/DASH"
rate = grlcprice/dashprice
cursor.execute(sql, (pair,rate,))

pair = "DASH/GRLC"
rate = dashprice/grlcprice
cursor.execute(sql, (pair,rate,))