# coding=utf-8
import json
from os.path import join, dirname
from watson_developer_cloud import DialogV1
import re
import ConfigParser
import os
import time
from mpd import MPDClient 
import sys
sys.path.insert(0,"/home/pi/Desktop/Dialogo/selene/tts")

from tts import sintetizador
from stt.stt import Stt
from personalidad.personalidad import Personalidad
from elTiempo.elTiempo import ElTiempo
from Noticias.twitter import Noticias
from Libros.libros import Lectura, InfoLibros, Libro

config = ConfigParser.ConfigParser()
config.read('credencialesIBM-dialogo.ini')

user = config.get('credenciales-dialogo', 'user')
password = config.get('credenciales-dialogo', 'password')

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
    
def mensajeRecordatorio(intervaloTiempoParaMensaje = 30 ):
    global tiempoDelUltimoMensajeEmitido
    tiempoTranscurrido = time.time() - tiempoDelUltimoMensajeEmitido
    if tiempoTranscurrido > intervaloTiempoParaMensaje:
        sintetizador("Le recuerdo que puedo decirle las noticias, el tiempo, ponerle la \
                        radio, escribir su diario o apagarme")
        tiempoDelUltimoMensajeEmitido = time.time()
    
    
## ------------------------------- PARA CREAR UN NUEVO DIALOGO --------------------------
## Hay que crear un archivo xml que lo contenga y descomentar y ejecutar el siguiente codigo
## con el nombre del nuevo archivo en el, y una vez hecho esto extraer el id del nuevo dialogo
# CREATE A DIALOG
#print(creaDialogo('selene_prueba_8','guionDialogo.xml' ))
# Print available dialogs         
#print(json.dumps(dialog.get_dialogs(), indent=2))
#dialogs = dialog.get_dialogs() 

with open("selene.img", "r") as imagenSenele:
    print(imagenSenele.read())
    
dialog_id = "f5d25932-e746-4783-b240-e53253477a3f"

initial_response = dialog.conversation(dialog_id)

conversation_id=initial_response['conversation_id']
client_id=initial_response['client_id']


tiempoDelUltimoMensajeEmitido = time.time()
# Saludo inicial y declaracion de opciones
sintetizador(initial_response['response'])

stt = Stt()
personalidad = Personalidad()
meteo = ElTiempo()
noticias = Noticias()

while True:
    
    orden = stt.escuchaYTranscribe()
    mensajeRecordatorio(intervaloTiempoParaMensaje = 60 )
    
    if bool(re.search(r'noticias', orden, re.IGNORECASE)):
        tiempoDelUltimoMensajeEmitido = time.time()
        respuesta = dialogo(entrada='noticias')
        sintetizador(respuesta)
        for noticia in noticias.daNoticias(numNoticias = 3):
            sintetizador(noticia)
            
    elif bool(re.search(r'libro', orden, re.IGNORECASE)):
        tiempoDelUltimoMensajeEmitido = time.time()
        respuesta = dialogo(entrada='libro')
        sintetizador(respuesta)
        lee = Lectura()
        info = InfoLibros()
        sintetizador("¿Quiere que le lea un libro cualquiera o uno de sus favoritos?")
        orden = stt.escuchaYTranscribe()
        if bool(re.search(r'cualquiera', orden, re.IGNORECASE)):
            ruta, numPrimerCapitulo, yaLeido = lee.empiezaALeerLibroAleatorio()
            sintetizador("¿Le ha gustado el libro?")
            orden = stt.escuchaYTranscribe()
            if bool(re.search(r'si', orden, re.IGNORECASE)):
                info.actualizaInfoLibro(Libro(ruta,numPrimerCapitulo, True))
                sintetizador("Procedo a guardar su libro en favoritos")
            if bool(re.search(r'no', orden, re.IGNORECASE)):
                info.actualizaInfoLibro(Libro(ruta,numPrimerCapitulo, False))
                sintetizador("Siento oir eso, si quiere le puedo leer otro libro")
        if bool(re.search(r'favorito', orden, re.IGNORECASE)) or \
            bool(re.search(r'favoritos', orden, re.IGNORECASE)):
            lee.leeLibroQueMeGusta()
        
    elif bool(re.search(r'tiempo', orden, re.IGNORECASE)):
        tiempoDelUltimoMensajeEmitido = time.time()
        respuesta = dialogo(entrada='tiempo')
        print(respuesta)
        sintetizador(respuesta)
        temperaturaMedia, vaALlover = meteo.resumenAlDespertar()
        sintetizador("La temperatura media mañana sera de " + str(int(temperaturaMedia))  \
                    + " grados centigrados")
        if vaALlover:
            sintetizador("Y parece que mañana va a llover")
        
    elif bool(re.search(r'diario', orden, re.IGNORECASE)):
        tiempoDelUltimoMensajeEmitido = time.time()
        respuesta = dialogo(entrada='diario')
        sintetizador(respuesta)
        sintetizador("Ya puede empezar a dictar")
        textoParaDiario = stt.escuchaYTranscribe(duracion= 20)
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
        tiempoDelUltimoMensajeEmitido = time.time()
        respuesta = dialogo(entrada='radio')
        print(respuesta)
        sintetizador(respuesta)
        radio = MPDClient()
        radio.connect("localhost",6600)
        radio.clear() # Limpia la playlist anterior
        radio.add("http://77.92.76.134:7100") # Pone una estacion de radio en la playlist
        # Busqueda de IPs de Radios en www.xatworld.com/radio-search
        radio.play()
        time.sleep(20)   # Tiempo en el que la radio estara encendida
        radio.stop()
        sintetizador(respuesta[1])
        orden = stt.escuchaYTranscribe()
        tiempoDelUltimoMensajeEmitido = time.time()
        while bool(re.search(r'si', orden, re.IGNORECASE)) or \
            bool(re.search(r'continuar', orden, re.IGNORECASE)):
            radio = MPDClient()
            radio.connect("localhost",6600)
            radio.clear() # Limpia la playlist anterior
            radio.add("http://77.92.76.134:7100")
            radio.play()
            time.sleep(20) # Tiempo en el que la radio estara encendida
            radio.stop()
            sintetizador(respuesta[1])
            orden = stt.escuchaYTranscribe()
            
        
    elif bool(re.search(r'apagado', orden, re.IGNORECASE)) or \
            bool(re.search(r'apágate', orden, re.IGNORECASE)) or \
            bool(re.search(r'adiós', orden, re.IGNORECASE)) :
        sintetizador("Buenas noches, procedo a mi apagado")
        sys.exit()
        
    else:
        print(orden)
        if orden != "":
            tiempoDelUltimoMensajeEmitido = time.time()
            respuesta = dialogo(entrada=orden)
            sintetizador(respuesta)
            print(respuesta)
        
        
        







