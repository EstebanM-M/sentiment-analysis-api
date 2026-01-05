# ⚡ QUICK START GUIDE

## 🚀 Empezar en 5 Minutos

### 1️⃣ Setup (2 min)
```bash
# Descomprimir y entrar al proyecto
cd sentiment-analysis-api

# Crear entorno virtual
python -m venv venv

# Activar
source venv/bin/activate  # Windows: venv\Scripts\activate

# Instalar
pip install -e .
```

### 2️⃣ Probar Modelo (2 min)
```bash
# Test rápido
python test_model.py

# Verás análisis de sentimientos en vivo! 🎭
```

### 3️⃣ Tests (1 min)
```bash
# Ejecutar tests
pytest -v

# Deberías ver 12 tests ✅
```

---

## 🎯 ¿Funcionó todo?

Si viste esto, estás listo! ✅

```
🧪 Testing Sentiment Analysis Model

Loading model...
Model loaded successfully

Text: I love this product! It's amazing...
Sentiment: POSITIVE
Confidence: 99.87%

✅ All tests passed!
```

---

## 📁 Archivos Importantes

| Archivo | Para qué sirve |
|---------|----------------|
| `RESUMEN_DIA_1.md` | 📊 Resumen completo del día |
| `DIA_1_PROGRESO.md` | 🎯 Detalles técnicos y próximos pasos |
| `GITHUB_SETUP.md` | 🐙 Cómo subir a GitHub |
| `README.md` | 📖 Documentación del proyecto |
| `src/models/sentiment_model.py` | 🧠 El código del modelo |
| `tests/test_model.py` | 🧪 Tests unitarios |

---

## 🆘 Problemas?

### Error: "No module named 'torch'"
```bash
pip install torch
```

### Error: "No module named 'transformers'"
```bash
pip install transformers
```

### Tests fallan
```bash
pip install -e ".[dev]"
```

---

## ✅ Checklist Antes del Día 2

- [ ] Modelo descarga y funciona
- [ ] Tests pasan (12/12)
- [ ] Entiendes la estructura del código
- [ ] Proyecto listo para GitHub

---

## 🔜 ¿Qué sigue?

**Día 2**: Crear la API con FastAPI
- Endpoints REST
- Swagger UI
- Validación de datos
- Tests de API

**Tiempo**: ~4 horas
**Resultado**: API funcional en http://localhost:8000

---

**¿Listo?** Lee `RESUMEN_DIA_1.md` para más detalles! 🚀
