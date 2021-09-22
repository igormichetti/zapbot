from requests import Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json

url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
parameters = {
  'start':'1',
  'limit':'5000',
  'convert':'BRL'
}
headers = {
  'Accepts': 'application/json',
  'X-CMC_PRO_API_KEY': '41d3889b-fcdd-4a41-a234-1ede763e2c4b',
}

session = Session()
session.headers.update(headers)

try:
  response = session.get(url, params=parameters)
  data = json.loads(response.text)
except (ConnectionError, Timeout, TooManyRedirects) as e:
  print(e, '...\n')
def get_coins():  
    coin_names = []
    coin_symbols = []
    i = 0
    for d in data["data"]:
        coin_names.append(d["name"].lower())
        coin_symbols.append(d["symbol"].lower())
        i += 1
        if i == 50:
            break
    return coin_names + coin_symbols

def get_keys():
    keys = []
    for d in data["data"]:
            for k in d:
                if k not in keys:
                    keys.append(k)
                else:
                    break
    return keys

def get_info(coin):
    for d in data["data"]:
            if d["name"].lower() == coin:
                qdata = d["quote"]
                brldata = qdata["BRL"]
                brldata = str(brldata).replace('{', '',1)
                brldata = brldata.replace('}', '', 1)
                return brldata
    
            if d["symbol"].lower() == coin:
                qdata = d["quote"]
                brldata = qdata["BRL"]
                brldata = str(brldata).replace('{', '',1)
                brldata = brldata.replace('}', '', 1)
                return brldata

def get_data(coin):
    for d in data["data"]:
        if d["name"].lower() == coin:
            
            print(d)
         

if __name__ == '__main__':
    
    while True:
        a = input('Coin: ').lower()
        print(get_info(a))
