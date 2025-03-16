import streamlit as st

def main():      
    st.set_page_config(
        layout="wide",
        page_title="Modelo Curva de Capacidad",
        page_icon="✍️",
    )
    st.title("Modelo de Curva de Capacidad")
    
    # Descripción del aplicativo web
    st.write("""
    ## Descripción del Aplicativo Web
    Este aplicativo web permite generar la curva de capacidad de muros de concreto reforzado utilizando un modelo de aprendizaje automático.
    A continuación se describen los parámetros de entrada necesarios:
    
    - **tw (Espesor del muro)**: Espesor del muro en metros.
    - **hw (Altura del muro)**: Altura del muro en metros.
    - **lw (Longitud del muro)**: Longitud del muro en metros.
    - **lbe (Longitud del elemento de borde)**: Longitud del elemento de borde en metros.
    - **P (Carga axial)**: Carga axial en kN.
    - **fc (Resistencia a la compresión del concreto)**: Resistencia a la compresión del concreto en MPa.
    - **fyh (Resistencia a la fluencia de la armadura horizontal)**: Resistencia a la fluencia de la armadura horizontal en MPa.
    - **fyv (Resistencia a la fluencia de la armadura vertical)**: Resistencia a la fluencia de la armadura vertical en MPa.
    - **fbe (Resistencia a la fluencia de la armadura del elemento de borde)**: Resistencia a la fluencia de la armadura del elemento de borde en MPa.
    - **ρh (Relación de refuerzo horizontal)**: Relación de refuerzo horizontal.
    - **ρvbe (Relación de refuerzo vertical del elemento de borde)**: Relación de refuerzo vertical del elemento de borde.
    - **ρhbe (Relación de refuerzo horizontal del elemento de borde)**: Relación de refuerzo horizontal del elemento de borde.
    - **Tag_web_reinf (Tipo de refuerzo)**: Tipo de refuerzo (0 para WWM, 1 para DB).
    
    El aplicativo permite ajustar estos parámetros mediante controles deslizantes y botones de opción en la barra lateral.
    Una vez definidos los parámetros, se genera la curva de capacidad que muestra la relación entre las derivas de entrepisos en % y la fuerza cortante en kN.
    Además, se puede descargar un archivo TXT con los resultados obtenidos.
    """)
    
    # Espacio reservado para una imagen gráfica
    st.image("Stream_lit\Imagenes\Muro_1.png", caption="Descripción gráfica del modelo", width=400)

if __name__ == "__main__":
    main()