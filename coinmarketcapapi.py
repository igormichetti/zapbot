import json
import os
from requests import Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
from dotenv import load_dotenv

load_dotenv()
CMC_API_KEY = os.environ.get('CMC_API_KEY')
url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
parameters = {
  'start':'1',
  'limit':'5000',
  'convert':'BRL'
}
headers = {
  'Accepts': 'application/json',
  'X-CMC_PRO_API_KEY': CMC_API_KEY,
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

def get_info(coin) -> str:
  for d in data["data"]:
    if d["name"].lower() == coin:
        qdata = d["quote"]
        brldata = qdata["BRL"]
        brldata = str(brldata).replace('{', '',1)
        brldata = brldata.replace("'", '')
        brldata = brldata.replace('}', '', 1)
        strcoin = coin.title()
    if d["symbol"].lower() == coin:
                
      qdata = d["quote"]
      brldata = qdata["BRL"]
      brldata = str(brldata).replace('{', '',1)
      brldata = brldata.replace("'", '')
      brldata = brldata.replace('}', '', 1)
      strcoin = f'${coin.upper()}'

  info = f'Ultima atualizacao de {strcoin}' + ':\n\n'
  return info+brldata

def get_data(coin):
    for d in data["data"]:
        if d["name"].lower() == coin:
            
            print(d)
         

if __name__ == '__main__':
    
    while True:
        a = input('Coin: ').lower()
        print(get_info(a))
