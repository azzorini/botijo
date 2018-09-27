#!/usr/bin/python
# -*- coding: utf-8 -*-

import telebot # Libreria de la API del bot.
from telebot import types # Tipos para la API del bot.
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw 
import time # Librería para hacer que el programa que controla el bot no se acabe.
import random
import logging
import tresenraya as TER

TOKEN = '' # Nuestro token del bot (el que @BotFather nos dió).

partidas = {}

commands = {  # command description used in the "help" command

              'start': 'Inicia el bot',
              'help': 'Ayuda del botijario',
			  'chiste': 'Chiste 100tifiko',
			  'einstein': 'Meme de einstein con el texto que se le pase',
			  'tres': 'Unirse/crear una partida de tres en raya',
			  'juego': 'Hacer un movimiento en la partida (/juego b2)'
}

chistes = ["Van dos y se cae PRADO",
		   "Making bad chemistry jokes because all the good ones argon",
		   "¿Qué dice un grupo CH3 en lo alto de un tejado?\n¿Metilo o no metilo?",
		   "1 de cada 10 personas saben binario",
		   "Mi mujer tiene un gran físico - Albert Einstein",
		   "¿Cuál es la fórmula del agua bendita?\nH DIOS O",
		   "¿Qué es un langostino?\nUna langosta con un triple enlace",
		   "No soporto a los químicos, lo sodio",
		   "-¿Cuántos físicos hacen falta para cambiar una bombilla?\n-Dos, uno para sujetar la bombilla y otro para rotar el universo.",
		   "¿Cuál es la ley física más zen?\nLa ley de Ohm",
		   "Fotón a protón:\n-Hey, vente a la fiesta, vamos a ir unos cuantos."]

class Partida:
	def __init__(self, cid, player1):
		self.juego = TER.Partida3EnRaya()
		self.cid = cid
		self.jugador = player1
		self.jugador1 = player1
		self.completo = False
		self.victoria = ' '
	
	def add_player2(self, player2):
		if (self.juagdor2 != 0):
			self.juagdor2 = player2
			return True
		return False
	
	def jugada(self, jugador, letra, numero):
		if (jugador == self.jugador):
			if (self.juego.jugada(letra, numero))
				if (self.juego.victoria != ' '):
					self.victoria = self.juego.victoria
				return True
		return False

bot = telebot.TeleBot(TOKEN) # Creamos el objeto de nuestro bot.
#############################################
#Listener
def listener(messages): # Con esto, estamos definiendo una función llamada 'listener', que recibe como parámetro un dato llamado 'messages'.
	for m in messages: # Por cada dato 'm' en el dato 'messages'
		if m.content_type == 'text': # Filtramos mensajes que sean tipo texto.
			cid = m.chat.id # Almacenaremos el ID de la conversación.
			print("[" + str(cid) + "]: " + m.text) # Y haremos que imprima algo parecido a esto -> [52033876]: /start

bot.set_update_listener(listener) # Así, le decimos al bot que utilice como función escuchadora nuestra función 'listener' declarada arriba.
#############################################
#Funciones
@bot.message_handler(commands=['start'])
def command_start(m):

	cid = m.chat.id
	bot.send_message(cid, "Arrancando BOTIJO...\n¡Buenas! ¿En qué puedo servirle?")
	command_help(m)

@bot.message_handler(commands=['help'])
def command_help(m):

    cid = m.chat.id

    help_text = "Los siguientes comando están disponibles:\n\n"

    for key in commands:  # generate help text out of the commands dictionary defined at the top
        help_text += "/" + key + ": "
        help_text += commands[key] + "\n"

    bot.send_message(cid, help_text)  # send the generated help page

@bot.message_handler(commands=['chiste']) # Indicamos que lo siguiente va a controlar el comando '/miramacho'
def command_comentario(m): # Definimos una función que resuleva lo que necesitemos.
	cid = m.chat.id # Guardamos el ID de la conversación para poder responder.
	bot.send_message( cid, random.choice(chistes)) # Con la función 'send_message()' del bot, enviamos al ID almacenado el texto que queremos.

@bot.message_handler(commands=['einstein'])
def einstein(m):
	cid = m.chat.id
	texto = m.text[len("/einstein "):]
	
	i = 40
	sigue = True
	while (i < len(texto) and sigue):
		while (texto[i] != ' ' and sigue):
			i -= 1
			if (i <= 0 or texto[i] == "\n"):
				sigue = False
		if (sigue):
			texto = texto[:i] + "\n" + texto[i:]
			i += 41
		

	img = Image.open("Einstein.jpg")
	draw = ImageDraw.Draw(img)
	font = ImageFont.truetype("impact.ttf", 32)
	draw.text((550, 250), texto + "\n\n                                             Albert Einstein",(255,255,255),font=font)
	img.save('Meme.jpg')
	bot.send_photo(cid, open('Meme.jpg', 'rb'))

@bot.message_handler(commands=['tres'])
def command_tres(m):
	cid = m.chat.id
	if (partidas.get(cid) == None):
		partidas[cid] = Partida(cid, m.from_user)
		bot.send_message(cid, "Partida iniciada por: " + str(m.from_user))
	elif (not(partidas[cid].completo)):
		partidas[cid].add_player2(m.from_user)
		bot.send_message(cid, str(m.from_user) + " se ha unido a la partida")
	else:
		bot.send_message(cid, "Ya hay una partida en marcha")

@bot.message_handler(commands=['juego'])
def command_juego(m):
	cid = m.chat.id
	

@bot.message_handler(func=lambda message: message.text.lower() == "hola")
def saludo(m):
	cid = m.chat.id
	bot.reply_to(m, "Salu2 100tifkos")
	
@bot.message_handler(func=lambda message: "prado" in message.text.lower())
def saludo(m):
	bot.reply_to(m, "¿Otra vez se ha caído el PRADO?")

@bot.message_handler(func=lambda message: "botijo" in message.text.lower())
def aludido(m):
	bot.reply_to(m, "Sí, BOTIJO es mi nombre, no lo uses mucho que se desgasta")

#############################################

#Peticiones
logger = logging.getLogger(__name__)

while True:

    try:

            bot.polling(none_stop=True)

    except Exception as err:

            logger.error(err)

            time.sleep(10)

            print('Error en la conexión')
