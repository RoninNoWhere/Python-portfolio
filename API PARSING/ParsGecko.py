import requests

#checking prices of different crypto from the web site CoinGecko
url = 'https://api.coingecko.com/api/v3/simple/price'

#parametrs of the request
params = {

'ids': 'bitcoin,ethereum,litecoin', #crypto id
'vs_currencies': 'usd,eur' #currencies
}

#GET-request to CoinGecko API 
response = requests.get(url, params=params)

#success check
if response.status_code == 200:
#Parsing the response in JSON format
     data = response.json()

#Display current prices of cryptocurrencies in USD and EUR
for crypto, prices in data.items():
        print(f"Crypto: {crypto.capitalize()}")
        print(f"Price in USD: {prices['usd']}")
        print(f"Price in EUR: {prices['eur']}\n")
else:
        print(f"Error: can't get data. Error code: {response.status_code}")