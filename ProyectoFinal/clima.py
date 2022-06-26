from unicodedata import name
import requests
def saber_clima(message):
    ciudad = message.text
    response = requests.get("http://api.weatherapi.com/v1/current.json?key=51df2be0422945f4bb831625222506&q="+ ciudad + "&aqi=no")
    print(response)
    respuesta = response.json()
    territorio = respuesta['location']['name']
    temperatura = respuesta['current']['temp_c']
    entorno = respuesta['current']['condition']['text']
    