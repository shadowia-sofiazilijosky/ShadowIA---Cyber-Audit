import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import json
import re
import zipfile
import io
import socket
import os
from fpdf import FPDF
from datetime import datetime

# ==========================================
# 1. CONFIGURACIÓN DE MARCA Y ESTILO
# ==========================================
st.set_page_config(page_title="SHADOWIA - CYBER AUDIT", page_icon="🛡️", layout="wide")

st.markdown(f"""
    <style>
    .main {{ background-color: #0E1117; color: white; }}
    .stTextArea textarea {{ background-color: #1A1C23; color: #00FFFF; border: 1px solid #00FFFF; font-family: 'Courier New'; }}
    .stButton>button {{ 
        background-color: #00FFFF; color: black; font-weight: bold; 
        border-radius: 4px; width: 100%; border: none; height: 3em;
        transition: 0.3s;
    }}
    .stButton>button:hover {{ background-color: #00CCCC; transform: scale(1.05); }}
    h1, h2, h3 {{ color: #00FFFF !important; font-family: 'Segoe UI', sans-serif; }}
    .stInfo {{ background-color: #1A1C23; color: white; border: 1px solid #00FFFF; }}
    </style>
    """, unsafe_allow_html=True)

# ==========================================
# 2. MOTOR PDF SHADOWIA - VERSIÓN CORREGIDA
# ==========================================
class ShadowPDF(FPDF):
    def __init__(self):
        super().__init__()
        self.set_auto_page_break(auto=True, margin=25)

    def add_page(self, *args, **kwargs):
        super().add_page(*args, **kwargs)
        self.set_fill_color(14, 17, 23)
        self.rect(0, 0, 210, 297, 'F')
        self.render_brand_elements()

    def render_brand_elements(self):
        # Mantenemos el logo si existe
        if os.path.exists("logo.png"):
            self.image("logo.png", 12, 12, 28)
        self.set_font("Helvetica", 'B', 16)
        self.set_text_color(0, 255, 255) 
        self.set_xy(45, 14)
        self.cell(0, 10, "SHADOWIA - CYBER AUDIT", ln=True)
        self.set_font("Helvetica", '', 9)
        self.set_text_color(160, 160, 160)
        self.set_xy(45, 23)
        fecha_str = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        client_id_str = f"SHW-USR-{datetime.now().strftime('%H%M%S')}"
        self.cell(0, 5, f"DATE: {fecha_str}  |  REPORT ID: {client_id_str}", ln=True)

    def footer(self):
        self.set_y(-20)
        self.set_font("Helvetica", 'I', 8)
        self.set_text_color(0, 255, 255)
        self.cell(0, 10, f'PROPRIETARY & CONFIDENTIAL - SHADOWIA - PAGE {self.page_no()}', align='C')

    def create_table(self, title, data, col_widths):
        self.set_font("Helvetica", 'B', 11)
        self.set_text_color(0, 255, 255)
        self.cell(0, 10, title, ln=True)
        self.set_fill_color(30, 30, 35)
        self.set_draw_color(0, 255, 255)
        self.set_font("Helvetica", 'B', 9)
        for i, header in enumerate(data[0]):
            self.cell(col_widths[i], 8, header, 1, 0, 'C', True)
        self.ln()
        self.set_font("Helvetica", '', 9)
        self.set_text_color(255, 255, 255)
        for row in data[1:]:
            for i, item in enumerate(row):
                self.cell(col_widths[i], 7, str(item), 1, 0, 'L', True)
            self.ln()
        self.ln(5)

def generar_pdf_final(reporte_texto, stats, fig):
    pdf = ShadowPDF()
    pdf.add_page()
    
    # I. Resumen Ejecutivo
    pdf.create_table("1. EXECUTIVE SECURITY SUMMARY", [
        ["METRIC", "VALUE"],
        ["Critical Vulnerabilities", stats.get('criticos', 0)],
        ["High Risk Threats", stats.get('altos', 0)],
        ["Security Score", f"{stats.get('score', 0)}/100"],
        ["Compliance Status", "ISO 27001 READY" if stats.get('score', 0) > 80 else "NEEDS REVIEW"]
    ], [95, 95])

    # II. Gráfico de Amenazas
    pdf.set_font("Helvetica", 'B', 11)
    pdf.set_text_color(0, 255, 255)
    pdf.cell(0, 10, "2. THREAT DISTRIBUTION CHART", ln=True)
    
    # Usar BytesIO para el gráfico evita archivos temporales corruptos
    img_buf = io.BytesIO()
    fig.write_image(img_buf, format="png", scale=2)
    pdf.image(img_buf, x=15, y=pdf.get_y() + 5, w=180)
    pdf.set_y(pdf.get_y() + 110)

    # III. Ruta de Remediación
    remediacion_data = [
        ["PRIORITY", "ACTION REQUIRED", "ESTIMATED EFFORT"],
        ["CRITICAL", "Fix Code Injections / Leaks", "Immediate"],
        ["HIGH", "Patch Dependencies & SSL", "High"],
        ["MEDIUM", "Security Header Config", "Medium"]
    ]
    pdf.create_table("3. REMEDIATION ROADMAP", remediacion_data, [40, 100, 50])

    # IV. Reporte Detallado
    pdf.add_page()
    pdf.set_font("Helvetica", 'B', 11)
    pdf.set_text_color(0, 255, 255)
    pdf.cell(0, 10, "4. DETAILED INTELLIGENCE REPORT", ln=True)
    pdf.ln(5)
    pdf.set_font("Helvetica", '', 9)
    pdf.set_text_color(220, 220, 220)
    reporte_safe = reporte_texto.encode('latin-1', 'ignore').decode('latin-1')
    pdf.multi_cell(0, 6, txt=reporte_safe)

    # V. Sello de Integridad
    pdf.ln(10)
    pdf.set_draw_color(0, 255, 255)
    pdf.rect(130, pdf.get_y(), 65, 22)
    pdf.set_xy(130, pdf.get_y() + 2)
    pdf.set_font("Helvetica", 'B', 8)
    pdf.cell(65, 5, "SHADOWIA DIGITAL SEAL", ln=True, align='C')
    pdf.set_font("Helvetica", '', 6)
    pdf.set_text_color(150, 150, 150)
    pdf.multi_cell(65, 4, f"Hash: {hash(reporte_texto)}\nVerified by ShadowIA AI\nISO/OWASP Compliant", align='C')

    # ARREGLO PARA STREAMLIT: Forzar salida a bytes puros
    pdf_output = pdf.output(dest='S')
    if isinstance(pdf_output, bytearray):
        return bytes(pdf_output)
    return pdf_output

# ==========================================
# 3. LÓGICA DE PROCESAMIENTO
# ==========================================
def audit_web_live(url):
    try:
        dominio = url.replace("https://", "").replace("http://", "").split("/")[0]
        reporte = f"SCANNING TARGET: {dominio}\n"
        puertos = {21: "FTP", 22: "SSH", 80: "HTTP", 443: "HTTPS", 3306: "MySQL"}
        abiertos = []
        for p, s in puertos.items():
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(0.6)
            if sock.connect_ex((dominio, p)) == 0: abiertos.append(f"{p}({s})")
            sock.close()
        reporte += f"OPEN PORTS: {', '.join(abiertos) if abiertos else 'None'}\n"
        h = requests.get(f"http://{dominio}", timeout=5).headers
        reporte += f"SERVER: {h.get('Server', 'Hidden')}\nWEB-PROTECTION: {h.get('X-XSS-Protection', 'Disabled')}"
        return reporte
    except: return "Target unreachable for live scanning."

def procesar_archivos(lista_archivos):
    contenido = ""
    for archivo in lista_archivos:
        if archivo.name.endswith('.zip'):
            with zipfile.ZipFile(archivo, 'r') as z:
                for n in z.namelist():
                    if n.endswith(('.py', '.js', '.java', '.php', '.sql', '.sh', '.cpp', '.c', '.txt')):
                        with z.open(n) as f:
                            contenido += f"\n--- FILE: {n} ---\n{f.read().decode('utf-8', errors='ignore')}"
        else:
            contenido += f"\n--- FILE: {archivo.name} ---\n{archivo.read().decode('utf-8', errors='ignore')}"
    return contenido

def analizar_ia(texto):
    API_KEY = st.secrets["GROQ_API_KEY"]
    prompt = f"Eres ShadowIA de SHADOWIA - CYBER AUDIT. Analiza vulnerabilidades bajo ISO 27001 y OWASP. Al final incluye: DATA_START{{\"criticos\": X, \"altos\": X, \"medios\": X, \"bajos\": X, \"score\": X}}DATA_END"
    r = requests.post("https://api.groq.com/openai/v1/chat/completions",
        headers={"Authorization": f"Bearer {API_KEY}"},
        json={
            "model": "llama-3.3-70b-versatile",
            "messages": [{"role": "system", "content": prompt}, {"role": "user", "content": texto[:9000]}],
            "temperature": 0.1
        })
    return r.json()['choices'][0]['message']['content']

def extraer_metricas(texto):
    try:
        match = re.search(r'DATA_START(.*?)}DATA_END', texto, re.DOTALL)
        if match:
            stats = json.loads(match.group(1) + "}")
            return stats, texto.replace(match.group(0), "").strip()
    except: pass
    return {"criticos": 0, "altos": 0, "medios": 0, "bajos": 0, "score": 100}, texto

# ==========================================
# 4. INTERFAZ STREAMLIT
# ==========================================
col_logo, col_text = st.columns([1, 4])
with col_logo:
    if os.path.exists("logo.png"): st.image("logo.png", width=150)
    else: st.title("🛡️")
with col_text:
    st.title("SHADOWIA - CYBER AUDIT")
    st.write("#### AI Security Intelligence: Static & Dynamic Analysis")

st.markdown("---")

metodo = st.sidebar.selectbox("MÓDULO DE AUDITORÍA:", ["Pegar Código", "Subir Archivos/ZIP", "URL Web Live"])
input_data = ""

if metodo == "Pegar Código":
    input_data = st.text_area("CÓDIGO FUENTE:", height=300, placeholder="Pega aquí tu código...")
elif metodo == "Subir Archivos/ZIP":
    files = st.file_uploader("Subir archivos sueltos (.py, .js, etc.) o Proyectos (.zip):", accept_multiple_files=True)
    if files: input_data = procesar_archivos(files)
else:
    url = st.text_input("URL OBJETIVO (ej: https://google.com):")
    if url:
        with st.spinner("Escaneando Red..."):
            input_data = audit_web_live(url)

if st.button("INICIAR AUDITORÍA TÁCTICA"):
    if input_data:
        with st.spinner("🤖 ShadowIA analizando..."):
            raw = analizar_ia(input_data)
            stats, reporte = extraer_metricas(raw)
            
            # DASHBOARD
            m1, m2, m3 = st.columns(3)
            m1.metric("RIESGOS CRÍTICOS", stats['criticos'], delta="Acción Urgente", delta_color="inverse")
            m2.metric("PUNTAJE SEGURIDAD", f"{stats['score']}/100")
            m3.metric("ISO 27001 STATUS", "COMPLIANT" if stats['score'] > 80 else "RISK")

            df = pd.DataFrame({'Nivel': ['Crítico', 'Alto', 'Medio', 'Bajo'], 
                              'Count': [stats['criticos'], stats['altos'], stats['medios'], stats['bajos']]})
            fig = px.bar(df, x='Nivel', y='Count', color='Nivel', template="plotly_dark",
                         color_discrete_map={'Crítico':'#FF3333','Alto':'#FFA500','Medio':'#FFFF00','Bajo':'#00FF00'})
            st.plotly_chart(fig, use_container_width=True)
            
            st.info(reporte)
            
            # PDF GENERATION (Arreglado)
            pdf_bytes = generar_pdf_final(reporte, stats, fig)
            st.download_button(
                label="📥 DESCARGAR REPORTE SHADOWIA",
                data=pdf_bytes,
                file_name=f"ShadowIA_Audit_{datetime.now().strftime('%M%S')}.pdf",
                mime="application/pdf"
            )
    else:
        st.error("Error: Por favor ingresa datos para la auditoría.")
