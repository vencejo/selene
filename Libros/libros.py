# -*- coding: utf-8-*-

from ebooklib import epub
import bs4
from tts import sintetizador
from itertools import islice
import os
import random
import pickle

enDepuracion = True
rutaInicial = os.getcwd()

class Libro():
    
    def __init__(self, ruta, numCapLeidos,meGusta):
        self.ruta = ruta
        self.numCapLeidos = numCapLeidos
        self.meGusta = meGusta
        
    def __repr__(self):
        return "ruta: %s, numCapLeidos: %s, meGusta: %s" % \
                (self.ruta, self.numCapLeidos, self.meGusta)
                
class InfoLibros():
    """ En esta clase van los metodos para trabajar con la informacion de los libros 
    que se ira guardando en archivos pickle """
    
    def __init__(self, nombreArchivo = "librosLeidos.pickle"):
        self.archivo = nombreArchivo
        
    def actualizaInfo(self, listaDeLibrosLeidos):
        """ Actualizamos los datos sobre nuestros gustos literarios guardados en disco """
        os.chdir(rutaInicial)
        
        if os.path.isfile(self.archivo): # si el archivo ya existe , lo abrimos y lo extendemos
            with open(self.archivo, "rb") as archivo:
                anteriorListaLibrosLeidos = pickle.load(archivo)
                listaDeLibrosLeidos.extend(anteriorListaLibrosLeidos)
        
        with open(self.archivo, "wb") as archivo:
            pickle.dump(listaDeLibrosLeidos, archivo)
            
    def actualizaInfoLibro(self, libro):
        """ Actualiza la info de un libro individual dentro de la lista de libros Guardada
        El archivo de la lista de Libros ha de existir 
        Devuelve verdadero si el libro estaba en la lista o falso si no lo estaba"""
        listaLibros = self.getInfo()
        for ind,lib in enumerate(listaLibros):
            if lib.ruta == libro.ruta:
                del listaLibros[ind]
                listaLibros.append(Libro(libro.ruta,libro.numCapLeidos, libro.meGusta))
                os.chdir(rutaInicial)
                with open(self.archivo, "wb") as archivo:
                    pickle.dump(listaLibros, archivo)
                return True
        # El libro no esta en la lista guardada
        listaLibros.append(Libro(libro.ruta,libro.numCapLeidos, libro.meGusta))
        os.chdir(rutaInicial)
        with open(self.archivo, "wb") as archivo:
            pickle.dump(listaLibros, archivo)
        return False
        
            
    def getInfo(self):
        os.chdir(rutaInicial)
        if os.path.isfile(self.archivo):
            with open(self.archivo, "rb") as archivo:
                listaLibros = pickle.load(archivo)
                return listaLibros
        return []
        
    def libroYaLeido(self, rutaLibro):
        """ Devuelve verdadero si el libro se ha leido ya o falso en caso contrario """
        listaLibrosLeidos = self.getInfo()
        for libro in listaLibrosLeidos:
            if libro.ruta == rutaLibro:
                return True
        return False
        
    def consultaInfoLibro(self, rutaLibro):
        """ Busca el libro en la lista de los leidos y devuelve su info, si no lo encuentra
        devuelve None """
        listaLibrosLeidos = self.getInfo()
        for libro in listaLibrosLeidos:
            if libro.ruta == rutaLibro:
                return libro
        return None
        
            
    def consultaInfo(self):
        with open(self.archivo, "rb") as archivo:
            datos= pickle.load(archivo)
            print("*"*30)
            print("Numero de libros leidos = %s" % str(len(datos)))
            print("")
            for libro in datos:
                print("")
                print(libro.ruta)
                print(libro.numCapLeidos)
                print(libro.meGusta)
            print("")
            print("*"*30)
   
   
class Lectura():
    
    def __init__(self):
        pass
   
    def leeLibroQueMeGusta(self):
        info = InfoLibros()
        listaLibros = info.getInfo()
        # Busco aleatoriamente un libro que me guste y lo leo
        random.shuffle(listaLibros)
        for indice,libro in enumerate(listaLibros):
            if libro.meGusta:
                self.sintetizaCapitulo(libro.ruta, libro.numCapLeidos+1)
                # Actualizo la informacion guardada en disco sobre los libros
                libro.numCapLeidos += 1
                info.actualizaInfoLibro(libro)
                return True
        # Si no encuentra ningun libro que me gusta devuelve falso
        return False
        
                
    
    def empiezaALeerLibroAleatorio(self):
        """ Empieza a leer un libro de manera aleatoria, si ya se habia leido , empieza 
        por el capitulo que se quedo """
        rutaDirLibro, contDirLibro = self.buscaRutaAleatoriaALibro()
        if not enDepuracion:
            sintetizador("Voy a proceder a leer el siguiente libro: ")
            sintetizador(libro)
        os.chdir(rutaDirLibro)
        for elem in contDirLibro:
            if elem.find('epub') != -1:
                ruta = os.path.join(os.getcwd(),elem)
                #Comprueba si este libro se ha leido ya y su info esta guardada en disco
                # En cuyo caso empieza a leerlo por el capito que se quedo
                info = InfoLibros()
                infoLibro = info.consultaInfoLibro(ruta)
                if infoLibro is not None:
                    #Este libro ya ha sido leido
                    self.sintetizaCapitulo(ruta, infoLibro.numCapLeidos + 1)
                    nuevaInfoLibro = Libro(ruta, infoLibro.numCapLeidos + 1, infoLibro.meGusta)
                    info.actualizaInfoLibro( nuevaInfoLibro)
                    yaLeido = True
                    return (ruta, infoLibro.numCapLeidos + 1, yaLeido)
                else:
                    # Libro no leido, leo el libro y guardo la informacion de su lectura en disco
                    numPrimerCapitulo = self.leePrimerCapitulo(ruta)
                    yaLeido = False
                    return (ruta, numPrimerCapitulo, yaLeido)
                    
                        
                
    def buscaRutaAleatoriaALibro(self):
        os.chdir(os.path.join(rutaInicial,'./Literatura/Libros_Descargados'))
        listaAutores = os.listdir('.')
        autor = random.choice(listaAutores)
        os.chdir(os.path.join(os.getcwd(),autor))
        listaLibros = os.listdir('.') 
        libro = random.choice(listaLibros)
        os.chdir(os.path.join(os.getcwd(),libro))
        contDirLibro = os.listdir('.')
        rutaLibro = os.getcwd()
        return (rutaLibro, contDirLibro)
    
    def leePrimerCapitulo(self,ruta):
        """ Busca y lee el primer capitulo legible,
        devuelve el numero de capitulo"""
        for capitulo in range(1,10):
            if not self.sintetizaCapitulo(ruta, capitulo):
                continue
            else:
                return capitulo
    
    def sintetizaCapitulo(self,ruta, numCapitulo, numMinCaracteres = 500): 
        """ Devuelve verdadero si ha conseguido sintetizar algún texto o falso si no """
        libro = epub.read_epub(ruta)
        capitulo = next(islice(libro.get_items(),numCapitulo,None), None)
        algunTextoSintetizado = False
        if isinstance(capitulo, epub.EpubHtml):
            # print(item.get_content())
            soup = bs4.BeautifulSoup(capitulo.get_content())
            listaTextos = self.preparaTextoParaSintetizar(soup)
            for fragmento in listaTextos:
                print(fragmento)
                if len(fragmento) > numMinCaracteres:
                    algunTextoSintetizado = True
                    if enDepuracion:
                        print(fragmento)
                    else:
                        sintetizador(fragmento)
        return algunTextoSintetizado
            
    def preparaTextoParaSintetizar(self, html):
        """ Toma un texto en forma de html , extrae el texto puro y lo trocea en subtextos 
        de 2000 caracateres o menos para poder mandarlos a Bluemix
        La funcion entrega una lista con los subtextos  """
        lonSinte = 2000
        texto = html.get_text().strip()
        listaTextos = [texto[i:i+lonSinte] for i in range(0,len(texto),lonSinte) ]  
        return listaTextos  
        
if __name__ == "__main__":
    
    info = InfoLibros()
    lee = Lectura()
    
    ruta, numPrimerCapitulo, yaLeido = lee.empiezaALeerLibroAleatorio()
    opinion = raw_input("Te ha gustado lo que has leido? (s/n)")
    if opinion == "s":
        info.actualizaInfoLibro(Libro(ruta,numPrimerCapitulo, True))
    else:
        info.actualizaInfoLibro(Libro(ruta,numPrimerCapitulo, False))
        
    # Consulto los datos Guardados
    info.consultaInfo()
    
    # Lee un libro ya leido 
    lee.leeLibroQueMeGusta()
    
    # Consulto los datos Guardados
    info.consultaInfo()
    
        
    
    
    #libro = 'Cita con Rama - Arthur C. Clarke.epub'
    #sintetizaCapitulo(libro, 5)
    
    
    
