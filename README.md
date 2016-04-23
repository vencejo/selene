# selene
Asistente nocturno con Raspberry Pi capaz de mantener diálogos gracias al servicio Watson de IBM Bluemix

Info completa en [la web de guadatech](http://www.guadatech.com/proyecto-selene)

[video demostrativo](https://www.youtube.com/watch?v=uigE7JxHXR4)

Este proyecto surge como una continuación lógica de nuestro anterior trabajo con Jasper, 
en el que vimos como la inclusión de servicios en la nube de IBM simplificaban en gran medida 
el código y la mantenibilidad del asistente vocal.

Con Selene hemos avanzado en este sentido, haciendo  un uso intensivo de la nube de IBM Bluemix.

En concreto, se trata de  la realización de una prueba de concepto de un “asistente personal nocturno” 
consistente en una Raspberry Pi con Micrófono y Altavoces en la parte hardware colocado todo esto 
de manera discreta en la mesita de noche junto a la cama del usuario.

La idea es que antes de dormirte puedas hablar con Selene y pedirle que te lea las noticias, 
te ponga la radio, 
te diga el tiempo que va a hacer mañana, y escuche y guarde tu relato del día y lo guarde en tu pequeño diario digitalizado.

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

El otro gran módulo del proyecto es el de Personality de Watson del que podemos ver aquí 
una demostración de su potencia .

En este proyecto en particular, al ser una prueba de concepto, 
nos hemos restringido a una parte ínfima del análisis psicológico que nos ofrece Watson . 
En concreto se ha centrado en el binomio egoísmo versus altruismo. 
Así , cada vez que Watson analiza el diario, enunciado por el usuario y guardado por Selene
en un archivo txt, se  fija solo en esos dos valores y se comparan:
 
Si el texto del diario tiende mas hacia el egoísmo, Selene toma aleatoriamente 
una cita/refrán altruista y se lo narra al usuario, y si es al revés y el diario tiende 
al altruismo Selene le dirá una cita egoísta al usuario, 
siempre buscando que  equilibro emocional del usuario no se desvíe hacia uno u  otro concepto 
y se mantenga centrado.

Otro módulo Bluemix utilizado ha sido el meteorológico para el uso del cual hemos echado mano 
del módulo requests de Python para acceder a la API directamente.

Como conclusión de este proyecto decir que la experiencia ha sido muy positiva , 
ha sido sorprendentemente fácil aprender y trabajar con los módulos de Watson , 
así como adaptarlos a un entorno doméstico , alejado del comercial para el 
que inicialmente están enfocados,

también ha facilitado mucho las cosas el trabajo previo hecho con Jasper, 
sobre todo a la hora de configurar la Raspberry y 
de implementar los módulos de voz a texto (stt) y de texto a voz (tts) .

