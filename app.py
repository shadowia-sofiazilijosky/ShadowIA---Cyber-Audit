import streamlit as st
import requests
from fpdf import FPDF

# 1. CONFIGURACIÓN DE MARCA (Cian Neón)
CIAN_NEON = "#00FFFF"
FONDO_OSCURO = "#0E1117"

st.set_page_config(page_title="ShadowIA - Cyber Audit", page_icon="🛡️", layout="wide")

# Estilo CSS para la estética Hacker Cian
st.markdown(f"""
    <style>
    .main {{ background-color: {FONDO_OSCURO}; color: white; }}
    .stTextArea textarea {{ background-color: #1A1C23; color: {CIAN_NEON}; border: 1px solid {CIAN_NEON}; }}
    .stButton>button {{ 
        background-color: {CIAN_NEON}; 
        color: black; 
        font-weight: bold; 
        border-radius: 8px;
        width: 100%;
        border: none;
    }}
    h1, h2, h3 {{ color: {CIAN_NEON} !important; }}
    .stFileUploader {{ border: 1px dashed {CIAN_NEON}; border-radius: 10px; padding: 10px; }}
    .stInfo {{ background-color: #1A1C23; color: white; border: 1px solid {CIAN_NEON}; }}
    </style>
    """, unsafe_allow_html=True)

# 2. FUNCIÓN PARA GENERAR EL REPORTE PDF
def generar_pdf(resultado):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(200, 10, txt="INFORME DE AUDITORIA - SHADOWIA", ln=True, align='C')
    pdf.ln(10)
    pdf.set_font("Arial", size=12)
    # Limpiamos el texto para que el PDF no de error con símbolos raros
    texto_limpio = resultado.encode('latin-1', 'ignore').decode('latin-1')
    pdf.multi_cell(0, 10, txt=texto_limpio)
    return pdf.output(dest='S').encode('latin-1')

# 3. ENCABEZADO CON TU LOGO
col1, col2 = st.columns([1, 4])
with col1:
    try:
        # Asegúrate de que el archivo se llame logo.png y sea el transparente
        st.image("logo.png", width=150) 
    except:
        st.write("🛡️")

with col2:
    st.title("SHADOW IA")
    st.write("### Autonomous Security Code Auditor")

st.markdown("---")

# 4. FUNCIÓN DE ANÁLISIS (Tu Cerebro IA)
API_KEY = "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"

def analizar_codigo(texto):
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}
    data = {
        "model": "llama-3.3-70b-versatile",
        "messages": [
            {"role": "system", "content": "Eres ShadowIA, un experto en ciberseguridad. Analiza vulnerabilidades y da soluciones directas."},
            {"role": "user", "content": f"Analiza este código buscando fallos de seguridad:\n\n{texto}"}
        ]
    }
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        return response.json()['choices'][0]['message']['content']
    else:
        return f"Error en la conexión: {response.status_code}"

# 5. SECCIÓN DE ENTRADA DE CÓDIGO
opcion = st.radio("Elige método de entrada:", ["Pegar Código", "Subir Archivo .py"])

codigo_final = ""

if opcion == "Pegar Código":
    codigo_final = st.text_area("Pega el código aquí:", height=250)
else:
    archivo = st.file_uploader("Carga tu archivo de Python (.py)", type=["py"])
    if archivo:
        codigo_final = archivo.read().decode("utf-8")
        st.code(codigo_final, language="python")

# 6. BOTÓN DE ACCIÓN Y RESULTADOS
if st.button("EJECUTAR ESCANEO SHADOW"):
    if codigo_final:
        with st.spinner("🕵️ ShadowIA rastreando vulnerabilidades..."):
            resultado = analizar_codigo(codigo_final)
            st.markdown(f"### [ RESULTADO DEL ANÁLISIS ]")
            st.info(resultado)
            
            # Crear y mostrar el botón de descarga del PDF
            try:
                pdf_data = generar_pdf(resultado)
                st.download_button(
                    label="📥 DESCARGAR INFORME PDF",
                    data=pdf_data,
                    file_name="reporte_shadowia.pdf",
                    mime="application/pdf"
                )
            except Exception as e:
                st.error(f"No se pudo generar el PDF: {e}")
    else:
        st.error("Por favor, ingresa código o sube un archivo.")