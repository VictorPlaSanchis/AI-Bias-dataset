# 📚 Recursos Técnicos para Backend – AI Bias & Data Issue Detector

Este documento recoge papers, artículos, documentación y librerías recomendadas para implementar el backend del proyecto. Está organizado por módulos funcionales clave.

---

## 📘 1. Detección de Sesgos y Fairness

### 📝 Papers / Artículos
- **"Fairness in Machine Learning: Lessons from Political Philosophy"**  
  *Friedler et al., 2016*  
  https://arxiv.org/abs/1412.3756

- **"A Survey on Bias and Fairness in Machine Learning"**  
  *Mehrabi et al., 2019*  
  https://arxiv.org/abs/1908.09635

- **IBM AI Fairness 360 Toolkit**  
  https://aif360.readthedocs.io/en/latest/

### 📦 Librerías
- `aif360`
- `fairlearn`

---

## 📘 2. Detección de Correlaciones y Data Leaks

### 📝 Guías / Conceptos
> ⚠️ Algunos enlaces previos están obsoletos. Se sugiere investigar correlaciones categóricas (como Cramér’s V) y data leakage directamente desde fuentes académicas o ejemplos en repositorios de GitHub.

- **Cramér’s V**
  - Buscar implementaciones en GitHub o calcular manualmente con `scipy.stats.contingency` y `numpy`.

- **Correlación Numérica**
  - Pearson (con `pandas.corr()` o `scipy.stats.pearsonr`)

- **Data Leakage**
  - Revisión manual de features sospechosamente predictivas (muy correlacionadas con el target).
  - Validación cruzada estricta (evitar usar variables creadas post-target).

### 📦 Librerías
- `scipy`, `pingouin`, `pandas`, `yellowbrick`

---

## 📘 3. Explicabilidad con SHAP y LIME

### 📝 Papers Clásicos
- **"SHAP: A Unified Approach to Interpreting Model Predictions"**  
  *Lundberg & Lee, 2017*  
  https://arxiv.org/abs/1705.07874

- **"Why Should I Trust You?": Explaining the Predictions of Any Classifier**  
  *Ribeiro et al., 2016*  
  https://arxiv.org/abs/1602.04938

### 📦 Librerías
- `shap`
- `lime`

---

## 📘 4. Outliers y Detección de Columnas Problemáticas

### 📖 Métodos
- Z-score, IQR
- DBSCAN (clustering)
- Isolation Forest
- Local Outlier Factor (LOF)

### 📚 Referencias
- **Scikit-learn – Guía oficial sobre detección de outliers**  
  https://scikit-learn.org/stable/modules/outlier_detection.html

### 📦 Librerías
- `sklearn`, `scipy`, `numpy`

---

## 📘 5. Reporte HTML / PDF

### 📦 Herramientas
- `Jinja2` – para generar HTML dinámico.
- `WeasyPrint` – HTML + CSS → PDF.
- `pdfkit` – alternativa basada en `wkhtmltopdf`.

### 📚 Guía recomendada
- https://weasyprint.readthedocs.io/

---

## 📘 6. Utilidades Python recomendadas

- `pandas-profiling` (ahora `ydata-profiling`)
- `sweetviz`
- `plotly`, `seaborn`, `matplotlib`

---

## ✅ Recomendación de orden de lectura

1. Fairness: papers de Mehrabi, Friedler y documentación de AIF360.
2. SHAP: paper + ejemplos prácticos.
3. Análisis de correlaciones: Pearson, Cramér’s V.
4. Detección de leakage y outliers.
5. Renderizado de reportes HTML → PDF.