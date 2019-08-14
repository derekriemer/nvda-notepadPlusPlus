# Notepad++ Complemento para NVDA #

Este complemento mejora la accesibilidad de notepad++. Notepad++ es un editor de texto para Windows, y tiene muchas características. Puedes obtener más información al respecto en <https://notepad-plus-plus.org/>

## Caracteristicas:

### Apoyo para marcadores

Notepad++ te permite establecer marcadores en tu texto.
Un marcador te permite volver rápidamente a una ubicación en el editor en cualquier momento.
Para establecer un marcador, desde la línea que deseas marcar, pulsa control+f2.
Luego, cuando quieras regresar a este marcador, pulsa f2 para saltar al siguiente marcador, o shift+f2 para saltar hacia atrás al anterior.
Puedes establecer tantos marcadores como desees.

### Anuncio de longitud máxima de línea

Notepad++ tiene una regla que se puede utilizar para comprobar la longitud de una línea. Sin embargo, esta característica no es ni accesible ni significativa para los usuarios ciegos, por lo que este complemento tiene un indicador audible 
de longitud de línea que emitirá un pitido cuando una línea sea más larga que el número especificado de caracteres.

Para activar esta función, primero activa Notepad++, luego ve al menú de NVDA y pulsa Notepad++
bajo el menú Opciones. Marca la casilla "Activar el indicador de longitud de línea" y cambia el número máximo de caracteres según sea necesario. Cuando la función esté activada, escucharás un pitido al desplazarte a través de líneas que sean demasiado largas o caracteres que estén más allá de la longitud máxima. Alternativamente, puedes pulsar NVDA+g para saltar al primer carácter de desbordamiento en la línea activa.

### Moverse al delimitador simétrico

En Notepad++ puedes desplazarte al delimitador simétrico de un programa puulsando control+b. 
Para moverte tienes que estar en Un carácter de la llave que deseas hacer coincidir.
Al pulsar este comando, NVDA leerá la línea en la que aterrizó y si la línea consiste sólo en una llave, leerá la línea arriba y debajo de la llave para que pueda tener una idea del contexto.

### Autocompletado

La funcionalidad de autocompletado de Notepad++ no es accesible por defecto. El autocompletado tiene muchos problemas, incluyendo que se muestra en una ventana flotante. Para hacer esta funcionalidad accesible, se hacen tres cosas. 

1. Cuando aparece una sugerencia de autocompletado, se reproduce un sonido como un deslizamiento. El sonido inverso se hace cuando desaparecen las sugerencias.
2. Al pulsar las flechas abajo/arriba lee el texto sugerido siguiente/anterior. 
3. El texto recomendado se verbaliza cuando aparecen las sugerencias.

### Búsqueda incremental

Una de las caracteristicas mas interesantes de notepad++ es la capacidad para usar la busqueda incremental. 
La búsqueda incremental es un modo de búsqueda en el que buscas una frase de prueba escribiendo en el campo de edición, y el documento se desplaza mostrandote la búsqueda en tiempo real. 
Mientras escribe, el documento se desplaza para mostrar la línea de texto con la frase más probable que estás buscando. También resalta el texto que coincida.
El programa también te muestra cuántas coincidencias se han detectado. Hay botones para desplazarse hacia la coincidencia siguiente y anterior.
Mientras escribes, NVDA anunciará la línea de texto que notepad++ detectó en un resultado de búsqueda. NVDA anuncia también cuántas coincidencias hay, pero sólo si el número de coincidencias ha cambiado. 
Cuando has encontrado la línea de texto que quieras, simplemente pulsa escape, y esa línea de texto estará en tu cursor.
Para abrir este cuadro de diálogo, selecciona Búsqueda incremental Desde el menu Buscar, o pulsa alt+control+i.

### Anunciando información acerca de la línea actual

Pulsando NVDA+shift+\ (barra inversa) en cualquier momento se anunciará lo siguiente:

* el número de línea
* el número de la columna, es decir, cuán lejos estás en la línea.
* el tamaño de la seleccion, (número de caracteres horizontalmente seleccionados, seguido por un símbolo, seguido por el número de caracteres seleccionados verticalmente, lo que haría un rectángulo.
 
### Apoyo a la funcion de busqueda anterior / siguiente

Por defecto, si pulsas control+f aparece el cuadro de diálogo Buscar. 
Si tecleas un texto aquí y pulsas Intro, el texto en la ventana se selecciona y el documento se desplaza hacia el resultado de la búsqueda siguiente.
En Notepad++ puedes pulsar f3 o shift+f3 para repetir la búsqueda en dirección hacia adelante o hacia atrás respectivamente. 
NVDA leerá tanto la línea actual, y la selección dentro de la línea que representa el texto encontrado.

### Vista previa de MarkDown o Hipertexto como página web 

Notepad++ No es compatible con MarkDown (*.md) p.ej. el resaltado del lenguaje. 
Sin embargo, puede obtener una vista previa de dicho contenido como mensaje navegable si pulsa NVDA+h (Escape para cerrar el mensaje). 
Si pulsa NVDA+shift+h, la abrirá en su navegador estándar. 
Algunas extensiones de Markdown populares como PHP Extra o TOC son compatibles. 
Funciona también con (de una sola página) Html. 

Para probarlo, copie el siguiente bloque, péguelo en un nuevo documento de Notepad ++ y presione NVDA+h:

<br>

    ---
    ## Donde empezó...  
    > Hace mucho tiempo,  
    > en un país extranjero.  
    ## Y adónde fue después  
    1. Primera etapa  
    2. Segunda etapa  
    ## Eventualmente se convirtió en  
    * no ordenado  
    * pero sigue siendo  
    * una lista  

<br>

## Atajos de teclado de Notepad++ no por defecto

Este complemento supone que Notepad++ es utilizado con las teclas de acceso directo por defecto. 
Si este no es el caso, por favor modifica las teclas de órdenes de este app module para reflejar tus órdenes de Notepad++ según necesites en el cuadro de diálogo Gestos de Entrada de NVDA.
Todas las órdenes del complemento están bajo la sección de notepad++.