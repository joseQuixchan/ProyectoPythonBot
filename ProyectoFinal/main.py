from cgitb import text
from unicodedata import name
import requests
from telebot.types import ReplyKeyboardMarkup
from telebot.types import ForceReply 
from constantes import * #Importacion de la clse que contiene el token
import telebot #Libreria para la API de telegram
import clima as C

bot = telebot.TeleBot(API_KEY) #Instanciamos el bot de telegram con el token respectivo

print("¡El bot ha inicado con exito!") #Indiqca que el bot esta corriendo
datos = [] #Declaramos la lista donde se almacenara los datos del usuairo

@bot.message_handler(commands=["start", "Start"]) #Declaracion para el comando start
def start_command(message): #Recive como argumento el mensaje start "el argumento message es un Json con informacion del usuario"
    bot.reply_to(message, "¡Hola! \npuedes utilizar los siguientes comandos /Bitacora y /Weather, si necesitas ayuda puedes usar /help.") #Cita el mensaje enviado y responde un texto

@bot.message_handler(commands=["help", "Help"]) #Declaracion para el comando help
def help_command(message):
    bot.reply_to(message, "Actualmente puedes interactuar de 2 formas:" 
    +"\nCon el comando /Bitacora que te invitará a contestar una serie de preguntas"
    +"\nCon el comando /Weather para conocer la informacion del clima actual en tu ciudad."
    +"\nSi necesitas mas ayuda puedes preguntarle a Google.") #Cita el mensaje enviado y responde un texto

@bot.message_handler(commands=["weather", "Weather"]) #Responde al comando weather
def weather_command(message):
    markup = ForceReply()
    msg = bot.send_message(message.chat.id, "¿Nombre de tu ciudad?", reply_markup=markup) #almacenamos en una baritable lo que le usuario responda a la pregunta
    bot.register_next_step_handler(msg, saber_clima) #regista la respuesta y manda la respuesta a otra funcion
   
def saber_clima(message): #Funcion para el clima   
    ciudad = message.text #Sacamos el mensaje del Json messaje para optener la ciudad
    response = requests.get("http://api.weatherapi.com/v1/current.json?key=51df2be0422945f4bb831625222506&q="+ ciudad + "&aqi=no") #instanciamos la api del clima al cual le pasamos la ciudad ingresada
    print(response)
    respuesta = response.json() #Recivimos un Json de la api del clima
    city = respuesta['location']['name'] #Almacenamos los datos necesario
    pais = respuesta['location']['country']
    temperatura = respuesta['current']['temp_c']
    entorno = respuesta['current']['condition']['text']
    icon = respuesta['current']['condition']['icon']
    bot.reply_to(message, "Ciudad: "+str(city)+", Pais: "+str(pais)+", Temp: "+str(temperatura)+"Cº,  Entorno: "+str(entorno)+ "\n"+str(icon)) #El bot contesta los datos selecionados

@bot.message_handler(commands=["Bitacora","bitacora", "Bitácora","bitácora"])
def bitacora_command(message):
    markup = ForceReply()
    msg = bot.send_message(message.chat.id, "Bienvenido a la Bitácora\n¿Cuál es tu nombre?", reply_markup=markup) #guardamos la respuesta a la pregunta en una variable
    bot.register_next_step_handler(msg, edad)#mandamos la respuesta junto con otra funcion
   
def edad(message):
    datos.append(message.text) #almacenamos en una lista la posicion text del Json del mensaje de la respuesta anterior
    markup = ForceReply()
    msg = bot.send_message(message.chat.id, "¿Cuál es tu edad? (ingrese solo el número)", reply_markup=markup)
    bot.register_next_step_handler(msg, sentir)
    

def sentir(message):
    datos.append(message.text)
    markup = ForceReply()
    msg = bot.send_message(message.chat.id, "¿Como te sientes hoy?", reply_markup=markup)
    bot.register_next_step_handler(msg, mejorar)
 
def mejorar(message):
    datos.append(message.text)
    markup = ForceReply()
    msg = bot.send_message(message.chat.id, "¿Que mejorarias en tu vida?", reply_markup=markup)
    bot.register_next_step_handler(msg, metas)


def metas(message):
    datos.append(message.text)
    markup = ForceReply()
    msg = bot.send_message(message.chat.id, "¿Que metas tienes para hoy?", reply_markup=markup)
    bot.register_next_step_handler(msg, agradecimiento)


def agradecimiento(message):
    datos.append(message.text) #se almacena todos los datos de las respuesta a las pregutnas
    bot.send_message(message.chat.id, "Nombre del usuario: " + datos[0] + "\n" + "Edad: " + datos[1] + "\n" + "Sentimiento: " + datos[2] + "\n" + "Mejorar en vida: " + datos[3] + "\n" + "Metas: " + datos[4])#Responde al usariio un resumen de los datos ingresados
    print(datos)
    datos.clear() #limpia la lista a vacia

@bot.message_handler(content_types=["text"]) #Controlador de palabras no conocidad y comando no conocidos
def respuestas_simples(message):
    mensaje=message.text.lower()
    if mensaje.startswith("/"):
        bot.send_message(message.chat.id, "Comando no disponible")
    elif mensaje == "bitacora" or mensaje == "bitácora":
        bitacora_command(message)
    elif mensaje == "weather":
        weather_command(message)
    else: 
        bot.send_message(message.chat.id, "Hola, Soy Climatobot\n Utiliza el comando /help si necesitas ayuda")



bot.infinity_polling() #Bucle que deja escuchando al bot infinitamente


