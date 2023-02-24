import requests

def obtener_precio_dolar():
    url = 'https://api.exchangeratesapi.io/latest?base=USD'
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(url, headers=headers)
    data = response.json()
    precio_dolar = data['rates']['EUR']
    return precio_dolar
