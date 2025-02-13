import pandas as pd
import plotly.express as px
import streamlit as st

def plot_deflexiones(df, muro):
    # Filtrar el DataFrame según Muro
    df_filtrado = df[df['Muro'] == muro]
    
    if df_filtrado.empty:
        st.write(f"No se encontraron datos para Muro: {muro}")
        return
    
    # Ordenar el DataFrame por Batea y Fecha
    df_filtrado = df_filtrado.sort_values(by=['Batea', 'Fecha'])
    
    # Convertir la columna de fechas a formato datetime
    df_filtrado['Fecha'] = pd.to_datetime(df_filtrado['Fecha'])
    
    # Crear un DataFrame para cada deflexión y concatenarlos
    df_deflexiones = pd.melt(df_filtrado, id_vars=['Fecha', 'Batea'], value_vars=['D1', 'D2', 'D3', 'D4', 'D5'], 
                             var_name='Deflexión', value_name='Valor')

    # Crear la gráfica usando Plotly
    fig = px.line(df_deflexiones, x='Fecha', y='Valor', color='Deflexión', line_group='Batea',
                  title=f"Deflexiones para Muro: {muro}")
    fig.update_layout(xaxis_title='Fecha', yaxis_title='Valor de Deflexión')
    st.plotly_chart(fig)

# Configurar la aplicación Streamlit
st.title("Visualización de Deflexiones")
archivo_excel = st.file_uploader("Sube tu archivo Excel", type=["xlsx"])

if archivo_excel:
    df = pd.read_excel(archivo_excel)
    st.write("DataFrame completo:")
    st.write(df)

    muros = df['Muro'].unique()
    
    for muro in muros:
        plot_deflexiones(df, muro)
