Selene
======

Asistente nocturno con Raspberry Pi capaz de mantener diálogos gracias al servicio Watson de IBM Bluemix

Info completa en [la web de guadatech](http://www.guadatech.com/proyecto-selene)

[video demostrativo](https://www.youtube.com/watch?v=uigE7JxHXR4)

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
introducción, sino que también tendria gran aplicación  en el mundo de las personas con 
diversidad funcional como asistente para personas de la tercera edad, invidentes , etc ...


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

Diego J. Martinez García - apussapus@gmail.com - [guadatech](http://www.guadatech.com)

<a rel="license" href="http://creativecommons.org/licenses/by/3.0/deed.es_ES"><img alt="Licencia de Creative Commons" style="border-width:0" src="http://i.creativecommons.org/l/by/3.0/88x31.png" /></a><br />
Este obra está bajo una <a rel="license" href="http://creativecommons.org/licenses/by/3.0/deed.es_ES">licencia de Creative Commons Reconocimiento 3.0 Unported</a>.


