Este aplicativo utiliza modelos de redes neuronales generados en mi trabajo de maestría disponible en la [Biblioteca](https://noesis.uis.edu.co/handle/20.500.14071/11267) de la Universidad Industrial de Santander. Estos modelos están diseñados para predecir propiedades físicas de la roca como agua, porosidad, resistividad, cargabilidad, entre otras, específicamente para las Formaciones aflorantes en la Mesa de Los Santos.

![Captura de Pantalla](https://github.com/sergioGarcia91/AplicativoMesaLosSantos/blob/main/App.png?raw=true)

Para utilizar el aplicativo, es necesario cargar un archivo CSV siguiendo las siguientes consideraciones:
1. El archivo CSV debe estar delimitado por comas (,) y utilizar el punto (.) como separador decimal.
2. El sistema de coordenadas debe estar en EPSG:3116.
3. El orden de las columnas debe ser: Coordenadas en X, Coordenadas en Y, Altura en metros, Distancia a la falla más cercana en metros y unidades geológicas.
4. Las unidades geológicas permitidas son: K1t, K1p, K1r, K1ls_ms, K1ls_mm, K1ls_mi, J1-2j, J1gp, Oss.
5. Las formaciones geológicas y las fallas corresponden al trabajo realizado por el INGEOMINAS-UIS (2007).

# Requerimientos
El aplicativo fue desarrollado en `Python==3.11.5`. Se recomienda generar un entorno virtual e instalar las siguientes librerías:

```
altgraph==0.17.4
joblib==1.3.2
numpy==1.26.2
packaging==23.2
pandas==2.1.4
pefile==2023.2.7
pyinstaller==6.3.0
pyinstaller-hooks-contrib==2023.11
python-dateutil==2.8.2
pytz==2023.3.post1
pywin32-ctypes==0.2.2
scikit-learn==1.3.2
scipy==1.11.4
six==1.16.0
threadpoolctl==3.2.0
tk==0.1.0
tzdata==2023.3
```

# Ejecución
Después de instalar las librerías y descargar los archivos del repositorio, dirigirse a la carpeta donde se encuentran descargados y ejecuta en la ventana de comandos:

```bash
pyinstaller --icon=MesaIcon.ico --hidden-import Scikit-learn --hidden-import sklearn --hidden-import joblib --hidden-import scipy --hidden-import tk --hidden-import PyInstaller --hidden-import sklearn.neural_network myAppNN.py
```

Esto generará varias carpetas, siendo `\dist\myAppNN\` la de interés. Colocar el archivo `MesaIcon.ico` y la carpeta `modelosNN` en esa ubicación. Utiliza el archivo `GeoSup_MesaLosSantos.csv` para probar la ejecución. El archivo generado queda en la misma ubicacion del CSV cargado.

> **Observación:** El `.exe` puede tardar un poco en ejecutarse, al igual que hacer la predicción de los valores. Actualmente, la ventana de comandos está presente para visualizar posibles errores. El único posible error es debido a las versiones de los modelos, que no afecta la predicción de los valores. Se espera corregir esto en el futuro.

# Archivo RAR
Si lo prefiere, puede descargar el archivo [`.rar`](https://drive.google.com/file/d/1xZogJy02ZHeW5V9IlxzYp-76dr7JJMUb/view?usp=sharing), que ya contiene el aplicativo. Solo requiere descomprimir y ejecutar el `.exe`.

# Contribuciones
¡Se agradecen las contribuciones y sugerencias! Si encuentras errores o tienes ideas para mejorar la aplicación, no dudes en informarlo. Tu colaboración es bienvenida.

Se esperan mejoras en un futuro no muy lejano.
