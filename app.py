import streamlit as st
import requests
from fpdf import FPDF
from datetime import datetime

# 1. CONFIGURACIÓN DE MARCA PREMIUM
CIAN_NEON_RGB = (0, 255, 255)
FONDO_OSCURO_RGB = (14, 17, 23)
GRIS_BLOQUE = (26, 28, 35)

st.set_page_config(page_title="ShadowIA - Cyber Audit", page_icon="🛡️", layout="wide")

# Estilo CSS para la interfaz web
st.markdown(f"""
    <style>
    .main {{ background-color: #0E1117; color: white; }}
    .stTextArea textarea {{ background-color: #1A1C23; color: #00FFFF; border: 1px solid #00FFFF; }}
    .stButton>button {{ 
        background-color: #00FFFF; color: black; font-weight: bold; 
        border-radius: 8px; width: 100%; border: none;
    }}
    h1, h2, h3 {{ color: #00FFFF !important; }}
    .stFileUploader {{ border: 1px dashed #00FFFF; border-radius: 10px; padding: 10px; }}
    .stInfo {{ background-color: #1A1C23; color: white; border: 1px solid #00FFFF; }}
    </style>
    """, unsafe_allow_html=True)

# 2. FUNCIÓN PARA GENERAR EL REPORTE PDF "PREMIUM"
def generar_pdf(resultado):
    class PDF(FPDF):
        def header(self):
            # Fondo negro total
            self.set_fill_color(14, 17, 23)
            self.rect(0, 0, 210, 297, 'F')
            
            # Logo en la cabecera
            try:
                self.image("logo.png", 15, 12, 35)
            except:
                pass
            
            # Metadatos del informe (Startup Style)
            self.set_font("Arial", 'B', 8)
            self.set_text_color(0, 255, 255)
            fecha_hoy = datetime.now().strftime("%d/%m/%Y")
            self.set_xy(150, 12)
            self.cell(45, 5, f"FECHA: {fecha_hoy}", ln=True, align='R')
            self.set_x(150)
            self.cell(45, 5, "ID: SHW-AUD-9921", ln=True, align='R')
            self.set_x(150)
            self.cell(45, 5, "STATUS: CRITICAL", ln=True, align='R')
            
            self.ln(25)
            self.set_draw_color(0, 255, 255)
            self.set_line_width(0.5)
            self.line(10, 35, 200, 35) # Línea decorativa neón

        def footer(self):
            self.set_y(-15)
            self.set_font("Arial", 'I', 8)
            self.set_text_color(0, 255, 255)
            self.cell(0, 10, f'CONFIDENTIAL - SHADOWIA CYBER AUDIT - PÁGINA {self.page_no()}', align='C')

    pdf = PDF()
    pdf.add_page()
    
    # TÍTULO PRINCIPAL
    pdf.set_font("Arial", 'B', 20)
    pdf.set_text_color(0, 255, 255)
    pdf.cell(0, 15, "INFORME DE SEGURIDAD ELITE", ln=True, align='L')
    pdf.ln(5)

    # PROCESAMIENTO DE BLOQUES
    lineas = resultado.split('\n')
    for linea in lineas:
        linea_limpia = linea.encode('latin-1', 'ignore').decode('latin-1')
        if not linea_limpia.strip(): continue

        # Si es un Título (Vulnerabilidad)
        if linea.strip().startswith(('###', '1.', '2.', 'Análisis', '**')):
            pdf.ln(5)
            pdf.set_font("Arial", 'B', 14)
            pdf.set_text_color(0, 255, 255)
            pdf.multi_cell(0, 10, txt=linea_limpia.replace('#',''))
        
        # Si es Código (Caja Gris con borde Neón)
        elif any(x in linea for x in ['python', 'query =', 'def ', 'import ', 'cursor.']):
            pdf.set_fill_color(26, 28, 35) # Gris medio oscuro
            pdf.set_draw_color(0, 255, 255) # Borde Cian
            pdf.set_text_color(200, 200, 200) # Texto gris claro
            pdf.set_font("Courier", size=9)
            # Dibujamos el bloque de código
            ancho_pag = 190
            pdf.multi_cell(ancho_pag, 7, txt=linea_limpia, border=1, fill=True)
        
        # Texto Normal
        else:
            pdf.set_font("Arial", size=11)
            pdf.set_text_color(240, 240, 240) # Blanco casi puro
            pdf.multi_cell(0, 8, txt=linea_limpia)

    return pdf.output(dest='S').encode('latin-1')

# 3. INTERFAZ WEB (SE MANTIENE IGUAL)
col1, col2 = st.columns([1, 4])
with col1:
    try: st.image("logo.png", width=150)
    except: st.write("🛡️")
with col2:
    st.title("SHADOW IA")
    st.write("### Autonomous Security Code Auditor")

st.markdown("---")

API_KEY = st.secrets["GROQ_API_KEY"]

def analizar_codigo(texto):
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}
    data = {
        "model": "llama-3.3-70b-versatile",
        "messages": [
            {"role": "system", "content": "Eres ShadowIA, un auditor de élite. Analiza fallos como Inyección SQL y contraseñas expuestas. Responde con títulos claros y bloques de código de solución."},
            {"role": "user", "content": f"Audita este código:\n\n{texto}"}
        ]
    }
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        return response.json()['choices'][0]['message']['content']
    return f"Error: {response.status_code}"

opcion = st.radio("Entrada:", ["Pegar Código", "Subir Archivo .py"])
codigo_final = ""
if opcion == "Pegar Código":
    codigo_final = st.text_area("Pega el código:", height=250)
else:
    archivo = st.file_uploader("Sube .py", type=["py"])
    if archivo: codigo_final = archivo.read().decode("utf-8")

if st.button("EJECUTAR ESCANEO SHADOW"):
    if codigo_final:
        with st.spinner("🕵️ Auditando..."):
            resultado = analizar_codigo(codigo_final)
            st.info(resultado)
            try:
                pdf_data = generar_pdf(resultado)
                st.download_button(
                    label="📥 DESCARGAR INFORME PREMIUM PDF",
                    data=pdf_data,
                    file_name="shadowia_premium_report.pdf",
                    mime="application/pdf"
                )
            except Exception as e:
                st.error(f"Error PDF: {e}")
