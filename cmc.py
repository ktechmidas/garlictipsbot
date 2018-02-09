import urllib
import json
from utils import utils
from decimal import *

grlcpriceurl = 'https://api.coinmarketcap.com/v1/ticker/garlicoin/'
dashpriceurl = 'https://api.coinmarketcap.com/v1/ticker/dash/'

utils = utils()
cursor = utils.get_mysql_cursor()

sql = "TRUNCATE TABLE rates"
cursor.execute(sql)

response = urllib.urlopen(grlcpriceurl)
data = json.loads(response.read())
grlcprice = round(Decimal(data[0]['price_usd']),8)

response = urllib.urlopen(dashpriceurl)
data = json.loads(response.read())
dashprice = round(Decimal(data[0]['price_usd']),8)

sql = "INSERT INTO rates (pair,rate) VALUES (%s, %s)"
pair = "GRLC/DASH"
rate = grlcprice/dashprice
cursor.execute(sql, (pair,rate,))

pair = "DASH/GRLC"
rate = dashprice/grlcprice
cursor.execute(sql, (pair,rate,))
