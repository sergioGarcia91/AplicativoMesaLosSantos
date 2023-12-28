# -*- coding: utf-8 -*-
"""
Spyder Editor

Author: Sergio Andrés García Arias
Created on Thu Dec 28 10:16:05 2023
version: 0.1.0
"""
import pandas as pd
import joblib
import numpy as np

PuntosFallas = 'PuntosSobreFallas.csv'
df_PuntosFallas = pd.read_csv(PuntosFallas, sep=',', decimal='.')
df_PuntosFallas = df_PuntosFallas[['CoorX', 'CoorY', 'DEM_mesa_r']]
df_PuntosFallas.columns = [ 'X', 'Y', 'Z']

df_PuntosFallas.head()

csv = 'GeoSup_MesaLosSantos.csv'
df = pd.read_csv(csv, delimiter=',', decimal='.')
df_Geo = df.iloc[:, 0:5].copy()
df_Geo.columns = ['X', 'Y', 'Z', 'DF', 'Formacion']
#print(df_Geo.head())
# Calcular distancia minima a Fallas


# Cambiar Geo a numeros
df_Geo['Formacion'] = df_Geo['Formacion'].str.lower()
dict_geo = {'k1t':8,
            'k1p':7,
            'k1r':6,
            'k1ls_ms':5,
            'k1ls_mm':4,
            'k1ls_mi':3,
            'j1-2j':2,
            'j1gp':1,
            'oss':0}
df_Geo['GeoNN'] = df_Geo['Formacion'].replace(dict_geo, inplace=False)

# Normalizar datos
df_Geo['Xn'] = (df_Geo['X'] - 1096700) / (1120100 - 1096700)
df_Geo['Yn'] = (df_Geo['Y'] - 1235500) / (1260100 - 1235500)
df_Geo['Zn'] = (df_Geo['Z'] - (-150)) / (1830 - (-150))
df_Geo['DFn'] = (df_Geo['DF'] - (000)) / (3000 - (000))


df_Geo = df_Geo[['Xn', 'Yn', 'Zn', 'DFn', 'GeoNN']].to_numpy()


# Cargar modelos NN
agua = joblib.load('./modelosNN/aguaNNrelu_hl15_7_5Sc51.pkl')
densidad = joblib.load('./modelosNN/densidadNNrelu_hl35_11_5Sc45.pkl')
hf = joblib.load('./modelosNN/hfNNrelu_hl30_10_5Sc65.pkl')
is50 = joblib.load('./modelosNN/is50NNrelu_hl20_6_5Sc36.pkl')
lf = joblib.load('./modelosNN/lfNNrelu_hl10_6_5Sc61.pkl')
mDry = joblib.load('./modelosNN/mDryNNrelu_hl5_5_5Sc31.pkl')
mWet = joblib.load('./modelosNN/mWetNNrelu_hl15_5_5Sc40.pkl')
peakLoad = joblib.load('./modelosNN/peakLoadNNrelu_hl15_5_5Sc37.pkl')
porosidad = joblib.load('./modelosNN/porosidadNNrelu_hl25_8_5Sc32.pkl')
rhoDry = joblib.load('./modelosNN/rhoDryNNrelu_hl25_9_5Sc53.pkl')
rhoWet = joblib.load('./modelosNN/rhoWetNNrelu_hl10_6_5Sc33.pkl')
vp = joblib.load('./modelosNN/vpNNrelu_hl15_13_5Sc41.pkl')


# Prefecir
df['Agua [%]'] = np.round(agua.predict(df_Geo), 2)
df['Porosidad [%]'] = np.round(porosidad.predict(df_Geo), 2)
df['Densidad [gr/cm3]'] = np.round(densidad.predict(df_Geo), 2)
df['Rho Dry [Ohm*m]'] = np.round(10 ** rhoDry.predict(df_Geo), 2)
df['Rho Wet [Ohm*m]'] = np.round(10 ** rhoWet.predict(df_Geo), 2)
df['M Dry [mV/V]'] = np.round(mDry.predict(df_Geo), 2)
df['M Wet [mV/V]'] = np.round(mWet.predict(df_Geo), 2)
df['Vp [m/s]'] = np.round(10 ** vp.predict(df_Geo), 2)
df['Peak Load [kN]'] = np.round(peakLoad.predict(df_Geo), 2)
df['Is50 [MPa]'] = np.round(is50.predict(df_Geo),2)
df['HF [SI]'] = np.round(10 ** hf.predict(df_Geo), 7)
df['LF [SI]'] = np.round(10 ** lf.predict(df_Geo), 7)

#print(df.iloc[:, 0:5].head())
del df_Geo
# Guardar
#df.to_csv('Predichos.csv', index=False)

















