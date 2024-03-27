import streamlit as st
import zipfile
import pandas as pd
from openai import OpenAI

# Crea una instancia del cliente OpenAI y realiza solicitud a la API (Añadir API_KEY propia)
def get_response_chatgpt(prompt):
    client = OpenAI(api_key="API_KEY")

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    return ((response.choices[0].message.content))

# Extraer y leer el archivo CSV
ruta_zip = 'Datos\Prosa_IA.csv.zip'
with zipfile.ZipFile(ruta_zip, "r") as archivo_zip:
    archivo_csv = archivo_zip.extract("Prosa_IA.csv", path="Datos")
df = pd.read_csv(archivo_csv)

# Crear el prompt con los datos del CSV
prompt = ''

for i in df.iloc[:,1].values:
    prompt = prompt + '"' + i + '"' + '\n'

prompt = prompt + '''
En base a cada una de esas opiniones definidas entre las comillas quiero que me realices un texto en prosa 
compuesto por 2 parrafos de 6 lineas que las tenga en cuenta. 
Evita enfatizar tanto y se mas politicamente correcto pero representando bien las opiniones.'''

# Confifurar app web con streamlit
st.set_page_config(
    page_title="Coloquio",
    layout="wide",
    initial_sidebar_state="expanded")

# Configurar el contenido del sidebar
with st.sidebar:
    st.image("Imagenes\cli-logo.jpg", use_column_width=True)
    c1, c2, c3, c4 = st.columns((1,1,1,1))
    c2.image("Imagenes\Ayto_Bilbao.png", width=200)
    st.markdown("""
    <style>
        .sidebar-text {
            color: #BA0000;
        }
    </style>
    """, unsafe_allow_html=True)
    for i in df.iloc[:,1].values:
        linea = '"' + i + '"' + '\n'
        st.write(f"<h4 class='sidebar-text'>📩 {linea}</h4>", unsafe_allow_html=True)

st.markdown("""
    <style>
        .title {
            text-align: center;
            color: #BA0000;
        }
        .prosa {
            text-align: center;
            color: #BA0000;
            font-size: 1.17em;
            font-weight: bold;
            margin-bottom: 1em;
        }
    </style>
""", unsafe_allow_html=True)
st.markdown('<h1 class="title">🌎 Coloquio: Racismo en las aulas 🌍</h1>', unsafe_allow_html=True)

# Crear botón para generar el texto
if st.button("Generar reflexión conjunta", type='primary', use_container_width=20):
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    prosa = (get_response_chatgpt(prompt)).split('\n\n')
    st.markdown(f"<div class='prosa'>{prosa[0]}</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='prosa'>{prosa[1]}</div>", unsafe_allow_html=True)