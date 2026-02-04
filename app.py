import streamlit as st
import requests
from fpdf import FPDF
from datetime import datetime

# ==========================================
# 1. CONFIGURACIÓN DE MARCA ELITE
# ==========================================
CIAN_NEON = (0, 255, 255)
FONDO_OSCURO = (14, 17, 23)
GRIS_BLOQUE = (26, 28, 35)
ROJO_ERROR = (255, 51, 51)

st.set_page_config(page_title="ShadowIA - Cyber Audit Platform", page_icon="🛡️", layout="wide")

# Estilo CSS para la Web
st.markdown(f"""
    <style>
    .main {{ background-color: #0E1117; color: white; }}
    .stTextArea textarea {{ background-color: #1A1C23; color: #00FFFF; border: 1px solid #00FFFF; font-family: 'Courier New'; }}
    .stButton>button {{ 
        background-color: #00FFFF; color: black; font-weight: bold; 
        border-radius: 4px; width: 100%; border: none; height: 3em;
        transition: 0.3s;
    }}
    .stButton>button:hover {{ background-color: #00CCCC; transform: scale(1.01); }}
    h1, h2, h3 {{ color: #00FFFF !important; font-family: 'Segoe UI', sans-serif; }}
    .stInfo {{ background-color: #1A1C23; color: white; border: 1px solid #00FFFF; }}
    </style>
    """, unsafe_allow_html=True)

# ==========================================
# 2. MOTOR DE GENERACIÓN PDF PREMIUM
# ==========================================
def generar_pdf_elite(resultado):
    class PDF(FPDF):
        def header(self):
            self.set_fill_color(14, 17, 23)
            self.rect(0, 0, 210, 297, 'F')
            try: self.image("logo.png", 15, 12, 35)
            except: pass
            
            self.set_font("Helvetica", 'B', 9)
            self.set_text_color(0, 255, 255)
            fecha_str = datetime.now().strftime("%d/%m/%Y")
            self.set_xy(140, 12)
            self.cell(55, 6, f"REPORT ID: SHW-{datetime.now().strftime('%M%S')}", ln=True, align='R')
            self.set_x(140)
            self.cell(55, 6, f"DATE: {fecha_str}", ln=True, align='R')
            self.set_x(140)
            self.set_text_color(255, 51, 51)
            self.cell(55, 6, "CLASSIFICATION: CRITICAL", ln=True, align='R')
            
            self.set_draw_color(0, 255, 255)
            self.set_line_width(0.3)
            self.line(10, 38, 200, 38)
            self.ln(25)

        def footer(self):
            self.set_y(-15)
            self.set_font("Helvetica", 'I', 8)
            self.set_text_color(0, 255, 255)
            self.cell(0, 10, f'PROPRIETARY & CONFIDENTIAL - SHADOWIA INTEL - PÁGINA {self.page_no()}', align='C')

    pdf = PDF()
    pdf.add_page()
    
    pdf.set_font("Helvetica", 'B', 18)
    pdf.set_text_color(0, 255, 255)
    pdf.cell(0, 10, "EXECUTIVE AUDIT SUMMARY", ln=True)
    
    pdf.set_fill_color(26, 28, 35)
    pdf.rect(10, 52, 190, 25, 'F')
    pdf.set_xy(15, 55)
    pdf.set_font("Helvetica", 'B', 11)
    pdf.set_text_color(255, 255, 255)
    pdf.cell(0, 7, "OBJETIVO: ANALISIS DE CODIGO ESTATICO (SAST)", ln=True)
    pdf.set_x(15)
    pdf.set_text_color(255, 51, 51)
    pdf.cell(0, 7, "RIESGO DETECTADO: NIVEL CRITICO - ACCION REQUERIDA", ln=True)
    pdf.ln(12)

    lineas = resultado.split('\n')
    for linea in lineas:
        linea_limpia = linea.encode('latin-1', 'ignore').decode('latin-1')
        if not linea_limpia.strip(): continue

        if linea.strip().startswith(('###', '1.', '2.', 'Análisis', '**')):
            pdf.ln(4)
            pdf.set_font("Helvetica", 'B', 13)
            pdf.set_text_color(0, 255, 255)
            pdf.cell(0, 10, f"> {linea_limpia.replace('#','')}", ln=True)
            pdf.set_font("Helvetica", 'B', 8)
            pdf.set_text_color(255, 51, 51)
            pdf.cell(0, 5, "[ SEVERITY: HIGH ]", ln=True)
            pdf.ln(2)
        elif any(x in linea for x in ['python', 'query =', 'def ', 'import ', 'cursor.', 'hashlib']):
            pdf.set_fill_color(20, 22, 28)
            pdf.set_draw_color(0, 255, 255)
            pdf.set_text_color(170, 170, 170)
            pdf.set_font("Courier", size=9)
            pdf.multi_cell(190, 6, txt=linea_limpia, border=1, fill=True)
        else:
            pdf.set_font("Helvetica", size=10)
            pdf.set_text_color(230, 230, 230)
            pdf.multi_cell(0, 7, txt=linea_limpia)

    return pdf.output(dest='S').encode('latin-1')

# ==========================================
# 3. INTERFAZ Y LOGICA DE LA APP
# ==========================================
col1, col2 = st.columns([1, 5])
with col1:
    try: st.image("logo.png", width=140)
    except: st.title("🛡️")
with col2:
    st.title("SHADOWIA CYBER AUDIT")
    st.write("#### Enterprise-Grade AI Security Intelligence")

st.markdown("---")

# TU CLAVE DIRECTA
API_KEY = st.secrets["GROQ_API_KEY"]

def analizar_codigo_ia(texto):
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {API_KEY}", 
        "Content-Type": "application/json"
    }
    
    # Reducción de tamaño para evitar Error 400
    codigo_seguro = texto[:6000].encode('utf-8', 'ignore').decode('utf-8')
    
    data = {
        "model": "llama-3.3-70b-versatile",
        "messages": [
            {"role": "system", "content": "Eres ShadowIA, auditor de ciberseguridad militar. Analiza el código buscando Inyección SQL y fallos graves. Responde en español con soluciones técnicas."},
            {"role": "user", "content": f"Audita este código fuente:\n\n{codigo_seguro}"}
        ],
        "temperature": 0.3
    }
    
    try:
        response = requests.post(url, headers=headers, json=data)
        
        # Log para consola
        print(f"DEBUG GROQ: {response.status_code}")
        
        if response.status_code == 200:
            return response.json()['choices'][0]['message']['content']
        else:
            # Captura detalle del error 400
            detalle = response.json().get('error', {}).get('message', 'Desconocido')
            return f"Error de enlace (Código: {response.status_code}). Detalle: {detalle}"
    except Exception as e:
        return f"Error de conexión: {str(e)}"

opcion = st.radio("MÉTODO DE ENTRADA:", ["Terminal de Código", "Carga de Script (.py)"])
codigo_fuente = ""

if opcion == "Terminal de Código":
    codigo_fuente = st.text_area("CONSOLA DE ENTRADA:", height=300, placeholder="Pega aquí el código sospechoso...")
else:
    archivo_py = st.file_uploader("UPLOAD SOURCE FILE:", type=["py"])
    if archivo_py: codigo_fuente = archivo_py.read().decode("utf-8")

if st.button("INICIAR AUDITORÍA DE SISTEMAS"):
    if codigo_fuente:
        with st.spinner("🕵️ Rastreando vulnerabilidades en el núcleo..."):
            reporte_texto = analizar_codigo_ia(codigo_fuente)
            st.markdown("### 🛠️ HALLAZGOS DE INTELIGENCIA")
            st.info(reporte_texto)
            
            try:
                if "Error de enlace" not in reporte_texto:
                    data_pdf = generar_pdf_elite(reporte_texto)
                    st.download_button(
                        label="📥 DESCARGAR REPORTE DE INTELIGENCIA (PDF)",
                        data=data_pdf,
                        file_name=f"SHADOWIA_AUDIT_{datetime.now().strftime('%Y%m%d')}.pdf",
                        mime="application/pdf"
                    )
            except Exception as e:
                st.error(f"Fallo en motor PDF: {e}")
    else:
        st.error("Error: No se detectó código para procesar.")

