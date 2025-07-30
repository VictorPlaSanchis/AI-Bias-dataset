# 🧠 AI Bias & Data Issue Detector – Plan de Desarrollo Detallado

Este documento describe el roadmap detallado para llevar el proyecto desde su estado actual hasta una versión MVP funcional, incluyendo generación de reportes y visualizaciones para detectar sesgos, leaks y problemas de calidad en datasets CSV.

---

## ✅ Milestone 0 – Estado Actual

- Backend FastAPI funcional (`/api/analyze`), acepta CSV y devuelve preview.
- Frontend con React + Vite creado, sin conexión aún.
- Dataset de prueba presente (`sample_dataset.csv`).
- Docker para backend (sin frontend).

---

## 🚀 Milestone 1 – Integración y Análisis Básico (Semana 1-2)

### 🔹 Backend
- [ ] Parsing automático de tipos de columna (numérica, categórica, booleana, fecha, ID).
- [ ] Análisis de correlación entre features y con el target:
  - [ ] Pearson (variables numéricas).
  - [ ] Cramér’s V (categóricas).
  - [ ] Heatmap de correlación.
- [ ] Detección de data leaks (features muy correladas con el target).
- [ ] Evaluación del balance de clases.
- [ ] Identificación de columnas "problema":
  - [ ] Constantes, vacías.
  - [ ] Altamente correladas.
  - [ ] Columnas tipo ID.

### 🔹 Frontend
- [ ] Conectar formulario de subida con el backend.
- [ ] Mostrar columnas, tipos y primeras filas como preview.

---

## 🎯 Milestone 2 – Evaluación Explicativa (Semana 3-4)

### 🔹 Backend
- [ ] Entrenar modelo de clasificación baseline (RandomForest o XGBoost).
- [ ] Generar explicaciones con:
  - [ ] SHAP (feature importance).
  - [ ] LIME (opcional).
- [ ] Análisis de bias por subgrupos sensibles (`género`, `edad`, `país`, etc.):
  - [ ] Comparación de métricas por subgrupo.
  - [ ] Métricas de fairness: Demographic Parity, Equal Opportunity.
- [ ] Output como JSON estructurado para render visual.

### 🔹 Frontend
- [ ] Mostrar gráficas de distribución y correlación.
- [ ] Visualizar importancia de features (gráfico SHAP).
- [ ] Mostrar alertas de sesgo, leaks, columnas redundantes.

---

## 📄 Milestone 3 – Reporte Visual & Exportable (Semana 5-6)

### 🔹 Backend
- [ ] Motor de reporte HTML (con Jinja2 o HTML puro).
- [ ] Contenido del reporte:
  - Dataset summary.
  - Correlaciones.
  - Data leaks.
  - Feature importance.
  - Fairness/bias analysis.
- [ ] Exportación como PDF (`WeasyPrint` o `pdfkit`).

### 🔹 Frontend
- [ ] Mostrar preview del reporte (HTML renderizado).
- [ ] Botón para "Descargar PDF".

---

## 💼 Milestone 4 – Empaquetado, Demo y Despliegue (Semana 7-8)

### 🔹 Backend
- [ ] Docker completo con backend + frontend.
- [ ] Endpoint `/api/report` para generación directa de reporte HTML/PDF.

### 🔹 Frontend
- [ ] Landing mínima (explicación + demo pública).
- [ ] Modo demo con dataset de ejemplo.

### 🔹 DevOps
- [ ] Publicar en HuggingFace Spaces o Railway.app.
- [ ] Subir imagen Docker a DockerHub.

---

## 🔮 Futuro / Post-MVP

- Comparación entre datasets (pre/post limpieza).
- Plugin Jupyter o librería `ai-bias-detector`.
- Recomendador automático de limpieza.
- Dashboard exploratorio tipo Streamlit.