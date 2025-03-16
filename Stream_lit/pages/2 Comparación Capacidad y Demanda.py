import streamlit as st
import pandas as pd
import io
import numpy as np
from scipy import signal

# Input fields for Factor de Participación Modal and Masa Efectiva
factor_participacion_modal = st.number_input('Factor de Participación Modal', min_value=0.0, step=0.1)
masa_efectiva = st.number_input('Masa Efectiva', min_value=0.0, step=0.1)

# File upload fields for capacity curve and accelerometric data
curva_capacidad_file = st.file_uploader('Subir archivo de Curva de Capacidad (txt)', type='txt')
acelerometricos_file = st.file_uploader('Subir datos acelerométricos de un sismo cm/s2', type=['txt', 'csv'])

# Función para obtener S_a (usando aproximaciones simplificadas)
def compute_spectrum(acc, dt):
    # Parámetros del espectro
    T = np.linspace(0.05, 5, 100)  # Períodos entre 0.05s y 5s
    xi = 0.05  # Amortiguamiento 5%
    
    omega = 2 * np.pi / T
    S_a = np.zeros_like(T)
    for i, w in enumerate(omega):
        wn = w / np.sqrt(1 - xi**2)  # Frecuencia natural ajustada
        response = signal.lsim((wn**2, 2*xi*wn, 1), acc, np.arange(0, len(acc)*dt, dt))[1]
        S_a[i] = max(abs(response))
    return S_a

if curva_capacidad_file is not None:
    curva_capacidad_data = curva_capacidad_file.read().decode('utf-8')
    st.text_area('Datos de Curva de Capacidad', curva_capacidad_data)
    
    # Extract the height (hw) from the file
    hw_line = next(line for line in curva_capacidad_data.splitlines() if line.startswith('hw'))
    hw = float(hw_line.split(':')[1].strip())
    
    # Read the capacity curve data starting from line 18
    curva_capacidad_df = pd.read_csv(io.StringIO(curva_capacidad_data), skiprows=17, delim_whitespace=True, header=None, names=['Deriva', 'Fuerza Cortante'])
    
    # Convert drifts to displacements
    curva_capacidad_df['Desplazamiento'] = curva_capacidad_df['Deriva'] * hw
    
    # Calculate the spectral displacement
    curva_capacidad_df['Pseudodesplazamiento espectral (Sd)'] = curva_capacidad_df['Desplazamiento'] / factor_participacion_modal
    
    # Calculate the spectral acceleration using the "Fuerza Cortante" column
    curva_capacidad_df['Pseudoaceleración espectral (Sa)'] = curva_capacidad_df['Fuerza Cortante'] / masa_efectiva
    
    st.write('Espectro de Capacidad Calculado:')
    st.dataframe(curva_capacidad_df)
    
    # Plotting the spectral displacement (Sd) vs spectral acceleration (Sa) using Streamlit
    st.line_chart(curva_capacidad_df.set_index('Pseudodesplazamiento espectral (Sd)')['Pseudoaceleración espectral (Sa)'])

if acelerometricos_file is not None:
    acelerometricos_data = acelerometricos_file.read().decode('utf-8')
    st.text_area('Datos Acelerométricos', acelerometricos_data)
    
    # Input field for the variable dt with default value 0.01
    dt = st.number_input('Ingrese el valor de dt', min_value=0.0, step=0.001, value=0.01)
    
    # Read the accelerometric data
    acelerometricos_df = pd.read_csv(io.StringIO(acelerometricos_data), delim_whitespace=True)
    
    if acelerometricos_df.shape[1] < 2:
        st.error('El archivo de datos acelerométricos debe tener al menos dos columnas.')
    else:
        # Calculate the spectral acceleration (Sa) of the earthquake using the provided function
        acc = acelerometricos_df.iloc[:, 1].values
        Sa = compute_spectrum(acc, dt)
        
        acelerometricos_df['Pseudoaceleración espectral (Sa)'] = Sa
