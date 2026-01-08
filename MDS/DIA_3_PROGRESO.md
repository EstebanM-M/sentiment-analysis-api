# DÍA 3: DATABASE INTEGRATION - PROGRESO

## ✅ COMPLETADO

### 1. Modelos de Base de Datos (100%)
**Archivo**: `src/database/models.py`

Modelos SQLAlchemy implementados:
- ✅ `SentimentAnalysis` - Almacena cada análisis de sentimiento
  - id, text, label, score
  - created_at, processing_time_ms
  - model_name, is_batch
- ✅ `AnalysisStats` - Estadísticas agregadas (para dashboards)
  - Conteos diarios
  - Promedios
  - Métricas de performance

**Características:**
- Indexes para queries eficientes
- Timestamps automáticos
- Métodos to_dict() para serialización
- Soporte para SQLite y PostgreSQL

### 2. Configuración de Base de Datos (100%)
**Archivo**: `src/database/database.py`

- ✅ Engine SQLAlchemy configurado
- ✅ SessionLocal para manejo de sesiones
- ✅ init_db() para crear tablas
- ✅ get_db() dependency para FastAPI
- ✅ close_db() para cleanup
- ✅ Soporte dual: SQLite (dev) / PostgreSQL (prod)

### 3. CRUD Operations (100%)
**Archivo**: `src/database/crud.py`

Operaciones implementadas:
- ✅ create_analysis() - Guardar nuevo análisis
- ✅ get_analysis_by_id() - Obtener por ID
- ✅ get_analyses() - Listar con filtros y paginación
- ✅ get_total_analyses_count() - Contar total
- ✅ delete_analysis() - Eliminar análisis
- ✅ get_statistics() - Estadísticas agregadas
- ✅ get_recent_analyses() - Últimos análisis
- ✅ get_analyses_by_date_range() - Timeline por fecha
- ✅ search_analyses() - Búsqueda por texto
- ✅ update_daily_stats() - Actualizar stats diarias

### 4. Schemas Actualizados (100%)
**Archivo**: `src/api/schemas.py`

Nuevos schemas agregados:
- ✅ `AnalysisHistoryItem` - Item individual en historial
- ✅ `AnalysisHistoryResponse` - Respuesta paginada
- ✅ `StatsResponse` - Estadísticas completas
- ✅ `DateRangeStats` - Timeline por fechas

### 5. Endpoints REST Actualizados (100%)
**Archivo**: `src/api/routes/sentiment.py`

#### Endpoints Modificados:
- ✅ POST /api/v1/analyze - Ahora guarda en DB automáticamente
- ✅ POST /api/v1/batch-analyze - Guarda cada análisis del batch

#### Nuevos Endpoints:
1. **GET /api/v1/history**
   - Historial paginado de análisis
   - Filtros: label, min_score
   - Parámetros: page, page_size

2. **GET /api/v1/stats**
   - Estadísticas agregadas
   - Total de análisis
   - Conteos por sentimiento
   - Promedios de score y tiempo
   - Opcional: filtrar por días

3. **GET /api/v1/stats/timeline**
   - Conteo de análisis por fecha
   - Últimos N días (default: 7)
   - Útil para gráficas

4. **GET /api/v1/search**
   - Búsqueda por contenido de texto
   - Parámetro: q (query)
   - Límite configurable

### 6. Integración en Lifespan (100%)
**Archivo**: `src/api/main.py`

- ✅ init_db() se llama en startup
- ✅ close_db() se llama en shutdown
- ✅ Manejo de errores robusto

---

## 📊 ESTADÍSTICAS DEL DÍA 3

```
📦 Archivos nuevos:        3
📦 Archivos modificados:   6
📝 Líneas de código:       ~700
🔌 Endpoints nuevos:       4
⚙️  Funciones CRUD:        10+
⏱️  Tiempo estimado:       5-6 horas
```

---

## 🚀 CÓMO USAR LA BASE DE DATOS

### Opción 1: SQLite (Desarrollo - Por defecto)

```bash
# No requiere configuración adicional
# El archivo se crea automáticamente en:
# sentiment_analysis.db

python run_api.py
# La base de datos se crea en el primer arranque
```

### Opción 2: PostgreSQL (Producción)

```bash
# 1. Instalar PostgreSQL localmente o usar Docker
docker run -d \
  --name sentiment-postgres \
  -e POSTGRES_USER=sentiment_user \
  -e POSTGRES_PASSWORD=sentiment_pass \
  -e POSTGRES_DB=sentiment_db \
  -p 5432:5432 \
  postgres:15-alpine

# 2. Configurar .env
echo "DATABASE_URL=postgresql://sentiment_user:sentiment_pass@localhost:5432/sentiment_db" >> .env

# 3. Iniciar API
python run_api.py
```

### Opción 3: Docker Compose (Todo en uno)

```bash
# Ya está configurado en docker-compose.yml
docker-compose up --build

# API: http://localhost:8000
# PostgreSQL: localhost:5432
```

---

## 🎯 VALIDACIÓN - CHECKLIST

### 1. ✅ Base de datos se inicializa
```bash
python run_api.py
# Ver logs:
# "Initializing database..."
# "Database initialized successfully"
```

### 2. ✅ Análisis se guardan automáticamente
```bash
# Hacer un análisis
curl -X POST http://localhost:8000/api/v1/analyze \
  -H "Content-Type: application/json" \
  -d '{"text": "This is amazing!"}'

# Verificar en historial
curl http://localhost:8000/api/v1/history
```

### 3. ✅ Nuevos endpoints funcionan
```bash
# History
curl "http://localhost:8000/api/v1/history?page=1&page_size=10"

# Stats
curl "http://localhost:8000/api/v1/stats"

# Timeline
curl "http://localhost:8000/api/v1/stats/timeline?days=7"

# Search
curl "http://localhost:8000/api/v1/search?q=amazing"
```

### 4. ✅ Swagger UI actualizado
Abre http://localhost:8000/docs
- Verifica que aparecen los 4 nuevos endpoints
- Prueba cada uno desde la interfaz

---

## 💡 EJEMPLOS DE USO

### Ejemplo 1: Analizar y Ver en Historial

```bash
# 1. Hacer varios análisis
curl -X POST http://localhost:8000/api/v1/analyze \
  -H "Content-Type: application/json" \
  -d '{"text": "Great product!"}'

curl -X POST http://localhost:8000/api/v1/analyze \
  -H "Content-Type: application/json" \
  -d '{"text": "Terrible experience"}'

curl -X POST http://localhost:8000/api/v1/analyze \
  -H "Content-Type: application/json" \
  -d '{"text": "It'\''s okay"}'

# 2. Ver historial
curl http://localhost:8000/api/v1/history?page=1&page_size=10
```

**Response:**
```json
{
  "total": 3,
  "page": 1,
  "page_size": 10,
  "analyses": [
    {
      "id": 3,
      "text": "It's okay",
      "label": "POSITIVE",
      "score": 0.5521,
      "created_at": "2025-01-06T12:03:00Z",
      "processing_time_ms": 45.2,
      "model_name": "distilbert-base-uncased-finetuned-sst-2-english",
      "is_batch": false
    },
    ...
  ]
}
```

### Ejemplo 2: Ver Estadísticas

```bash
curl http://localhost:8000/api/v1/stats
```

**Response:**
```json
{
  "total_analyses": 150,
  "positive_count": 120,
  "negative_count": 30,
  "positive_percentage": 80.0,
  "negative_percentage": 20.0,
  "average_score": 0.89,
  "average_processing_time_ms": 45.2
}
```

### Ejemplo 3: Timeline para Gráfica

```bash
curl "http://localhost:8000/api/v1/stats/timeline?days=7"
```

**Response:**
```json
{
  "dates": {
    "2025-01-01": 10,
    "2025-01-02": 15,
    "2025-01-03": 8,
    "2025-01-04": 12,
    "2025-01-05": 20,
    "2025-01-06": 5,
    "2025-01-07": 0
  },
  "total": 70
}
```

### Ejemplo 4: Buscar Análisis

```bash
curl "http://localhost:8000/api/v1/search?q=product&limit=10"
```

**Response:**
```json
[
  {
    "id": 1,
    "text": "Great product!",
    "label": "POSITIVE",
    "score": 0.9995,
    ...
  },
  {
    "id": 15,
    "text": "Love this product",
    "label": "POSITIVE",
    "score": 0.9987,
    ...
  }
]
```

### Ejemplo 5: Filtrar Historial

```bash
# Solo sentimientos positivos
curl "http://localhost:8000/api/v1/history?label=POSITIVE"

# Solo con score > 0.9
curl "http://localhost:8000/api/v1/history?min_score=0.9"

# Combinado
curl "http://localhost:8000/api/v1/history?label=POSITIVE&min_score=0.95&page_size=5"
```

---

## 🎓 CONCEPTOS TÉCNICOS APLICADOS

### 1. **SQLAlchemy ORM**
```python
# Define modelo como clase Python
class SentimentAnalysis(Base):
    __tablename__ = "sentiment_analyses"
    id = Column(Integer, primary_key=True)
    text = Column(Text, nullable=False)
    # ...

# SQLAlchemy lo convierte a tabla SQL automáticamente
```

### 2. **Dependency Injection con FastAPI**
```python
@router.get("/history")
async def get_history(db: Session = Depends(get_db)):
    # FastAPI automáticamente:
    # 1. Llama get_db()
    # 2. Obtiene sesión de DB
    # 3. La pasa como parámetro
    # 4. La cierra al terminar (finally block)
    analyses = db.query(SentimentAnalysis).all()
```

### 3. **Paginación**
```python
# Calcular skip y limit
skip = (page - 1) * page_size  # Página 2, size 20 → skip 20
query.offset(skip).limit(page_size)  # SQL: OFFSET 20 LIMIT 20
```

### 4. **Queries con Filtros**
```python
query = db.query(SentimentAnalysis)
if label:
    query = query.filter(SentimentAnalysis.label == label)
if min_score:
    query = query.filter(SentimentAnalysis.score >= min_score)
results = query.all()  # Ejecuta query final
```

### 5. **Agregaciones SQL**
```python
# Contar por grupo
db.query(
    func.date(SentimentAnalysis.created_at).label('date'),
    func.count(SentimentAnalysis.id).label('count')
).group_by(func.date(SentimentAnalysis.created_at))

# Promedio
avg_score = db.query(func.avg(SentimentAnalysis.score)).scalar()
```

---

## 🔄 FLUJO COMPLETO CON BASE DE DATOS

```
Usuario → POST /api/v1/analyze
            ↓
      FastAPI valida input
            ↓
      Endpoint analyze_sentiment()
            ↓
      analyzer.analyze(text)
            ↓
      Guarda en DB (crud.create_analysis)
            ↓
      Retorna respuesta al usuario
            ↓
      Usuario puede consultar:
      - GET /history → Ver análisis guardado
      - GET /stats → Ver en estadísticas
      - GET /search → Encontrarlo buscando
```

---

## 📊 ESTRUCTURA ACTUALIZADA DEL PROYECTO

```
sentiment-analysis-api/
├── src/
│   ├── models/
│   │   └── sentiment_model.py      ← Día 1 ✅
│   ├── api/
│   │   ├── main.py                  ← Día 2 ✅ (actualizado)
│   │   ├── config.py                ← Día 2 ✅ (actualizado)
│   │   ├── schemas.py               ← Día 2 ✅ (actualizado)
│   │   └── routes/
│   │       └── sentiment.py         ← Día 2 ✅ (actualizado)
│   ├── database/                    ← Día 3 ✅ NUEVO
│   │   ├── __init__.py
│   │   ├── models.py                ← Modelos SQLAlchemy
│   │   ├── database.py              ← Configuración DB
│   │   └── crud.py                  ← Operaciones CRUD
│   └── utils/
├── tests/
│   ├── test_model.py                ← Día 1 ✅
│   └── test_api.py                  ← Día 2 ✅
├── sentiment_analysis.db            ← Base de datos SQLite (auto-creada)
└── ...
```

---

## 🔜 PRÓXIMO: DÍA 4 - PRODUCTION DEPLOYMENT

**Objetivos:**
1. ✅ Configuración de producción
2. ✅ Deploy en Render/Railway
3. ✅ Variables de entorno
4. ✅ Optimizaciones
5. ✅ Documentación final

**Entregables esperados:**
- ✅ API en producción (URL pública)
- ✅ PostgreSQL en la nube
- ✅ Documentación completa
- ✅ Portfolio-ready

**Tiempo estimado**: 3-4 horas

---

## 💡 PARA ENTREVISTAS

**Puntos a destacar del Día 3:**
- "Implementé persistencia con SQLAlchemy ORM"
- "Base de datos con PostgreSQL y SQLite dual support"
- "API RESTful completa con historial, stats y búsqueda"
- "Paginación eficiente y filtros múltiples"
- "Queries agregadas con SQL functions"
- "Dependency injection para manejo de sesiones"

---

## 🐛 TROUBLESHOOTING

**Problema**: Base de datos no se crea
```bash
# Verificar logs
python run_api.py
# Buscar: "Initializing database..."

# Crear manualmente
python -c "from database.database import init_db; init_db()"
```

**Problema**: Error con PostgreSQL
```bash
# Verificar conexión
psql -h localhost -U sentiment_user -d sentiment_db

# Verificar DATABASE_URL en .env
echo $DATABASE_URL
```

**Problema**: Historial vacío después de análisis
```bash
# Verificar que se guardó
sqlite3 sentiment_analysis.db "SELECT COUNT(*) FROM sentiment_analyses;"

# Ver último registro
sqlite3 sentiment_analysis.db "SELECT * FROM sentiment_analyses ORDER BY id DESC LIMIT 1;"
```

---

## ✨ LOGROS DEL DÍA 3

✅ Persistencia completa de datos
✅ 4 endpoints nuevos funcionando
✅ Historial paginado con filtros
✅ Estadísticas agregadas
✅ Timeline para visualización
✅ Búsqueda de texto completo
✅ Dual database support (SQLite/PostgreSQL)
✅ CRUD operations completo

**Progreso total**: 75% (3/4 días)

---

¿Listo para el Día 4 (Deploy a producción)? 🚀
