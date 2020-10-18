# landmarksmanosradiografias
Programa para marcar manualmente 2 landmarks y localizarlas automáticamente en imágenes radiográficas de manos humanas

Se explicará primero como marcar las landmarks manuales y después la localización automática. Nota: se pueden localizar las landmarks automáticamente sin necesidad de
ubicarlas manualmente.

Para marcar manualmente dos landmarks se debe ingresar en la carpeta "etiquetador_manual" y ejecutar el archivo "Landmarks_manual_main.py" el cual abre un explorador de archivos
donde se debe seleccionar una carpeta con las imágenes radiográficas en formato .jpg o .png. A continuación se despliega una nueva ventana que muestra las imagenes seleccionadas 
pero corregidas en contraste, escala y traslación. Para ubicar primero la landmark en la parte superior del tercer hueso metacarpiano y después en la parte inferior
del hueso mencionado. Una vez que se finalizó la localización manual se cierra la venta y en la carpeta raiz se crea un archivo llamado "Manual_landmarks.csv" que contiene
las coordenadas de las dos landmarks en cada imagen. Tambien se crea uan carpeta llamada "Corregidas" que contiene las imagenes que se seleccionaron pero corregidas en contraste, 
escala y traslación.

Para la localización automática se debe ejecutar el archivo "landmarks_MAIN.py" para iniciar el programa. El cual abre un explorador de archivos para seleccioanr una 
carpeta que contenga imagenes radiográficas de manos en formato .jpg o .png. Para continuar con la búsqueda de las landamrks. Una vez finalizada la búsqueda en la carpeta raiz
de las imagenes a evaluar se crea una carpeta llamada "Aligned_Images" que contiene las imágenes radiograficas corregidas en contraste, escala y traslación. También se crea un 
archivo llamado "Landmarks.csv" que tiene las coordenadas de las dos landmarks (superior e inferior) con su correspondiente nombre de la imagen a la cual pertencen. Finalmente se 
crea otra carpeta llamada "Estimated_landmarks_images" que contiene el nombre de las imágenes que también estan corregidas en contraste, escala y traslación con las landmarks 
ubicadas en el tercer hueso metacarpiano, donde la landmark superior se muestra de color azul y la landmark inferior en color rojo.

Como se mencionó se pueden localizar landmarks automáticamente ya que en la carpeta "espacios" se encuentra la información que se ocupó como entrenamiento del algoritmo. Así si
se marcan manaulmente landmarks y se copia el archivo llamado "Manual_landmarks.csv" en donde estan ubicadas las imagenes para ubicar automáticamente landmarks, además de crear 
los archivos mencionados se crea un archivo llamado "información.log" que contiene información sobre el número de imágenes evaluadas, su tamaño y los errores rmse y mae
respecto a las landmarks manuales y localizadas automáticamente.

Se adjunta el archivo "APORTES_Y_APLICACIONES_EN_LAS_CIENCIAS_CMPUTACIONALES.pdf" relacionado al proyecto desarrollado
