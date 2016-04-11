# coding=utf-8
import json
from os.path import join, dirname
from watson_developer_cloud import DialogV1
import re
import ConfigParser
import os

from tts.tts import sintetizador
from stt.stt import Stt
from personalidad.personalidad import Personalidad

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

while True:
    
    orden = stt.escuchaYTranscribe()
    
    if bool(re.search(r'noticias', orden, re.IGNORECASE)):
        sintetizador(dialogo('noticias'))
        
    elif bool(re.search(r'tiempo', orden, re.IGNORECASE)):
        sintetizador(dialogo('tiempo'))
        
    elif bool(re.search(r'diario', orden, re.IGNORECASE)):
        sintetizador(dialogo('diario'))
        sintetizador("Ya puede empezar a dictar")
        textoParaDiario = stt.escuchaYTranscribe(listen_time=60)
        sintetizador("Procedo a guardar la Transcripción en su diario digital")
        os.chdir(os.path.dirname(os.path.realpath(__file__)))
        rutaDiario = "/home/pi/Desktop/Dialogo/selene/personalidad/diario.txt"
        with open("/home/pi/Desktop/Dialogo/selene/personalidad/diario.txt", "a") as diario:
            diario.write(textoParaDiario)
        
        consejo = "Viendo su diario me permito darle el siguiente consejo " + \
                        personalidad.getAdviceFromFile(rutaDiario)
        sintetizador(consejo)
            
    elif bool(re.search(r'radio', orden, re.IGNORECASE)):
        sintetizador(dialogo('radio'))
        
    elif bool(re.search(r'libro', orden, re.IGNORECASE)):
        sintetizador(dialogo('libro'))
        
    elif bool(re.search(r'apagado', orden, re.IGNORECASE)):
        sintetizador(dialogo('apagado'))
        







