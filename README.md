# 🛡️ SHADOWIA - CYBER AUDIT

```json
 ██████  ██   ██  █████  ██████   ██████  ██     ██ ██  █████  
██       ██   ██ ██   ██ ██   ██ ██    ██ ██     ██ ██ ██   ██ 
   ████  ███████ ███████ ██   ██ ██    ██ ██  █  ██ ██ ███████ 
      ██ ██   ██ ██   ██ ██   ██ ██    ██ ██ ███ ██ ██ ██   ██ 
██████   ██   ██ ██   ██ ██████   ██████   ███ ███  ██ ██   ██ 
                                                               
      >> NEXT-GEN AI CYBER AUDIT ENGINE [v2.0.4]
```

[![Python](https://img.shields.io/badge/Python-3.10+-00FFFF?style=for-the-badge&logo=python&logoColor=black)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-App-00FFFF?style=for-the-badge&logo=streamlit&logoColor=black)](https://streamlit.io/)
[![Llama3.3](https://img.shields.io/badge/AI-Llama_3.3_70B-00FFFF?style=for-the-badge&logo=meta&logoColor=black)](https://groq.com/)

---

## 📝 Descripción Técnica
**ShadowIA - Cyber Audit** es una suite avanzada de inteligencia de seguridad diseñada para la identificación proactiva de vectores de ataque. Mediante la integración de **Modelos de Lenguaje de Gran Escala (LLM)** y técnicas de **Análisis Estático (SAST)** y **Dinámico (DAST)**, la plataforma automatiza la detección de vulnerabilidades críticas en infraestructuras digitales.

Este sistema no solo identifica fallos bajo el estándar **OWASP Top 10**, sino que contextualiza el riesgo y genera una hoja de ruta de remediación técnica automatizada.



---

## 🚀 Características Principales

### 🔍 Auditoría de Código (SAST)
* **Análisis Profundo:** Detección de Inyección SQL, Cross-Site Scripting (XSS), Inyección de Comandos y Broken Access Control.
* **Soporte Multi-archivo:** Procesamiento de proyectos completos mediante carga de archivos `.zip` o selección múltiple.
* **Contextualización IA:** Explicación técnica de la vulnerabilidad y propuesta de código corregido (Patching).

### 🌐 Auditoría de Red y Web (DAST)
* **Live Scanning:** Escaneo de puertos activos (FTP, SSH, HTTP, MySQL, etc.).
* **Security Headers:** Análisis de cabeceras de seguridad (HSTS, XSS-Protection, CSP).
* **Target Fingerprinting:** Identificación de tecnologías de servidor y superficies de exposición.

### 📄 Reporting Enterprise
* **Métricas Dinámicas:** Visualización de amenazas mediante dashboards interactivos de Plotly.
* **PDF Certificado:** Generación de informes con sello de integridad digital, métricas ISO 27001 y roadmap de remediación prioritario.

---

## 🛠️ Stack Tecnológico
* **Frontend:** Streamlit (UI Táctica en Modo Oscuro).
* **Core Engine:** Python 3.10+.
* **AI Model:** Llama 3.3 70B (Groq Inference Engine).
* **Data Viz:** Plotly Express.
* **PDF Engine:** FPDF2 con soporte para renderizado binario.

---

## ⚙️ Instalación y Despliegue

1. **Clonar el repositorio:**
   ```bash
   git clone [https://github.com/TU_USUARIO/shadowia-cyber-audit.git](https://github.com/TU_USUARIO/shadowia-cyber-audit.git)
   cd shadowia-cyber-audit
   ```

2. **Instalar dependencias:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configurar Secretos:**
   Crea un archivo `.streamlit/secrets.toml` o configura las variables de entorno:
   ```toml
   GROQ_API_KEY = "tu_api_key_aqui"
   ```

4. **Ejecutar Localmente:**
   ```bash
   streamlit run app.py
   ```

---

## 🛡️ Estándares de Cumplimiento
ShadowIA evalúa los activos basándose en los siguientes marcos de trabajo internacionales:
- **OWASP Top 10** (Vulnerabilidades Web)
- **ISO/IEC 27001** (Controles de Seguridad de la Información)
- **GDPR** (Privacidad y Protección de Datos)

---

## 🤝 Contribuciones
Las contribuciones son lo que hacen a la comunidad de ciberseguridad un lugar increíble para aprender e innovar. Cualquier contribución que hagas será **muy apreciada**.

1. Realiza un Fork del proyecto.
2. Crea tu Feature Branch (`git checkout -b feature/AmazingFeature`).
3. Realiza un Commit de tus cambios (`git commit -m 'Add AmazingFeature'`).
4. Realiza un Push a la Rama (`git push origin feature/AmazingFeature`).
5. Abre un Pull Request.

---

Desarrollado con 💻 y 🛡️ por **shadowia-sofiazilijosky**
```text
SHADOWIA - THE FUTURE OF SECURE CODE
```
