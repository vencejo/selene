# -*- coding: utf-8-*-

import requests
import pprint
import ConfigParser
import os


class ElTiempo():
    
    def __init__(self):
        self.get_config()
        
    def get_config(self):
        os.chdir(os.path.dirname(os.path.realpath(__file__)))
        config = ConfigParser.ConfigParser()
        config.read('datosCuentaElTiempo.ini')
        self.credenciales = config.get('datosCuentaElTiempo', 'credenciales')
        
    def elTiempoAhora(self, latitud=37.40,longitud=-1.75):
        """ Devuelve un diccionario con los valores climaticos acutales en las coordenadas dadas.
        La latitud y la longitud se han de dar con dos digitos de precision, por ejemplo:
        Coords. Pulpi: 37.40 Lat -1.75 Long """
        
        peticion = self.credenciales
        peticion += '/api/weather/v2/observations/current'
        peticion += '?units=m&geocode='+ ("2C" if latitud<0 else "") + str(latitud) + "%" + \
                    ("2C" if longitud<0 else "") + str(longitud)+ '&language=es' 
        
        res = requests.get(peticion)
        try:
            res.raise_for_status()
        except Exception as exc:
            print('There was a problem: %s' % (exc))
            
        observacion = res.json()['observation']
        
        return {'dia': observacion['dow'], 'nubes': observacion['sky_cover'], 'presion': observacion['ptend_desc'],
               'direccion del viento': observacion['wdir_cardinal'], 'velocidad del viento':observacion['metric']['wspd'],
                'temperatura aparente': observacion['metric']['feels_like'], 'indice ultravioleta': observacion['uv_desc'],
                
               }

    def elTiempo24h(self, latitud=37.40,longitud=-1.75):
        """ Devuelve un diccionario con los valores climaticos para las proximas 24h en las coordenadas dadas.
        La latitud y la longitud se han de dar con dos digitos de precision, por ejemplo:
        Coords. Pulpí: 37.40 Lat -1.75 Long """
        
        peticion = "https://5635e87f-4847-47e6-89eb-48389c89baf4:v7nWXHIh3q@twcservice.eu-gb.mybluemix.net"
        peticion += '/api/weather/v2/forecast/hourly/24hour'
        peticion += '?units=m&geocode='+ ("2C" if latitud<0 else "") + str(latitud) + "%" + \
                    ("2C" if longitud<0 else "") + str(longitud)+ '&language=es' 
        
        res = requests.get(peticion)
        try:
            res.raise_for_status()
        except Exception as exc: 
            print('There was a problem: %s' % (exc))
            
        observacion = res.json()['forecasts']
        
        probPrecipitacion24h = [observacion[i]['pop'] for i in range(24)]
        temperatura = [observacion[i]['feels_like'] for i in range(24)]
        velocidadViento = [observacion[i]['wspd'] for i in range(24)]
        indiceUltravioleta = [observacion[i]['uv_desc'] for i in range(24)]
        condicionesParaGolf = [observacion[i]['golf_category'] for i in range(24)] #No aplicable de noche
        
        return {'probPrecipitacion24h':probPrecipitacion24h, 'temperatura': temperatura, 'velocidadViento': velocidadViento,
               'indice ultravioleta': indiceUltravioleta, 'condicionesParaGolf':condicionesParaGolf}
       
        
    def resumenAlDespertar(self):
        """ Se considera que este metodo sera lanzado por la noche y ha de hacer un 
        resumen del tiempo que hara el dia siguiente (dentro de 8 horas) 
        Devuelve una tupla con la media de temperaturas del dia siguient y 
        con un booleano que dice si en alguna de las horas del día siguient 
        hay una probabilidad de precipitacion mayor del 50% """
        prevision = self.elTiempo24h()
        precipitaciones = prevision['probPrecipitacion24h'][8:-8]
        temperaturas = prevision['temperatura'][8:-8]
        return (sum(temperaturas)/8.0 ), any([p>0.5 for p in precipitaciones])
        
        
        
if __name__ == "__main__":
    
    tiempo = ElTiempo()    
    print(tiempo.resumenAlDespertar())
    pprint.pprint(tiempo.elTiempoAhora())
    print("")
    pprint.pprint(tiempo.elTiempo24h())
    
