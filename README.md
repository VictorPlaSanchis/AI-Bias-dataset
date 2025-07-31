# ▶️ Guía de ejecución - AI Bias & Data Issue Detector

Este documento explica cómo ejecutar localmente tanto el **backend** como el **frontend** del proyecto para probar la funcionalidad básica del análisis de datasets.

---

## 📁 Estructura del proyecto

```
AI-Bias-Detector/
├── backend-fastapi/       ← API en FastAPI
├── frontend-vite-app/     ← Frontend React + Vite
└── sample_dataset.csv     ← Dataset de prueba
```

---

## ✅ Requisitos

- Python 3.10+
- Node.js 18+ (con npm)
- pip (gestor de paquetes Python)
- (opcional) Docker

---

## 🧠 1. Ejecutar el Backend (FastAPI)

### Paso 1: Instalar dependencias

```bash
cd backend-fastapi
pip install -r requirements.txt
```

### Paso 2.0: Test

```bash
pytest -q --tb=line
```

### Paso 2: Iniciar el servidor FastAPI

```bash
uvicorn app.main:app --reload --port 8000
```

El backend quedará disponible en:  
🔗 `http://localhost:8000`  
Swagger UI: `http://localhost:8000/docs`

---

## 💻 2. Ejecutar el Frontend (Vite + React)

### Paso 1: Instalar dependencias

```bash
cd frontend-vite-app
npm install
```

### Paso 2: Iniciar la app

```bash
npm run dev
```

La app se abrirá automáticamente en:  
🔗 `http://localhost:5173`

---

## 📤 3. Probar la API manualmente (con CSV)

### Opción A: Usando Swagger UI
1. Ve a `http://localhost:8000/docs`
2. Abre `POST /api/analyze`
3. Haz clic en “Try it out” → Selecciona `sample_dataset.csv`
4. Presiona “Execute” para ver resultado

### Opción B: Usando `curl` (desde terminal)

```bash
curl -X POST http://localhost:8000/api/analyze   -F "file=@/ruta/a/sample_dataset.csv"
```

Ejemplo en Git Bash:

```bash
curl -X POST http://localhost:8000/api/analyze   -F "file=@sample_dataset.csv"
```

---

## 🧪 Dataset de prueba

Si no tienes el CSV, puedes usar el archivo proporcionado en este repositorio:  
📄 `sample_dataset.csv`

Contenido:
```
age,income,gender,default
25,30000,male,0
30,45000,female,0
45,80000,female,1
50,90000,male,0
60,120000,male,1
```

---

## 🧠 ¿Qué hace ahora?

Al subir un CSV:
- El backend lo carga con `pandas`
- Devuelve las columnas y una preview del contenido (3 primeras filas)
- Listo para añadir análisis de correlación, SHAP, fairness...

---

## ❓ Preguntas comunes

**Q: El `curl` dice que no encuentra el archivo.**  
A: Asegúrate de usar `@ruta/del/archivo.csv` (y que el archivo exista)

**Q: El frontend dice que no encuentra la API.**  
A: Verifica que el backend esté corriendo en `localhost:8000` y configurado correctamente

---

## ✅ Estado actual

- Backend funcionando (con subida de CSV)
- Frontend básico corriendo
- Dataset de prueba disponible
- Listo para añadir lógica real de análisis

