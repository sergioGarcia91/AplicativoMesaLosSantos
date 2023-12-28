# -*- coding: utf-8 -*-
"""
Spyder Editor

Author: Sergio Andrés García Arias
Created on Thu Dec 28 10:16:05 2023
version: 0.1.0
"""

import tkinter as tk
from tkinter import filedialog
import pandas as pd
import joblib
import numpy as np
import webbrowser


class CSVConverterApp:
    def __init__(self, root):
        colorFondo = '#171718'
        colorEstado = '#6a6e73'
        colorBotones = '#1f2124'
        colorObservaciones = '#393d42'
        colorGarcia = colorBotones
        colorTexto = "white"
        tipoLetra = 'Times News Roman'
        
        self.root = root
        self.root.geometry("1000x500") # Cambiar dimenciones
        self.root.title("Propiedades Físicas de la Roca: Mesa de Los Santos")
        self.root.configure(bg=colorFondo)
        self.root.iconbitmap("MesaIcon.ico")

        # Etiqueta para mostrar el estado
        self.status_label = tk.Label(root, text="Esperando acción...",
                                     font=(tipoLetra, 12, 'italic'),
                                     fg=colorTexto,
                                     bg=colorEstado)
        self.status_label.pack(pady=10)

        # Botón para cargar un archivo CSV
        self.load_button = tk.Button(root, text="Cargar CSV", command=self.load_csv,
                                     font=(tipoLetra, 13, 'bold'),
                                     fg=colorTexto,
                                     bg=colorBotones)
        self.load_button.pack(pady=10)

        # Botón para convertir los datos
        self.convert_button = tk.Button(root, text="Predecir propiedades", command=self.convert_data, state=tk.DISABLED,
                                        font=(tipoLetra, 12, 'bold'),
                                        fg=colorTexto,
                                        bg=colorBotones)
        self.convert_button.pack(pady=10)
        
        texto_observaciones = '''
        Este aplicativo compila los modelos de redes neuronales generados en el trabajo de maestría de Garcia-Arias (2022). Estos modelos predicen los valores de porosidad, velocidad de onda P, resistividad eléctrica, entre otras propiedades físicas de la roca para las Formaciones aflorantes en la Mesa de los Santos.

        Se requiere cargar un archivo CSV con las siguientes consideraciones:
        1. El archivo .csv esté delimitado por comas (,) y el decimal sea el punto (.).
        2. El sistema de coordenadas debes estar en EPSG:3116.
        3. El orden de las columnas debe ser: Coordenadas en X, Coordenadas en Y, Altura en metros, distancia a la falla mas cercana en metros y unidades geológicas.
        4. Las unidades geológicas permitidas son: K1t, K1p, K1r, K1ls_ms, K1ls_mm, K1ls_mi, J1-2j, J1gp, Oss.
        5. Las formaciones geológicas y las fallas corresponden al trabajo realizado por el INGEOMINAS-UIS (2007).
        '''

        self.observaciones = tk.Label(root, text=texto_observaciones, justify="left", wraplength=600,
                                      font=(tipoLetra, 11),
                                      fg=colorTexto,
                                      bg=colorObservaciones)
        self.observaciones.pack(padx=20, pady=10)

        def callback(url):
            webbrowser.open_new(url)
        
        link1 = tk.Label(root, text="Garcia-Arias (2022)", fg="cyan", cursor="hand2",
                         font=(tipoLetra, 11, 'italic'),
                         bg=colorGarcia)
        link1.pack()
        link1.bind("<Button-1>", lambda e: callback("https://noesis.uis.edu.co/handle/20.500.14071/11267"))


    def load_csv(self):
        self.file_path = filedialog.askopenfilename(filetypes=[("Archivos CSV", "*.csv")])
        if self.file_path:
            self.status_label.config(text=f"Archivo cargado: {self.file_path}")
            self.convert_button.config(state=tk.NORMAL)

            # Guardar el DataFrame cargado para su posterior uso
            self.df = pd.read_csv(self.file_path)
            self.df_Geo = self.df.iloc[:, 0:5].copy()
            self.df_Geo.columns = ['X', 'Y', 'Z', 'DF', 'Formacion']
    
    def cambiarGeo(self):
        # Cambiar la geologia a numeros
        self.df_Geo['Formacion'] = self.df_Geo['Formacion'].str.lower()
        self.dict_geo = {'k1t':8,
                         'k1p':7,
                         'k1r':6,
                         'k1ls_ms':5,
                         'k1ls_mm':4,
                         'k1ls_mi':3,
                         'j1-2j':2,
                         'j1gp':1,
                         'oss':0}
        self.df_Geo['GeoNN'] = self.df_Geo['Formacion'].replace(self.dict_geo, inplace=False)
        
    def normalizarDatos(self):
        # Normalizar los datos para la prediccion y pasar a Numpy
        self.df_Geo['Xn'] = (self.df_Geo['X'] - 1096700) / (1120100 - 1096700)
        self.df_Geo['Yn'] = (self.df_Geo['Y'] - 1235500) / (1260100 - 1235500)
        self.df_Geo['Zn'] = (self.df_Geo['Z'] - (-150)) / (1830 - (-150))
        self.df_Geo['DFn'] = (self.df_Geo['DF'] - (000)) / (3000 - (000))
        self.df_Geo = self.df_Geo[['Xn', 'Yn', 'Zn', 'DFn', 'GeoNN']].to_numpy()
        
    def load_NN(self):
        # Se cargan todos los modelos de Red Neuronal
        self.agua = joblib.load('./modelosNN/aguaNNrelu_hl15_7_5Sc51.pkl')
        self.densidad = joblib.load('./modelosNN/densidadNNrelu_hl35_11_5Sc45.pkl')
        self.hf = joblib.load('./modelosNN/hfNNrelu_hl30_10_5Sc65.pkl')
        self.is50 = joblib.load('./modelosNN/is50NNrelu_hl20_6_5Sc36.pkl')
        self.lf = joblib.load('./modelosNN/lfNNrelu_hl10_6_5Sc61.pkl')
        self.mDry = joblib.load('./modelosNN/mDryNNrelu_hl5_5_5Sc31.pkl')
        self.mWet = joblib.load('./modelosNN/mWetNNrelu_hl15_5_5Sc40.pkl')
        self.peakLoad = joblib.load('./modelosNN/peakLoadNNrelu_hl15_5_5Sc37.pkl')
        self.porosidad = joblib.load('./modelosNN/porosidadNNrelu_hl25_8_5Sc32.pkl')
        self.rhoDry = joblib.load('./modelosNN/rhoDryNNrelu_hl25_9_5Sc53.pkl')
        self.rhoWet = joblib.load('./modelosNN/rhoWetNNrelu_hl10_6_5Sc33.pkl')
        self.vp = joblib.load('./modelosNN/vpNNrelu_hl15_13_5Sc41.pkl')
        
    def predecir(self):
        # Se predicen los valores con los modelos de Red Neuronal
        self.df['Agua [%]'] = np.round(self.agua.predict(self.df_Geo), 2)
        self.df['Porosidad [%]'] = np.round(self.porosidad.predict(self.df_Geo), 2)
        self.df['Densidad [gr/cm3]'] = np.round(self.densidad.predict(self.df_Geo), 2)
        self.df['Rho Dry [Ohm*m]'] = np.round(10 ** self.rhoDry.predict(self.df_Geo), 2)
        self.df['Rho Wet [Ohm*m]'] = np.round(10 ** self.rhoWet.predict(self.df_Geo), 2)
        self.df['M Dry [mV/V]'] = np.round(self.mDry.predict(self.df_Geo), 2)
        self.df['M Wet [mV/V]'] = np.round(self.mWet.predict(self.df_Geo), 2)
        self.df['Vp [m/s]'] = np.round(10 ** self.vp.predict(self.df_Geo), 2)
        self.df['Peak Load [kN]'] = np.round(self.peakLoad.predict(self.df_Geo), 2)
        self.df['Is50 [MPa]'] = np.round(self.is50.predict(self.df_Geo),2)
        self.df['HF [SI]'] = np.round(10 ** self.hf.predict(self.df_Geo), 7)
        self.df['LF [SI]'] = np.round(10 ** self.lf.predict(self.df_Geo), 7)
        
           
    def convert_data(self):
        # Realizar aquí la lógica de conversión de datos
        # En este ejemplo, simplemente imprimiremos las primeras filas del DataFrame
        #if hasattr(self, 'df'):
            #print("Datos convertidos:")
            #print(self.df.head())
            #self.status_label.config(text="Datos convertidos. Consulta la consola.")
        #else:
            #self.status_label.config(text="Error: No se ha cargado ningún archivo CSV.")
        self.cambiarGeo()
        self.normalizarDatos()
        self.load_NN()
        self.predecir()
        del self.df_Geo
        self.df.to_csv(f'{self.file_path[:-4]}_pred.csv', index=False)
        self.convert_button.config(state=tk.DISABLED)
        self.status_label.config(text="Listo! ... Esperando acción...")

if __name__ == "__main__":
    root = tk.Tk()
    app = CSVConverterApp(root)
    root.mainloop()
