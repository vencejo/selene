Selene
======

![Selene](http://www.guadatech.com/wp-content/uploads/2016/04/selene.jpg)

#### Asistente domótico nocturno con Raspberry Pi multifuncional con capacidades cognitivas aumentadas gracias a IBM-Watson


La idea
--------
Este proyecto surge como una continuación lógica de 
[nuestro anterior trabajo con Jasper](https://github.com/vencejo/reconocimiento-de-voz-con-RaspberryPi), 
en el que vimos como la inclusión de servicios en la nube de IBM simplificaban en gran medida 
el código y la mantenibilidad del asistente vocal.

Con Selene hemos avanzado en este sentido, haciendo  un uso intensivo de la nube de IBM Bluemix.

En concreto, se trata de  la realización de una prueba de concepto de un “asistente personal nocturno” 
consistente en una Raspberry Pi con Micrófono y Altavoces en la parte hardware colocado todo esto 
de manera discreta en la mesita de noche junto a la cama del usuario.

**La idea es que antes de dormirte puedas hablar con Selene y pedirle que te lea las noticias, 
te ponga la radio, te lea un libro ,te diga el tiempo que va a hacer mañana, 
y escuche tu relato del día guardándolo en tu pequeño diario digitalizado.**


Videos demostrativos
--------------------

[![video demostrativo modo lectura](https://img.youtube.com/vi/cs2oBUR-p8o/0.jpg)](https://www.youtube.com/watch?v=cs2oBUR-p8o)

*Nuevo modo lectura de libros*



[![video demostrativo](https://img.youtube.com/vi/uigE7JxHXR4/0.jpg)](https://www.youtube.com/watch?v=uigE7JxHXR4)

*Funcionamiento general*


Dependencias
------------

* [IBM-Bluemix python-sdk](https://github.com/watson-developer-cloud/python-sdk)
* [Speech Recognition Python Library](https://github.com/Uberi/speech_recognition)
* [ebooklib](https://github.com/aerkalov/ebooklib)
* [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)
* [Tweepy](https://github.com/tweepy/tweepy)
* [Radio en el terminal con mpd](http://www.morethanfunctional.org/raspberry-pi-webradio-mpd-mpc-via-linux-shell-droid-android/)
* [Cliente Python para mpd](https://github.com/Mic92/python-mpd2)


Descarga de los libros
----------------------
En [este enlace](https://www.dropbox.com/sh/9h29ainsprsyltj/AAA2w9vhmYbAxx9U8t8Q9WYba?dl=0) 
están los libros que habria que descargar en un subdirectorio con el nombre 
"selene/Literarura/Libros_Descargados" borrando el contenido que inicalmente tiene (que sirve de muestra de los 
libros disponibles) y sustituyendolo por las carpetas de los libros , que contienen los archivos
.epub propiamente dichos que son los que lee el programa


Funcionamiento y credenciales
-----------------------------
Para hacer funcionar a Selene hay que ejecutar el programa "dialogo.py" de la carpeta selene.

Normalmente una primera ejecución dará error aún cuando se hayan instalado todas las 
dependencias ya que el programa no habrá encontrado los archivos ".ini" con las credenciales
de los servicios que hay que tener para ponerlos en cada módulo.

Así, en la carpeta principal, junto al propio programa "dialogo.py" , el propio usuario, ha
de crear un archivo con el nombre 'credencialesIBM-dialogo.ini' donde se pondrán las 
credenciales del servicio de Dialogo de Watson , en el que , claro está , el usuario tendría 
que darse de alta previamente , siendo este el aspecto del archivo :

    [credenciales-dialogo]
    user: aqui-va-el-usuario-del-servicio-dialogo-sin-comillas
    password: aqui-va-la-contraseña-del-servicio-dialogo-sin-comillas


Hay que realizar la misma operacion en la carpeta "tts" donde hay que crear el archivo
"credencialesIBM-tts.ini" con el siguiente aspecto y las credenciales del servicio Text-to-Speech

    [credenciales-tts]
    user: aqui-va-el-usuario-del-servicio-tts-sin-comillas
    password: aqui-va-la-contraseña-del-servicio-tts-sin-comillas


En la carpeta "stt"  hay que crear el archivo"credencialesIBM-stt.ini" con el siguiente 
aspecto y las credenciales del servicio Speech-to-text

    [credenciales-stt]
    user: aqui-va-el-usuario-del-servicio-stt-sin-comillas
    password: aqui-va-la-contraseña-del-servicio-stt-sin-comillas
    
En la carpeta "personalidad"  hay que crear el archivo "credencialesIBM-personalidad.ini" 
con el siguiente aspecto y las credenciales del servicio Personalidad

    [credenciales-personalidad]
    user: aqui-va-el-usuario-del-servicio-personalidad-sin-comillas
    password: aqui-va-la-contraseña-del-servicio-personalidad-sin-comillas

Y por último, en la carpeta "Noticias" hay que crear el archivo "datosCuentaTwitter.ini" con un formato
como el siguiente

    [datosTwitter]
    APP_KEY: la-key-de-la-aplicacion-sin-comillas
    APP_SECRET: la-app-secret-de-la-aplicacion-sin-comillas
    OAUTH_TOKEN:  el-oauth-token-de-la-aplicacion-sin-comillas
    OAUTH_TOKEN_SECRET:  el-oauth-token-secret-de-la-aplicacion-sin-comillas

    [datosCuentaTwitter]
    usuario: el-usuario-twitter-sin-comillas
    contraseña: la-contraseña-twitter-sin-comillas


Módulo Dialogo
--------------
Todo parece bastante similar  a lo conseguido con Jasper, pero Selene va mucho mas allá al incluir no solo los servicios stt y tts de Bluemix 
sino que alcanza unas potencialidades inusitadas al sumarle los módulos de Dialogo y de análisis de la personalidad de Watson.

Con el módulo Dialogo puedes simular una conversación dirigida a objetivos pero 
con ciertos parámetros aleatorios que dan mucho juego a la hora de intentar mantener 
la ilusión de personalidad del agente delante de un usuario humano.

Básicamente este módulo funciona alrededor de un archivo xml que guarda en él la estructura 
arbolescente de la conversación. Esta construcción acepta desviaciones condicionales 
en las conversaciones, gotos, sinónimos , conceptos y hasta cierta aleatoriedad 
para las expresiones de salida.

La documentación y los ejemplos de este módulo , 
como de los otros que hemos utilizado, son bastante claros, y el acceso a la API del módulo 
a través de Python es francamente fácil  con el SDK liberado por la propia IBM. 
Para otros lenguajes también hay disponibles SDK similares.


Módulo Personalidad (Básico)
-----------------------------
El otro gran módulo del proyecto es el de Personality de Watson del que podemos ver aquí 
una demostración de su potencia .

En este proyecto en particular, al ser una prueba de concepto, en una primera aproximación
nos  restringimos a una parte ínfima del análisis psicológico que nos ofrece Watson . 
En concreto se ha centrado en el binomio egoísmo versus altruismo. 
Así , cada vez que Watson analiza el diario, enunciado por el usuario y guardado por Selene
en un archivo txt, se  fija solo en esos dos valores y se comparan:
 
**Si el texto del diario tiende mas hacia el egoísmo, Selene toma aleatoriamente 
una cita/refrán altruista y se lo narra al usuario, y si es al revés y el diario tiende 
al altruismo Selene le dirá una cita egoísta al usuario, 
siempre buscando que  equilibro emocional del usuario** no se desvíe hacia uno u  otro concepto 
y se mantenga centrado.


Módulo Personalidad (Intermedio)
--------------------------------
A raiz de la actualización que permite a Selene la lectura de libros al usuario se ha hecho un 
uso mas extenso del módulo Personalidad de Watson.

La idea es que en la carpeta Literatura se guarden una colección de Betsellers de la literatura
universal. Y que **Selene, nos pueda leer un capítulo de alguno de estos libros **, eligiendolo
inicialmente de manera aleatoria, y una vez leido nos pida nuestra opinión sobre el mismo, y si esta
es positiva haga el análisis de personalidad del texto pasando los parametros que entrege dicho
análisis a un casificador Bayesiano , que **nos buscará para próximas lecturas libros que coincidan
con nuestros gustos.**


Módulo Meteorológico
--------------------
Otro módulo Bluemix utilizado ha sido el meteorológico para el uso del cual hemos echado mano 
del módulo requests de Python para acceder a la API directamente.


Conclusión
----------
Como conclusión de este proyecto decir que **la experiencia ha sido muy positiva , 
siendo sorprendentemente fácil aprender y trabajar con los módulos de Watson , 
así como adaptarlos a un entorno doméstico , alejado del comercial para el 
que inicialmente están enfocados**,

también ha facilitado mucho las cosas el trabajo previo hecho con Jasper, 
sobre todo a la hora de configurar la Raspberry y 
de implementar los módulos de voz a texto (stt) y de texto a voz (tts) .


Posibles aplicaciones
---------------------
La combinación entre las tremendas capacidades cognitivas de la Nube de IBM y el pequeño
tamaño y versatilidad de la Raspberry Pi hacen casi infinito el posible campo de aplicación
de proyectos como Selene, no ya en el ámbito de la domótica tal y como se ha dicho en la 
introducción, sino que también **tendria gran aplicación  en el mundo de las personas con 
diversidad funcional como asistente para personas de la tercera edad, invidentes , etc ...**


Posibles Mejoras
----------------
Al ser una prueba de concepto, prácticamente esta todo por hacer,  profundizar en
el tema del Dialogo , mejorar el lector de libros etc....


To-Do
-----
Implementación del clasificador Bayesiano aplicando lo aprendido en el proyecto del 
[mapa de opinión](http://www.guadatech.com/mapa-de-opinion-en-twitter-con-python-y-minecraft/)


Licencia
--------

Diego J. Martinez García 
correo: apussapus@gmail.com 
web : [guadatech](http://www.guadatech.com)

<a rel="license" href="http://creativecommons.org/licenses/by/3.0/deed.es_ES"><img alt="Licencia de Creative Commons" style="border-width:0" src="http://i.creativecommons.org/l/by/3.0/88x31.png" /></a><br />
Este obra está bajo una <a rel="license" href="http://creativecommons.org/licenses/by/3.0/deed.es_ES">licencia de Creative Commons Reconocimiento 3.0 Unported</a>.


