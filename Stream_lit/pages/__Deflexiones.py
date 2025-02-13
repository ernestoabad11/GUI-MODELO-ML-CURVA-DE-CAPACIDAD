import pandas as pd
import plotly.express as px
import streamlit as st

def plot_deflexiones(df, muro, batea):
    # Filtrar el DataFrame según Muro y Batea
    df_filtrado = df[(df['Muro'] == muro) & (df['Batea'] == batea)]
    
    if df_filtrado.empty:
        st.write(f"No se encontraron datos para Muro: {muro}, Batea: {batea}")
        return
    
    # Convertir la columna de fechas a formato datetime
    df_filtrado['Fecha'] = pd.to_datetime(df_filtrado['Fecha'])
    
    # Crear un DataFrame para cada deflexión y concatenarlos
    df_deflexiones = pd.melt(df_filtrado, id_vars=['Fecha'], value_vars=['D1', 'D2', 'D3', 'D4', 'D5'], 
                             var_name='Deflexión', value_name='Valor')
    
    # Filtrar solo las filas con la máxima altura (valor máximo de deflexión)
    df_max_deflexiones = df_deflexiones.loc[df_deflexiones.groupby('Fecha')['Valor'].idxmax()]

    # Crear la gráfica usando Plotly
    fig = px.line(df_max_deflexiones, x='Fecha', y='Valor', color='Deflexión', 
                  title=f'Deflexiones Máximas para Muro: {muro}, Batea: {batea}')
    
    # Mostrar la gráfica en Streamlit
    st.plotly_chart(fig)

# Configurar la aplicación Streamlit
st.title("Visualización de Deflexiones")
archivo_excel = st.file_uploader("Sube tu archivo Excel", type=["xlsx"])

if archivo_excel:
    df = pd.read_excel(archivo_excel)
    st.write("DataFrame completo:")
    st.write(df)

    muros = df['Muro'].unique()
    bateas = df['Batea'].unique()
    
    for muro in muros:
        for batea in bateas:
            plot_deflexiones(df, muro, batea)
