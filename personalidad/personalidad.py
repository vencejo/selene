#!/usr/bin/env python3
# -*- coding: utf-8-*-

import json
from os.path import join, dirname
from watson_developer_cloud import PersonalityInsightsV2
import ConfigParser
import os


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
        print(json.dumps(self.personality.profile(text=personality_insights_json), indent=2))
        
if __name__ == "__main__":
    
    texto = """ Me creen malo, y lo sé – decía -. 
            Pero me es igual. No quiero conocer a nadie excepto a los que aprecio, 
            y a éstos les quiero tanto que hasta daría la vida por ellos; a los demás, 
            los pisotearía si los hallara en mi camino. Tengo una madre inapreciable, 
            que adoro, dos o tres amigos (tú uno de ellos), y en cuanto a los otros poco 
            me importa que me sean útiles o perjudiciales. Y casi todos estorban, 
            las mujeres las primeras. Sí, amigo mío; he tropezado con  hombres enamorados, 
            nobles y elevados, pero mujeres, salvo las que se venden (condesa o cocinera, 
            que para el caso es lo mismo), no he hallado ninguna. 
            Todavía no me ha sido dado hallar la pureza celestial, 
            la devoción que busco en la mujer. Si hallara una, le daría mi vida. 
            Y las demás… – hizo un gesto despreciativo -. 
            Puedes creerme que si aún me interesa la vida es porque espero hallar 
            a esa criatura divina que me purificará, me regenerará, me elevará. 
            Pero tú no puedes comprender esto… """
    
    palabras = texto.split(" ")
    print(len(palabras))
    persona = Personalidad()
    persona.getPersonality(texto)
    

