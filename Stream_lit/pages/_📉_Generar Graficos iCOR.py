import pandas as pd
import plotly.express as px
import streamlit as st

def plot_deflexiones(df, batea, muro, altura):
    # Filtrar el DataFrame según Batea, Muro y Altura
    filtro = (df['Batea'] == batea) & (df['Muro'] == muro) & (df['Altura'] == altura)
    df_filtrado = df[filtro]
    
    if df_filtrado.empty:
        st.write(f"No se encontraron datos para Batea: {batea}, Muro: {muro}, Altura: {altura}")
        return
    
    # Convertir la columna de fechas a formato datetime
    df_filtrado['Fecha'] = pd.to_datetime(df_filtrado['Fecha'])
    
    # Crear un DataFrame para cada deflexión y concatenarlos
    df_deflexiones = pd.melt(df_filtrado, id_vars=['Fecha'], value_vars=['D1', 'D2', 'D3', 'D4', 'D5'], 
                             var_name='Deflexión', value_name='Valor')

    # Crear la gráfica usando Plotly
    fig = px.line(df_deflexiones, x='Fecha', y='Valor', color='Deflexión',
                  title=f"Deflexiones para Batea: {batea}, Muro: {muro}, Altura: {altura}")
    fig.update_layout(xaxis_title='Fecha', yaxis_title='Valor de Deflexión')
    st.plotly_chart(fig)

# Configurar la aplicación Streamlit
st.title("Visualización de Deflexiones")
archivo_excel = st.file_uploader("Sube tu archivo Excel", type=["xlsx"])

if archivo_excel:
    df = pd.read_excel(archivo_excel)
    st.write("DataFrame completo:")
    st.write(df)

    batea = st.number_input("Batea", min_value=1)
    muro = st.text_input("Muro")
    altura = st.number_input("Altura")

    if st.button("Generar Gráfico"):
        plot_deflexiones(df, batea, muro, altura)
