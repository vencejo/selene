# coding=utf-8
import json
from os.path import join, dirname
from watson_developer_cloud import DialogV1
import re
import ConfigParser
import os
import time
from mpd import MPDClient 

from tts.tts import sintetizador
from stt.stt import Stt
from personalidad.personalidad import Personalidad
from elTiempo.elTiempo import ElTiempo
from Noticias.twitter import Noticias

config = ConfigParser.ConfigParser()
config.read('datosCuentaDialogoIBM.ini')

user = config.get('datosIBM', 'user')
password = config.get('datosIBM', 'password')

dialog = DialogV1(username=user,password=password)

conversation_id= ""
client_id= ""

def creaDialogo(nombre, archivo):
    with open(join(dirname(__file__), archivo)) as dialog_file:
        return(json.dumps(dialog.create_dialog(
            dialog_file=dialog_file, name=nombre), indent=2))
            
def dialogo(entrada=""):
    respuesta = dialog.conversation(dialog_id=dialog_id,
                                      dialog_input= entrada,
                                      conversation_id=initial_response['conversation_id'],
                                      client_id=initial_response['client_id'])
    return respuesta["response"]

# CREATE A DIALOG
# print(creaDialogo('selene_prueba_2','guionDialogo.xml' ))
# Print available dialogs         
#print(json.dumps(dialog.get_dialogs(), indent=2))

dialogs = dialog.get_dialogs() 

dialog_id = dialogs["dialogs"][2]["dialog_id"]

initial_response = dialog.conversation(dialog_id)

conversation_id=initial_response['conversation_id']
client_id=initial_response['client_id']

# Saludo inicial y declaracion de opciones
sintetizador(initial_response['response'])

stt = Stt()
personalidad = Personalidad()
meteo = ElTiempo()
noticias = Noticias()

while True:
    
    orden = stt.escuchaYTranscribe()
    
    if bool(re.search(r'noticias', orden, re.IGNORECASE)):
        sintetizador(dialogo('noticias'))
        for noticia in noticias.daNoticias():
            sintetizador(noticia)
        
    elif bool(re.search(r'tiempo', orden, re.IGNORECASE)):
        sintetizador(dialogo('tiempo'))
        temperaturaMedia, vaALlover = meteo.resumenAlDespertar()
        sintetizador("La temperatura media mañana sera de " + str(temperaturaMedia)  \
                    + " grados centigrados")
        if vaALlover:
            sintetizador("Y parece que mañana va a llover")
        
    elif bool(re.search(r'diario', orden, re.IGNORECASE)):
        sintetizador(dialogo('diario'))
        sintetizador("Ya puede empezar a dictar")
        textoParaDiario = stt.escuchaYTranscribe(duracion= 30)
        print("****************************")
        print(textoParaDiario)
        print("****************************")
        if textoParaDiario.startswith("IBM Speech to Text could not understand"):
            sintetizador("No he entendido lo que ha dicho")
            continue
        sintetizador("Procedo a guardar la Transcripción en su diario digital")
        os.chdir(os.path.dirname(os.path.realpath(__file__)))
        rutaDiario = "/home/pi/Desktop/Dialogo/selene/personalidad/diario.txt"
        with open("/home/pi/Desktop/Dialogo/selene/personalidad/diario.txt", "a") as diario:
            diario.write(textoParaDiario +"\n")
        
        consejo = personalidad.dameConsejoSegunArchivo(rutaDiario)
        sintetizador("Viendo su diario me permito darle el siguiente consejo .......... ")
        time.sleep(1.5)
        sintetizador(consejo)
            
    elif bool(re.search(r'radio', orden, re.IGNORECASE)):
        sintetizador(dialogo('radio'))
        radio = MPDClient()
        radio.connect("localhost",6600)
        radio.clear() # Limpia la playlist anterior
        radio.add("http://77.92.76.134:7100") # Pone una estacion de radio en la playlist
        # Busqueda de IPs de Radios en www.xatworld.com/radio-search
        radio.play()
        time.sleep(20)
        radio.stop()
        
    elif bool(re.search(r'apagado', orden, re.IGNORECASE)):
        sintetizador(dialogo('apagado'))
        
        







