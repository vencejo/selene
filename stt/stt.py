#!/usr/bin/env python3
# -*- coding: utf-8-*-
import os
import wave
import json
import tempfile
import logging
import urllib
import urlparse
import re
import subprocess
import requests
import speech_recognition as sr
import ConfigParser



class Stt():

    def __init__(self, userName=None,password =None, language='es-ES'):
        
        self.get_config()
        self.language = language
        self.r = sr.Recognizer()
        
    def get_config(self):
        
        os.chdir(os.path.dirname(os.path.realpath(__file__)))
        config = ConfigParser.ConfigParser()
        config.read('credencialesIBM-stt.ini')

        self.user = config.get('credencialesIBM-stt', 'USER')
        self.password = config.get('credencialesIBM-stt', 'PASS')
  
    def transcribe(self, audio):
        """
        Performs STT via the IBM Speech API, transcribing an audio file and
        returning an Spanish string.
        """

        try:
            mensaje = self.r.recognize_ibm(audio, username=self.user, password=self.password,
                                        language=self.language, show_all=False)
        except sr.UnknownValueError:
            mensaje = "IBM Speech to Text could not understand audio"
        except sr.RequestError as e:
            mensaje ="Could not request results from IBM Speech to Text service; {0}".format(e)
        
        finally:
            return mensaje
            
            
    def escuchaYTranscribe(self, duracion=5):
        
        m = sr.Microphone(device_index=0, sample_rate=44100)
        
        with m as source:
            
            try:
                audio = self.r.record(m, duration = duracion)
                mensaje = self.transcribe(audio)
                fraseInterpretada = mensaje.encode('utf-8')
                print(fraseInterpretada)
                return fraseInterpretada
            except sr.WaitTimeoutError:
                print("No se ha escuchado nada")
                return ""
            except :
                return ""


            
if __name__ == "__main__":
    stt = Stt()
    print("Ya puedes hablar durante 5 seg")
    stt.escuchaYTranscribe() 
