import streamlit as st
import requests
from fpdf import FPDF

# 1. CONFIGURACIÓN DE MARCA (Cian Neón)
CIAN_NEON_RGB = (0, 255, 255)
FONDO_OSCURO_RGB = (14, 17, 23)

st.set_page_config(page_title="ShadowIA - Cyber Audit", page_icon="🛡️", layout="wide")

# Estilo CSS para la interfaz web
st.markdown(f"""
    <style>
    .main {{ background-color: #0E1117; color: white; }}
    .stTextArea textarea {{ background-color: #1A1C23; color: #00FFFF; border: 1px solid #00FFFF; }}
    .stButton>button {{ 
        background-color: #00FFFF; 
        color: black; 
        font-weight: bold; 
        border-radius: 8px;
        width: 100%;
        border: none;
    }}
    h1, h2, h3 {{ color: #00FFFF !important; }}
    .stFileUploader {{ border: 1px dashed #00FFFF; border-radius: 10px; padding: 10px; }}
    .stInfo {{ background-color: #1A1C23; color: white; border: 1px solid #00FFFF; }}
    </style>
    """, unsafe_allow_html=True)

# 2. FUNCIÓN PARA GENERAR EL REPORTE PDF CON ESTILO HACKER
def generar_pdf(resultado):
    class PDF(FPDF):
        def header(self):
            # Pintar el fondo de toda la página de negro
            self.set_fill_color(14, 17, 23)
            self.rect(0, 0, 210, 297, 'F')
            
            # Insertar Logo
            try:
                self.image("logo.png", 10, 8, 30)
            except:
                pass
            
            # Título del Informe en Cian
            self.set_font("Arial", 'B', 16)
            self.set_text_color(0, 255, 255)
            self.cell(0, 10, "INFORME DE AUDITORIA - SHADOWIA", ln=True, align='C')
            self.ln(20)

        def footer(self):
            self.set_y(-15)
            self.set_font("Arial", 'I', 8)
            self.set_text_color(0, 255, 255)
            self.cell(0, 10, f'ShadowIA - Autonomous Security Audit - Página {self.page_no()}', align='C')

    pdf = PDF()
    pdf.add_page()
    
    # Procesar el texto para dar formato a títulos y códigos
    lineas = resultado.split('\n')
    for linea in lineas:
        linea_limpia = linea.encode('latin-1', 'ignore').decode('latin-1')
        
        # Detectar títulos o secciones importantes para poner en Cian
        if linea.strip().startswith(('###', '1.', '2.', 'Análisis', '**')):
            pdf.set_font("Arial", 'B', 12)
            pdf.set_text_color(0, 255, 255)
            pdf.multi_cell(0, 10, txt=linea_limpia)
        # Detectar bloques de código
        elif 'python' in linea or 'query =' in linea or 'def ' in linea:
            pdf.set_font("Courier", size=10)
            pdf.set_text_color(180, 180, 180) # Gris claro
            pdf.multi_cell(0, 7, txt=linea_limpia)
        else:
            # Texto normal en blanco
            pdf.set_font("Arial", size=11)
            pdf.set_text_color(255, 255, 255)
            pdf.multi_cell(0, 8, txt=linea_limpia)
    
    return pdf.output(dest='S').encode('latin-1')

# 3. ENCABEZADO DE LA PÁGINA
col1, col2 = st.columns([1, 4])
with col1:
    try:
        st.image("logo.png", width=150) 
    except:
        st.write("🛡️")

with col2:
    st.title("SHADOW IA")
    st.write("### Autonomous Security Code Auditor")

st.markdown("---")

# 4. CONFIGURACIÓN DE LA IA (SECRETOS)
API_KEY = st.secrets["GROQ_API_KEY"]

def analizar_codigo(texto):
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}
    data = {
        "model": "llama-3.3-70b-versatile",
        "messages": [
            {"role": "system", "content": "Eres ShadowIA, un experto en ciberseguridad. Analiza vulnerabilidades críticas como Inyección SQL y contraseñas expuestas y da soluciones técnicas directas."},
            {"role": "user", "content": f"Analiza este código buscando fallos de seguridad:\n\n{texto}"}
        ]
    }
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        return response.json()['choices'][0]['message']['content']
    else:
        return f"Error en la conexión con la IA: {response.status_code}"

# 5. INTERFAZ DE USUARIO
opcion = st.radio("Elige método de entrada:", ["Pegar Código", "Subir Archivo .py"])
codigo_final = ""

if opcion == "Pegar Código":
    codigo_final = st.text_area("Pega el código aquí:", height=250)
else:
    archivo = st.file_uploader("Carga tu archivo de Python (.py)", type=["py"])
    if archivo:
        codigo_final = archivo.read().decode("utf-8")
        st.code(codigo_final, language="python")

# 6. EJECUCIÓN Y DESCARGA
if st.button("EJECUTAR ESCANEO SHADOW"):
    if codigo_final:
        with st.spinner("🕵️ ShadowIA rastreando vulnerabilidades..."):
            resultado = analizar_codigo(codigo_final)
            st.markdown(f"### [ RESULTADO DEL ANÁLISIS ]")
            st.info(resultado)
            
            try:
                pdf_data = generar_pdf(resultado)
                st.download_button(
                    label="📥 DESCARGAR INFORME PDF PROFESIONAL",
                    data=pdf_data,
                    file_name="reporte_shadowia.pdf",
                    mime="application/pdf"
                )
            except Exception as e:
                st.error(f"Error al generar el PDF con diseño: {e}")
    else:
        st.error("Por favor, ingresa código o sube un archivo para analizar.")

