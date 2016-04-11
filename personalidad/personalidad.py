#!/usr/bin/env python3
# -*- coding: utf-8-*-

import json
from os.path import join, dirname
from watson_developer_cloud import PersonalityInsightsV2
import ConfigParser
import os
import random


class Personalidad():
    
    def __init__(self):
        
        self.initPersonality()
        
    def initPersonality(self):
    
        os.chdir(os.path.dirname(os.path.realpath(__file__)))
        config = ConfigParser.ConfigParser()
        config.read('config.ini')
        
        self.personality = PersonalityInsightsV2(
            username=config.get('keys', 'user'),
            password=config.get('keys', 'password'))
            
    def getPersonality(self, texto):
        personality_insights_json = {"contentItems": [{"contenttype": "text/plain", 
        "charset": "UTF-8", "language": "es-es","content": texto, "parentid": "", 
        "reply": "false", "forward": "false"}]}
        datos_json = json.dumps(self.personality.profile(text=personality_insights_json),indent=2)
        datos_dict = json.loads(datos_json)
        valores = {}
        for elem in datos_dict["tree"]["children"][2]["children"][0]["children"]:
            valores[elem["id"]] = elem["percentage"]
        return valores
        
    def getPersonalityFromFile(self, archivo):
        with open(archivo, "r") as diario:
            texto = diario.read()
            return self.getPersonality(texto)
            
    def getAdviceFromFile(self, archivo):
        os.chdir(os.path.dirname(os.path.realpath(__file__)))
        personalidad = self.getPersonalityFromFile(archivo)
        cita = ""
        if float(personalidad["Hedonism"]) > 0.5:
            with open("citas/citasParaEgoistas.cit", "r") as archivoCitas:
                citas = archivoCitas.read().splitlines()
                cita = random.choice(citas)
        elif float(personalidad["Self-transcendence"]) > 0.5:
            with open("citas/citasParaIngenuos.cit", "r") as archivoCitas:
                citas = archivoCitas.read().splitlines()
                cita = random.choice(citas)
        return cita
        
            
if __name__ == "__main__":
    
    persona = Personalidad()
    print(persona.getAdviceFromFile("diario.txt"))
    

