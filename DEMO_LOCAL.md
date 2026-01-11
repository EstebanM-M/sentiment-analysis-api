# 🎭 DEMO LOCAL - STREAMLIT APP

## 🎯 OVERVIEW

Esta es una aplicación de demostración interactiva que permite probar la API de Sentiment Analysis **sin necesidad de deployment**.

**Cualquier persona puede:**
1. Clonar el repositorio
2. Instalar dependencias
3. Ejecutar la demo
4. Ver la API en acción localmente

---

## 🚀 QUICK START

### **Paso 1: Clonar el Repositorio**

```bash
git clone https://github.com/EstebanM-M/sentiment-analysis-api.git
cd sentiment-analysis-api
```

### **Paso 2: Crear Entorno Virtual**

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Mac/Linux
python3 -m venv venv
source venv/bin/activate
```

### **Paso 3: Instalar Dependencias**

```bash
pip install -r requirements.txt
```

**Nota:** Primera instalación tarda ~5 minutos (descarga el modelo de HuggingFace ~500MB)

### **Paso 4: Ejecutar Demo**

```bash
streamlit run app_demo.py
```

La aplicación se abrirá automáticamente en: `http://localhost:8501`

---

## 📱 CARACTERÍSTICAS DE LA DEMO

### **Tab 1: Single Analysis** 🎯
- Analizar un texto individual
- Ver sentimiento (Positive/Negative)
- Ver score de confianza
- Tiempo de procesamiento
- Ejemplos pre-cargados
- Guardar en base de datos

### **Tab 2: Batch Analysis** 📦
- Analizar múltiples textos a la vez
- Ver estadísticas del batch
- Tabla de resultados coloreada
- Exportar a CSV
- Guardar todo en base de datos

### **Tab 3: Statistics** 📊
- Total de análisis realizados
- Distribución Positive/Negative
- Porcentajes
- Tiempo promedio de procesamiento
- Gráficos interactivos
- Actividad reciente

### **Tab 4: History** 🔍
- Historial completo de análisis
- Filtros por sentimiento
- Búsqueda de texto
- Exportar a CSV
- Paginación

---

## 💾 BASE DE DATOS

La demo usa **SQLite** por defecto (no requiere configuración):
- Archivo: `sentiment_analysis.db`
- Se crea automáticamente en la primera ejecución
- Persiste entre sesiones
- Puedes borrarlo para empezar de cero

---

## 🎨 SCREENSHOTS

Toma screenshots de la demo para tu README:

1. **Single Analysis**
   - Análisis positivo exitoso
   - Análisis negativo exitoso
   
2. **Batch Analysis**
   - Procesando múltiples textos
   - Tabla de resultados

3. **Statistics**
   - Dashboard con métricas

4. **History**
   - Lista de análisis históricos

---

## 📝 EJEMPLOS DE USO

### **Analizar Review Positivo:**
```
Text: "This product is absolutely amazing! Best purchase ever."
Result: POSITIVE (99.8% confidence)
```

### **Analizar Review Negativo:**
```
Text: "Terrible experience. Would not recommend."
Result: NEGATIVE (99.9% confidence)
```

### **Batch Analysis:**
```
Text 1: Great service!
Text 2: Not satisfied with quality
Text 3: Average product, nothing special
```

---

## 🛠️ TROUBLESHOOTING

### **Error: "No module named 'transformers'"**
```bash
pip install transformers torch
```

### **Error: "Failed to load model"**
- Verifica conexión a internet (primera vez descarga el modelo)
- Espera ~5 minutos en la primera carga

### **Error: "No module named 'streamlit'"**
```bash
pip install streamlit
```

### **Puerto 8501 ocupado:**
```bash
streamlit run app_demo.py --server.port 8502
```

---

## 🔄 ALTERNATIVA: EJECUTAR LA API

Si prefieres usar la API REST completa:

```bash
# Terminal 1: Iniciar API
python run_api.py

# Terminal 2: Probar endpoints
curl http://localhost:8000/api/v1/health
curl -X POST http://localhost:8000/api/v1/analyze \
  -H "Content-Type: application/json" \
  -d '{"text": "Great product!"}'
```

Swagger UI disponible en: `http://localhost:8000/docs`

---

## 📊 COMPARACIÓN

| Feature | Streamlit Demo | FastAPI |
|---------|----------------|---------|
| **Interfaz** | Visual (UI) | API REST |
| **Uso** | Click & type | HTTP requests |
| **Setup** | 1 comando | Configurar endpoints |
| **Best for** | Demos, testing | Integración, producción |

---

## 🎯 PARA QUÉ SIRVE ESTA DEMO

### **Para Reclutadores:**
- Ver la funcionalidad sin conocimientos técnicos
- Probar la API interactivamente
- Entender las capacidades

### **Para Desarrolladores:**
- Clonar y ejecutar fácilmente
- Verificar que el código funciona
- Experimentar con el modelo
- Base para integración

### **Para Ti (Portfolio):**
- Demo visual sin deployment
- Screenshots profesionales
- Video demo fácil
- Prueba de concepto funcional

---

## 💡 PRÓXIMOS PASOS

Después de probar la demo:

1. ✅ Explora las diferentes tabs
2. ✅ Prueba con tus propios textos
3. ✅ Revisa el código fuente
4. ✅ Mira la documentación de la API
5. ✅ Considera hacer deployment

---

## 📞 CONTACTO

**Esteban** - Electronic Engineer → ML/AI Engineer

- GitHub: [@EstebanM-M](https://github.com/EstebanM-M)
- LinkedIn: [Tu perfil](https://linkedin.com/in/tu-perfil)
- Email: tu-email@example.com

---

## 📄 LICENCIA

MIT License - Ver [LICENSE](LICENSE)

---

**¡Disfruta probando la demo!** 🎉

Si tienes preguntas o sugerencias, abre un issue en GitHub.
